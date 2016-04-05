# Copyright 2016 Nokia
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
from oslo_log import log as logging

from vitrage_tempest_tests.tests.api.base import BaseVitrageTest
from vitrage_tempest_tests.tests.api.utils.alarms \
    import AlarmsHelper

LOG = logging.getLogger(__name__)


class BaseAlarmsTest(BaseVitrageTest):
    """Alarms test class for Vitrage API tests."""

    def __init__(self):
        super(BaseAlarmsTest, self).__init__()
        self.alarms_client = AlarmsHelper()

    def test_compare_alarms(self):
        """Wrapper that returns a test graph."""
        api_alarms = self.alarms_client.get_api_alarms()
        cli_alarms = self.alarms_client.get_all_alarms()

        if self.alarms_client.compare_alarms_lists(
                api_alarms, cli_alarms) is False:
            LOG.error('The alarms list is not correct')
        else:
            LOG.info('The alarms list is correct')

    def test_nova_alarms(self):
        """Wrapper that returns test nova alarms."""
        self.alarms_client.create_alarms_per_component("nova")
        alarms = self.alarms_client.get_all_alarms()
        nova_alarms = self.alarms_client.filter_alarms(alarms, "nova")

        if self.alarms_client.validate_alarms_correctness(
                nova_alarms, "nova") is False:
            LOG.error('The nova alarms are not correct')
        else:
            LOG.info('The nova alarms are correct')

    def test_nagios_alarms(self):
        """Wrapper that returns test nagios alarms."""
        self.alarms_client.create_alarms_per_component("nagios")
        alarms = self.alarms_client.get_all_alarms()
        nagios_alarms = self.alarms_client.filter_alarms(alarms, "nagios")

        if self.alarms_client.validate_alarms_correctness(
                nagios_alarms, "nagios") is False:
            LOG.error('The nagios alarms are not correct')
        else:
            LOG.info('The nagios alarms are correct')

    def test_aodh_alarms(self):
        """Wrapper that returns test aodh alarms."""
        self.alarms_client.create_alarms_per_component("aodh")
        alarms = self.alarms_client.get_all_alarms()
        aodh_alarms = self.alarms_client.filter_alarms(alarms, "aodh")

        if self.alarms_client.validate_alarms_correctness(
                aodh_alarms, "aodh") is False:
            LOG.error('The aodh alarms are not correct')
        else:
            LOG.info('The aodh alarms are correct')