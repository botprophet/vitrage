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

from oslo_log import log as logging
from oslo_utils import importutils

from vitrage.common.constants import SynchronizerProperties as SyncProps
from vitrage.common.exception import VitrageTransformerError
from vitrage.common.utils import opt_exists
from vitrage.evaluator.actions.evaluator_event_transformer import \
    EvaluatorEventTransformer
from vitrage.evaluator.actions.evaluator_event_transformer import VITRAGE_TYPE

LOG = logging.getLogger(__name__)
ENTITIES = 'entities'


class TransformerManager(object):

    def __init__(self, conf):
        self.transformers = self.register_transformer_classes(conf)

    @staticmethod
    def register_transformer_classes(conf):

        transformers = {}
        for plugin in conf.synchronizer_plugins.plugin_type:
            transformers[plugin] = importutils.import_object(
                conf[plugin].transformer,
                transformers)
            if opt_exists(conf[plugin], ENTITIES):
                for entity in conf[plugin].entities:
                    transformers[entity] = importutils.import_object(
                        conf[plugin].transformer, transformers)

        transformers[VITRAGE_TYPE] = importutils.import_object(
            "%s.%s" % (EvaluatorEventTransformer.__module__,
                       EvaluatorEventTransformer.__name__), transformers)

        return transformers

    def get_transformer(self, key):

        try:
            transformer = self.transformers[key]
        except KeyError:
            raise VitrageTransformerError(
                'Could not get transformer instance for %s' % key)

        return transformer

    def transform(self, entity_event):
        sync_type = self._get_sync_type(entity_event)
        LOG.debug('TRANSFORMER EVENT: %s', sync_type)
        LOG.debug('Event:\n%s', entity_event)
        return self.get_transformer(sync_type).transform(entity_event)

    def enrich_event(self, entity_event, graph):
        sync_type = self._get_sync_type(entity_event)
        return self.get_transformer(sync_type).enrich_event(entity_event,
                                                            graph)

    def extract_key(self, entity_event):
        sync_type = self._get_sync_type(entity_event)
        return self.get_transformer(sync_type)._create_entity_key()

    @staticmethod
    def _get_sync_type(entity_event):
        try:
            return entity_event[SyncProps.SYNC_TYPE]
        except KeyError:
            raise VitrageTransformerError(
                'Entity Event must contains sync_type field.')
