from typing import Dict, Optional

from pydantic import SecretStr

from promptquality.constants.integrations import IntegrationName
from promptquality.set_config import set_config
from promptquality.types.config import Config
from promptquality.types.run import CreateIntegrationRequest


def add_openai_integration(
    api_key: str, organization_id: Optional[str] = None, config: Optional[Config] = None
) -> None:
    config = config or set_config()
    config.api_client.put_integration(
        integration_request=CreateIntegrationRequest(
            api_key=SecretStr(api_key), name=IntegrationName.openai, organization_id=organization_id
        ),
    )


def add_azure_integration(
    api_key: str, endpoint: str, headers: Optional[Dict[str, str]] = None, config: Optional[Config] = None
) -> None:
    config = config or set_config()
    config.api_client.put_integration(
        integration_request=CreateIntegrationRequest(
            api_key=SecretStr(api_key),
            name=IntegrationName.azure,
            endpoint=endpoint,
            headers=headers,
        ),
    )
