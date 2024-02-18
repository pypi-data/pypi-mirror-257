import os

import requests
from werkzeug.utils import secure_filename


class Pipeline:
    API_URL = "https://vecflow-apis-2147-e82b72a8-4s59j2od.onporter.run"
    # API_URL = "http://127.0.0.1:5001"
    UPLOAD_ENDPOINT = "/files/upload"
    QUERY_ENDPOINT = "/query/completion"

    def __init__(self, name, api_key):
        self.name = name
        self._api_key = api_key

    # must use full path for uploading file
    def upload(self, file_path):
        """
        The `upload` function uploads a file to an API endpoint using the provided API key and returns
        the response.
        
        :param file_path: The `file_path` parameter is the path to the file that you want to upload. It
        should be a string representing the file's location on your local machine
        :return: a dictionary containing the response from the API endpoint. If the upload is
        successful, it returns the JSON response from the API. If there is an error, it raises an
        exception with an error message, status code, and the error message from the API response.
        """
        req_headers = {"Authorization": self._api_key}
        # Check if file exists
        if not os.path.exists(file_path):
            raise Exception({"error": "Upload failed",
                "response": "file not found at path provided"})

        # Open the file in binary mode for uploading
        with open(file_path, "rb") as file:
            files = {
                "file": (secure_filename(os.path.basename(file_path)), file),
            }
            data = {
                "pipeline_name": self.name,
            }

            # Send a POST request to the endpoint
            try:
                response = requests.post(
                    self.API_URL + self.UPLOAD_ENDPOINT,
                    files=files,
                    data=data,
                    headers=req_headers,
                )
            except requests.RequestException as e:
                return {"error": str(e)}

        # Check response status and handle appropriately
        if response.status_code == 200:
            return response.json()  # Assuming the successful response is JSON
        else:
            raise Exception({"error": "Upload failed",
                "status_code": response.status_code,
                "response": response.json()["error"]["message"]})


       
    def query(
        self, query, retrieval_method, llm_config, history=None, system_message=None
    ):
        """
        The `query` function sends a POST request to an API endpoint with the provided query, retrieval
        method, llm_config, history, and system_message, and returns the response as JSON if the status
        code is 200, otherwise raises an exception with the error message.
        
        :param query: The query parameter is the user's input query or question that they want to ask
        the system. It can be a string or any other data type that represents the query
        :param retrieval_method: The retrieval_method parameter specifies the method to be used for
        retrieving documents. It could be a string value indicating the retrieval method, such as
        "tfidf" or "bm25". The specific retrieval methods available may depend on the implementation of
        the API you are using
        :param llm_config: The `llm_config` parameter is a configuration object that specifies the
        settings for the Language Model (LLM) used in the query. It contains various properties such as
        the model name, temperature, max tokens, and other options that control the behavior of the LLM
        during the query. The specific
        :param history: The `history` parameter is a list that contains the conversation history. Each
        element in the list represents a message in the conversation. The messages should be in
        chronological order, with the most recent message at the end of the list
        :param system_message: The `system_message` parameter is an optional message that can be
        provided to the query function. It is typically used to pass additional information or
        instructions to the underlying system or model that processes the query. This message can be
        used to provide context or guidance to the system, which can help improve the relevance
        :return: the response from the API endpoint as a JSON object.
        """
        
        if history is None:
            history = list()

        req_headers = {"Authorization": self._api_key, "Content-Type": "application/json"}

        data = {
            "pipeline_name": self.name,
            "query": query,
            "llm_config": llm_config,
            "retrieval_method": retrieval_method,
            "history": history,
            "system_message": system_message,
        }

        # Send a POST request to the endpoint
        response = requests.post(
            self.API_URL + self.QUERY_ENDPOINT,
            json=data,  # Use json parameter to ensure data is properly encoded as JSON
            headers=req_headers,
        )

        if response.status_code == 200:
            return response.json()  # Assuming the successful response is JSON
        else:
            raise Exception({"error": "Query failed",
                "status_code": response.status_code,
                "response": response.json()["error"]["message"]})
