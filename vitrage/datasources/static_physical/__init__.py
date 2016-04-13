# Copyright 2016 - Nokia
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR  CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from oslo_config import cfg

STATIC_PHYSICAL_DATASOURCE = 'static_physical'
SWITCH = 'switch'

OPTS = [
    cfg.StrOpt('transformer',
               default='vitrage.datasources.static_physical.transformer.'
                       'StaticPhysicalTransformer',
               help='Static physical transformer class path',
               required=True),
    cfg.StrOpt('driver',
               default='vitrage.datasources.static_physical.driver.'
                       'StaticPhysicalDriver',
               help='Static physical driver class path',
               required=True),
    cfg.IntOpt('changes_interval',
               default=5,
               min=5,
               help='interval between checking changes in the configuration '
                    'files of the physical topology data sources',
               required=True),
    cfg.StrOpt('directory', default='/etc/vitrage/static_datasources',
               help='Static physical data sources directory'),
    cfg.ListOpt('entities',
                default=[SWITCH],
                help='Static physical entity types list')
]