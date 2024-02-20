from abc import ABC, abstractmethod
from typing import Any, List, Optional

from pydantic.v1 import BaseModel, ConfigDict

from crewai_tools.tools.base_tool import BaseTool


class Adapter(BaseModel, ABC):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    @abstractmethod
    def query(self, question: str) -> str:
        """Query the knowledge base with a question and return the answer."""

class RagTool(BaseTool):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    name: str = "Knowledge base"
    description: str = "A knowledge base that can be used to answer questions."
    summarize: bool = False
    adapter: Optional[Adapter] = None
    app: Optional[Any] = None

    def _run(
        self,
        query: str,
    ) -> Any:
        from crewai_tools.adapters.embedchain_adapter import EmbedchainAdapter
        self.adapter = EmbedchainAdapter(embedchain_app=self.app, summarize=self.summarize)
        return f"Relevant Content:\n{self.adapter.query(query)}"

    # def from_pg_db(self, db_uri: str, table_name: str):
    #     from embedchain import App
    #     from embedchain.models.data_type import DataType
    #     from embedchain.loaders.postgres import PostgresLoader
    #     from crewai_tools.adapters.embedchain_adapter import EmbedchainAdapter

    #     config = { "url":  db_uri }
    #     postgres_loader = PostgresLoader(config=config)
    #     app = App()
    #     app.add(
    #         f"SELECT * FROM {table_name};",
    #         data_type='postgres',
    #         loader=postgres_loader
    #     )
    #     adapter = EmbedchainAdapter(embedchain_app=app)
    #     return RagTool(adapter=adapter)


    # def from_github_repo(self, gh_token: str, gh_repo: str, type: List[str] = ["repo"]):
    #     from embedchain import App
    #     from embedchain.loaders.github import GithubLoader
    #     from crewai_tools.adapters.embedchain_adapter import EmbedchainAdapter

    #     loader = GithubLoader(
    #         config={
    #             "token": gh_token,
    #             }
    #         )
    #     app = App()
    #     app.add(f"repo:{gh_repo} type:{','.join(type)}", data_type="github", loader=loader)
    #     adapter = EmbedchainAdapter(embedchain_app=app)
    #     return RagTool(adapter=adapter)

    # def from_youtube_channel(self, channel_handle: str):
    #     from embedchain.models.data_type import DataType
    #     if not channel_handle.startswith("@"):
    #         channel_handle = f"@{channel_handle}"
    #     return self._from_generic(channel_handle, DataType.YOUTUBE_CHANNEL)

    # def from_embedchain(self, config_path: str):
    #     from embedchain import App
    #     from crewai_tools.adapters.embedchain_adapter import EmbedchainAdapter

    #     app = App.from_config(config_path=config_path)
    #     adapter = EmbedchainAdapter(embedchain_app=app)
    #     return RagTool(name=self.name, description=self.description, adapter=adapter)

    # def _from_generic(self, source: str, type: str):
    #     from embedchain import App
    #     from crewai_tools.adapters.embedchain_adapter import EmbedchainAdapter
    #     app = App()
    #     app.add(source, data_type=type)
    #     adapter = EmbedchainAdapter(embedchain_app=app)
    #     return RagTool(name=self.name, description=self.description, adapter=adapter)