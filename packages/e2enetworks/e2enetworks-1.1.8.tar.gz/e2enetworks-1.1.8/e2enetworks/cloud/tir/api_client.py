import json
from typing import Optional

import requests

from e2enetworks.cloud.tir import client
from e2enetworks.cloud.tir.constants import MODEL_NAME_TO_URL_PATH_MAPPING
from e2enetworks.cloud.tir.helpers import (get_formated_data_for_model,
                                           get_model_url, get_random_string)
from e2enetworks.cloud.tir.minio_service import MinioService
from e2enetworks.cloud.tir.utils import prepare_object
from e2enetworks.constants import (BASE_GPU_URL, BUCKET_TYPES, MANAGED_STORAGE,
                                   MODEL_TYPES, headers)


class ModelAPIClient:
    def __init__(self, team: Optional[str] = "", project: Optional[str] = ""):
        client_not_ready = (
            "Client is not ready. Please initiate client by:"
            "\n- Using e2enetworks.cloud.tir.init(...)"
        )
        if not client.Default.ready():
            raise ValueError(client_not_ready)

        if project:
            client.Default.set_project(project)

        if team:
            client.Default.set_team(team)

    def infer(self, model_name, data):
        namespace = "p-" + str(client.Default.project())
        try:
            url_status, url = get_model_url(model_name, namespace)
            if not url_status:
                raise Exception(f"Invalid input Error {url} model not present")
            data_status, data = get_formated_data_for_model(model_name, data)
            if not data_status:
                raise Exception(f"Invalid data key Error {str(data)}")

        except Exception as e:
            raise Exception(f"Input Error {e}")
        headers["Authorization"] = f"Bearer {client.Default.access_token()}"
        response = requests.post(url=url, headers=headers, data=json.dumps(data))
        response = prepare_object(response)
        return response

    def list(self):
        response = MODEL_NAME_TO_URL_PATH_MAPPING.keys()
        return list(response)

    @staticmethod
    def help():
        print("ModelAPIClient Class Help")
        print("\t\t=================")
        print("\t\tThis class provides functionalities to infer with models.")
        print("\t\tAvailable methods:")
        print(
            "\t\t1. __init__(team, project): Initializes a Models instance with the specified team and project "
            "IDs."
        )
        print("\t\t2. list(): List all available models" "details.")
        print(
            "\t\t3. infer(model_name, data): Infer model with the provided "
            "details."
        )
        print("\t\t4. help(): Displays this help message.")

        # Example usages
        print("\t\tExample usages:")
        print("\t\tmodelclient = ModelAPIClient(123, 456)")
        print(f"\t\tmodelclient.list()")
        print(f"\t\tmodelclient.infer(model_name, data)")
