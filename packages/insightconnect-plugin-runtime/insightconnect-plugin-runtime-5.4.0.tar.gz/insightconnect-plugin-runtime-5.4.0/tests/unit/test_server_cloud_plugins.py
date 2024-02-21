from requests.exceptions import HTTPError, Timeout, TooManyRedirects
from parameterized import parameterized
from unittest import TestCase
from unittest.mock import patch, MagicMock

from insightconnect_plugin_runtime.server import PluginServer, DEFAULT_SCHEDULE_INTERVAL_MINUTES
from tests.plugin.hello_world import KomandHelloWorld
from .utils import MockResponse, Logger

SCHEDULE_INTERVAL, PLUGIN_VALUE_1, PLUGIN_VALUE_2 = 25, {"*": 24}, {"org_1": "Tues 14th Sept 2024"}


@patch("gunicorn.arbiter.Arbiter.run", side_effect=MagicMock())
@patch("insightconnect_plugin_runtime.server.is_running_in_cloud", return_value=True)
class TestServerCloudPlugins(TestCase):
    def setUp(self) -> None:
        self.plugin = KomandHelloWorld()
        self.plugin_name = self.plugin.name.lower().replace(" ", "_")

    @parameterized.expand([["Set cloud to false", False], ["Set cloud to true", True]])
    @patch("insightconnect_plugin_runtime.server.PluginServer.register_scheduled_tasks")
    @patch("insightconnect_plugin_runtime.server.request_get")
    def test_cloud_plugin_no_tasks_ignore_cps(self, _test_name, cloud, mocked_req, mocked_scheduler, mock_cloud, _run):
        mock_cloud.return_value = cloud  # Mock plugin running in cloud vs not
        self.plugin.tasks = None  # ensure still no tasks as other tests edit this and could fail before reverting
        plugin_server = PluginServer(self.plugin)  # this plugin has no tasks by default

        plugin_server.start()
        self.assertEqual(plugin_server.config_options, {})
        self.assertEqual(plugin_server.schedule_interval, None)

        # Depending on if we're running cloud or not this could be called but we only reach to CPS if we have tasks
        self.assertEquals(mocked_scheduler.called, cloud)

        # Plugin server never calls out to CPS as either we are not running in cloud mode or have no tasks.
        self.assertFalse(mocked_req.called)

    @patch("insightconnect_plugin_runtime.server.PluginServer.register_scheduled_tasks")
    @patch("insightconnect_plugin_runtime.server.request_get")
    def test_cloud_plugin_calls_cps(self, mocked_req, mocked_scheduler, _mock_cloud, _run):
        mocked_req.return_value = MockResponse({"plugins":{self.plugin_name: PLUGIN_VALUE_1, 'plugin': PLUGIN_VALUE_2},
                                                "config": {"interval": 25}})
        self.plugin.tasks = 'fake tasks'  # this plugin by default has no tasks so force it to have some
        plugin_server = PluginServer(self.plugin)
        plugin_server.start()

        # Plugin server should call out to CPS and save the response
        self.assertTrue(mocked_req.called)

        # We only save the plugin config for the current config and ignore `other_plugin`
        self.assertDictEqual(plugin_server.config_options, PLUGIN_VALUE_1)
        self.assertEqual(plugin_server.schedule_interval, SCHEDULE_INTERVAL)

        # We should now schedule this to run
        self.assertEquals(mocked_scheduler.called, True)
        self.plugin.tasks = None  # reset tasks value

    @parameterized.expand([["error", HTTPError], ["error", Timeout], ["unexpected", TooManyRedirects]])
    @patch("insightconnect_plugin_runtime.server.PluginServer.register_scheduled_tasks")
    @patch("insightconnect_plugin_runtime.server.request_get")
    @patch("structlog.get_logger")
    def test_cps_schedule_raises_an_error(self, test_cond, exception, log, mocked_req, _mocked_scheduler, _mock_cloud, _run):
        log.return_value = Logger()
        # If we have successfully got config and scheduler options, and later this call fails we should keep values
        mocked_req.return_value = MockResponse({"plugins": {self.plugin_name: PLUGIN_VALUE_1, 'plugin': PLUGIN_VALUE_2},
                                                "config": {"unused_config": "value"}})
        self.plugin.tasks = 'fake tasks'  # this plugin by default has no tasks so force it to have some
        self.plugin.name = "plugin"  # force to use next plugin name from previous test
        plugin_server = PluginServer(self.plugin)
        plugin_server.start()

        self.assertDictEqual(plugin_server.config_options, PLUGIN_VALUE_2)
        self.assertEqual(plugin_server.schedule_interval, DEFAULT_SCHEDULE_INTERVAL_MINUTES)  # no resp uses default

        # First call has happened and now successful - force scheduler to hit specific handled and unexpected errors.
        mocked_req.side_effect = exception("Warning HTTP error returned...")
        plugin_server.get_plugin_properties_from_cps()
        # we log error in all and `unexpected` in TooManyRedirects as there is no direct catch for this
        self.assertIn(test_cond, plugin_server.logger.last_error)

        # Values should not have changed
        self.assertDictEqual(plugin_server.config_options, PLUGIN_VALUE_2)
        self.assertEqual(plugin_server.schedule_interval, DEFAULT_SCHEDULE_INTERVAL_MINUTES)

        # Next schedule returns updated values, new schedule and no configurations for plugins
        new_schedule = 12345678
        mocked_req.return_value = MockResponse({"config": {"interval": new_schedule}})
        mocked_req.side_effect = None
        plugin_server.get_plugin_properties_from_cps()

        # And this new values are now updated for the plugin server
        self.assertDictEqual(plugin_server.config_options, {})
        self.assertEqual(plugin_server.schedule_interval, new_schedule)

        self.plugin.tasks = None  # reset tasks value
