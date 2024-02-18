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
        req_headers = {"x-api-key": self._api_key}
        # Check if file exists
        if not os.path.exists(file_path):
            return {"error": "File not found."}

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
        if history is None:
            history = list()

        req_headers = {"x-api-key": self._api_key, "Content-Type": "application/json"}

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
            raise Exception({"error": "Upload failed",
                "status_code": response.status_code,
                "response": response.json()["error"]["message"]})
