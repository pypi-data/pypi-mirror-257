"""
    QuaO Project dwave_system_provider.py Copyright © CITYNOW Co. Ltd. All rights reserved.
"""

from dwave.system import DWaveSampler, AutoEmbeddingComposite

from ...enum.provider_tag import ProviderTag
from ...model.provider.provider import Provider
from ...config.logging_config import *


class DwaveSystemProvider(Provider):

    def __init__(self, api_token, endpoint):
        super().__init__(ProviderTag.D_WAVE)
        self.api_token = api_token
        self.endpoint = endpoint

    def get_backend(self, device_specification: str):
        logger.debug("[Dwave system] Get backend")

        provider = self.collect_provider()

        return AutoEmbeddingComposite(provider)

    def collect_provider(self):
        logger.debug("[Dwave system] Connect to provider")

        return DWaveSampler(endpoint=self.endpoint, token=self.api_token)
