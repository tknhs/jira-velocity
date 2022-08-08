from pydantic import BaseSettings, Field


class JiraConfig(BaseSettings):
    server_uri: str = Field(..., env="SERVER_URI")
    user: str = Field(..., env="AUTH_USERNAME")
    api_token: str = Field(..., env="AUTH_API_TOKEN")
    project_id: str = Field(..., env="PROJECT_ID")
