from superwise_api.client import ApplicationCreate
from superwise_api.client import ApplicationsApi
from superwise_api.client import ApplicationUpdate
from superwise_api.client import AskRequestPayload
from superwise_api.errors import raise_exception


class Application:
    """
    Method | HTTP request | Description
    ------------- | ------------- | -------------
    **ask** | **POST** /v1/applications/ask | Ask
    **create_application** | **POST** /v1/applications | Create Application
    """

    def __init__(self, client):
        self.api = ApplicationsApi(client)

    @raise_exception
    def create(self, application_create: ApplicationCreate, **kwargs):
        """
        Create a new application.

        Parameters:

        - **payload**: Instance of ApplicationCreate model.
            - **name**: Name of the application.
            - **model_id**: UUID of the model.
            - **prompt**: Prompt for the application.
        """
        return self.api.create_application(application_create, **kwargs)

    @raise_exception
    def ask(self, application_id: str, ask_request_payload: AskRequestPayload, **kwargs):
        """
        Ask the application a question.

        Parameters:

        - **payload**: Instance of AskRequestPayload model.
            - **input**: Input to the application.
            - **config**: Configuration for the application is an ApplicationCreate model.
                - **name**: Name of the application.
                - **model_id**: UUID of the model.
                - **prompt**: Prompt for the application.
            - **chat_history**: Chat history for the application is a List[ChatHistoryEntry].
                - **role**: Role of the chat history entry. (HUMAN or AI)
                - **message**: Message of the chat history entry.
        """
        return self.api.ask(application_id, ask_request_payload, **kwargs)

    @raise_exception
    def get_applications(self, **query_params):
        """
        Get all applications. Filter if provided with name, created_by, model_id, or prompt.

        Parameters:
        - **name**: Name of the application. (optional)
        - **created_by**: User ID of the user who created the application. (optional)
        - **model_id**: UUID of the model. (optional)
        - **prompt**: Prompt for the application. (optional)
        """
        return self.api.get_applications(**query_params)

    @raise_exception
    def get_application_by_id(self, application_id: str, **kwargs):
        """
        Get an application by its id.

        Parameters:

        - **application_id**: UUID of the application.
        """
        return self.api.get_application(application_id, **kwargs)

    @raise_exception
    def update(self, application_id: str, application_update: ApplicationUpdate, **kwargs):
        """
        Update an application.

        Parameters:

        - **application_id**: UUID of the application.
        - **payload**: Instance of ApplicationUpdate model.
            - **name**: Name of the application. (optional)
            - **model_id**: UUID of the model. (optional)
            - **prompt**: Prompt for the application. (optional)
        """
        return self.api.update_application(application_id, application_update, **kwargs)
