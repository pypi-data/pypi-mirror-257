from superwise_api.client import ToolCreate
from superwise_api.client import ToolUpdateSQLDatabase
from superwise_api.client.api.tools_api import ToolsApi
from superwise_api.errors import raise_exception


class Tool:
    """
    *ToolsApi* | [**create_tool**](client/docs/ToolsApi.md#create_tool) | **POST** /v1/applications/{application_id}/tools | Create Tool

    *ToolsApi* | [**delete_tool**](client/docs/ToolsApi.md#delete_tool) | **DELETE** /v1/applications/{application_id}/tools/{tool_id} | Delete Tool

    *ToolsApi* | [**get_tool**](client/docs/ToolsApi.md#get_tool) | **GET** /v1/applications/{application_id}/tools/{tool_id} | Get Tool

    *ToolsApi* | [**get_tools**](client/docs/ToolsApi.md#get_tools) | **GET** /v1/applications/{application_id}/tools | Get Tools

    *ToolsApi* | [**update_tool**](client/docs/ToolsApi.md#update_tool) | **PATCH** /v1/applications/{application_id}/tools/{tool_id} | Update Tool
    """

    def __init__(self, client):
        self.api = ToolsApi(client)

    @raise_exception
    def create(self, application_id: str, tool_payload: ToolCreate, **kwargs):
        """
        Create a tool for the application.

        Parameters:

        - **application_id**: UUID of the application.
        - **payload**: Information about the tool to be created which should match one of the following configurations based on the tool type:
            - **SQL Database Tool**π
                - **name**: A human-readable name for the tool.
                - **description**: A brief summary describing the tool's purpose or use. This description will be a part of the prompt that the LLM uses for the database.
                - **type**: An identifier for the tool type, specifically for SQL databases in this case.
                - **secrets**: Connection information required to access the SQL database, such as a connection string.
        """
        return self.api.create_tool(application_id, tool_payload, **kwargs)

    @raise_exception
    def get_tool_by_id(self, application_id: str, tool_id: str, **kwargs):
        """
        Retrieve a Tool based on the given tool_id.

        - **application_id**: UUID of the application.
        - **tool_id**: UUID of the tool.
        """
        return self.api.get_tool(application_id, tool_id, **kwargs)

    @raise_exception
    def get_tools(self, application_id: str, **kwargs):
        """
        Retrieve Tools under a given application ID based on the provided filters.

        - **application_id**: UUID of the application.
        - **name**: Name of the tool.
        - **type**: Type of the tool.
        """
        return self.api.get_tools(application_id, **kwargs)

    @raise_exception
    def delete_tool(self, application_id: str, tool_id: str, **kwargs):
        """
        Delete a tool based on the given tool_id.

        - **application_id**: UUID of the application.
        - **tool_id**: UUID of the tool.
        """
        return self.api.delete_tool(application_id, tool_id, **kwargs)

    @raise_exception
    def update_tool(self, application_id: str, tool_id: str, tool_update: ToolUpdateSQLDatabase, **kwargs):
        """
        Update a tool based on the given tool_id.

        - **application_id**: UUID of the application.
        - **tool_id**: UUID of the tool.
        - **tool_update**: Information about the tool to be updated.
        """
        return self.api.update_tool(application_id, tool_id, tool_update, **kwargs)
