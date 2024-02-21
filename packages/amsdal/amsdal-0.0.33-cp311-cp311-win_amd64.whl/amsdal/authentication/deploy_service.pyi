from amsdal.authentication.handlers.base import AMSDAL_ENV_SUBDOMAIN as AMSDAL_ENV_SUBDOMAIN, ENCRYPT_PUBLIC_KEY as ENCRYPT_PUBLIC_KEY
from amsdal.authentication.handlers.client_service import AuthClientService as AuthClientService
from amsdal.configs.main import settings as settings
from amsdal.errors import AmsdalDeployError as AmsdalDeployError
from pydantic import BaseModel
from typing import Any

def _input(msg: str) -> str: ...
def _print(msg: str) -> None: ...
def want_deploy_input() -> str: ...
def want_redeploy_input() -> str: ...

DEPLOY_API_TIMEOUT: int

class DefaultResponse(BaseModel):
    status: str
    errors: list[str] | None

class DeployModel(BaseModel):
    deployment_id: str
    status: str

class DeployResponseBaseModel(DefaultResponse):
    details: dict[str, Any] | None

class DeploymentResponse(BaseModel):
    status: str
    client_id: str
    deployment_id: str
    created_at: float
    last_update_at: float
    application_uuid: str | None
    application_name: str | None

class UpdateDeployResponseModel(BaseModel):
    status: str
    deployment_id: str
    created_at: float
    last_update_at: float
    updated: bool

class ListDeployResponseModel(BaseModel):
    deployments: list[DeploymentResponse]

class ListSecretsResponse(DefaultResponse):
    secrets: list[str]

class DeployService:
    @classmethod
    def _credentials_data(cls) -> bytes: ...
    @classmethod
    def deploy_prompt(cls, deploy_type: str, lakehouse_type: str, application_uuid: str | None = None, application_name: str | None = None) -> bool: ...
    @classmethod
    def _redeploy(cls, deploy_data: dict[str, Any]) -> bool: ...
    @classmethod
    def list_deploys(cls) -> ListDeployResponseModel | None: ...
    @classmethod
    def update_deploy(cls, deployment_id: str) -> UpdateDeployResponseModel | None: ...
    @classmethod
    def destroy_deploy(cls, deployment_id: str) -> bool: ...
    @classmethod
    def add_secret(cls, secret_name: str, secret_value: str, application_uuid: str | None = None, application_name: str | None = None) -> bool: ...
    @classmethod
    def list_secrets(cls, application_uuid: str | None = None, application_name: str | None = None, *, with_values: bool = False) -> ListSecretsResponse | None: ...
    @classmethod
    def delete_secret(cls, secret_name: str, application_uuid: str | None = None, application_name: str | None = None) -> bool: ...
