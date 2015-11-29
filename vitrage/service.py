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

import keystoneclient.auth
import logging


from keystonemiddleware import opts as ks_opts
from oslo_config import cfg
from oslo_log import log
from oslo_policy import opts as policy_opts

from vitrage import opts

LOG = log.getLogger(__name__)


def prepare_service(args=None, default_opts=None, conf=None):
    if conf is None:
        conf = cfg.ConfigOpts()
    log.register_options(conf)
    for group, options in ks_opts.list_auth_token_opts():
        conf.register_opts(list(options), group=group)
    policy_opts.set_defaults(conf)

    for group, options in opts.list_opts():
        conf.register_opts(list(options),
                           group=None if group == "DEFAULT" else group)

    for opt, value, group in default_opts or []:
        conf.set_default(opt, value, group)

    conf(args, project='vitrage', validate_default_values=True)
    log.setup(conf, 'vitrage')
    conf.log_opt_values(LOG, logging.DEBUG)

    # NOTE(sileht): keystonemiddleware assume we use the global CONF object
    # (LP#1428317). In gnocchi, this is not the case, so we have to register
    # some keystoneclient options ourself. Missing options are hidden into
    # private area of keystonemiddleware and keystoneclient, so we
    # create a keystoneclient AuthPlugin object, that will register the options
    # into our configuration object. This have to be done after the
    # configuration files have been loaded because the authplugin options
    # depends of the authplugin present in the configuration file.
    keystoneclient.auth.register_conf_options(conf, 'keystone_authtoken')
    keystoneclient.auth.load_from_conf_options(conf, 'keystone_authtoken')
    return conf
