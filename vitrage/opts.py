# Copyright 2015 - Alcatel-Lucent
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
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import vitrage.api
import vitrage.entity_graph.consistency
import vitrage.evaluator
import vitrage.rpc
import vitrage.synchronizer
import vitrage.synchronizer.plugins


def list_opts():
    return [
        ('api', vitrage.api.OPTS),
        ('synchronizer', vitrage.synchronizer.OPTS),
        ('evaluator', vitrage.evaluator.OPTS),
        ('synchronizer_plugins', vitrage.synchronizer.plugins.OPTS),
        ('consistency', vitrage.entity_graph.consistency.OPTS),
        ('entity_graph', vitrage.entity_graph.OPTS),
        ('DEFAULT', vitrage.rpc.OPTS)
    ]
