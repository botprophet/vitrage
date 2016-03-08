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

import oslo_messaging

from oslo_policy import policy
from pecan import hooks

from vitrage import rpc as vitrage_rpc


class ConfigHook(hooks.PecanHook):
    """Attach the configuration and policy enforcer object to the request. """

    def __init__(self, conf):
        self.conf = conf
        self.enforcer = policy.Enforcer(conf)

    def before(self, state):
        # TODO(dany) add Context
        state.request.cfg = self.conf
        state.request.enforcer = self.enforcer


class RPCHook(hooks.PecanHook):
    """Create and attach an rpc to the request. """

    def __init__(self, conf):
        transport = oslo_messaging.get_transport(conf)
        target = oslo_messaging.Target(topic=conf.rpc_topic)
        self.client = vitrage_rpc.get_client(transport, target)
        self.ctxt = {}

    def before(self, state):
        state.request.client = self.client


class TranslationHook(hooks.PecanHook):

    def after(self, state):
        # After a request has been done, we need to see if
        # ClientSideError has added an error onto the response.
        # If it has we need to get it info the thread-safe WSGI
        # environ to be used by the ParsableErrorMiddleware.
        if hasattr(state.response, 'translatable_error'):
            state.request.environ['translatable_error'] = (
                state.response.translatable_error)
