# Copyright 2016 - Alcatel-Lucent
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

from oslo_log import log as logging

from algorithm import GraphAlgorithm
from sub_graph_matching import subgraph_matching
from vitrage.graph.driver import NXGraph
from vitrage.graph.query import create_predicate

LOG = logging.getLogger(__name__)


class NXAlgorithm(GraphAlgorithm):

    def __init__(self, graph):
        """Create a new GraphAlgorithm

        :param graph: graph instance
        :type graph: driver.Graph
        """
        super(NXAlgorithm, self).__init__(graph)

    def graph_query_vertices(self, query_dict=None, root_id=None, depth=None):

        if not root_id:
            root_id = self.graph.root_id
        root_data = self.graph._g.node[root_id]

        if not query_dict:
            match_func = lambda item: True
        else:
            match_func = create_predicate(query_dict)

        if not match_func(root_data):
            LOG.info('graph_query_vertices: root %s does not match filter %s',
                     str(root_id), str(query_dict))
            return None

        n_result = []
        visited_nodes = set()
        n_result.append(root_id)
        nodes_q = [(root_id, 0)]
        while nodes_q:
            node_id, curr_depth = nodes_q.pop(0)
            if (node_id in visited_nodes) or (depth and curr_depth >= depth):
                continue
            visited_nodes.add(node_id)
            (n_list, e_list) = self.graph._neighboring_nodes_edges_query(
                node_id, vertex_predicate=match_func)
            n_result.extend([v_id for v_id, data in n_list])
            nodes_q.extend([(v_id, curr_depth + 1) for v_id, data in n_list])

        graph = NXGraph('graph')
        graph._g = self.graph._g.subgraph(n_result)
        return graph

    def sub_graph_matching(self, subgraph, known_matches, validate=False):
        return subgraph_matching(self.graph, subgraph, known_matches, validate)
