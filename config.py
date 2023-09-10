from pydantic import Field
from pydantic_settings import BaseSettings

class JiraConfig(BaseSettings):
    server_uri: str = Field(..., alias="SERVER_URI")
    user: str = Field(..., alias="AUTH_USERNAME")
    api_token: str = Field(..., alias="AUTH_API_TOKEN")
    project_id: str = Field(..., alias="PROJECT_ID")
