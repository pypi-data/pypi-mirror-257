import requests
import json
# import time

class Anote:
    def __init__(self, api_key):
        self.API_BASE_URL = 'http://localhost:5000'
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {api_key}'
        }

    def create_dataset(self, task_type, name):
        url = f"{self.API_BASE_URL}/public/createDataset"
        data = json.dumps({
            "taskType": task_type,
            "name": name
        })
        response = requests.post(url, data=data, headers=self.headers)
        print(response)

        return response.json()

    def upload(self, file_path, dataset_id, decomposition_type):
        url = f"{self.API_BASE_URL}/public/upload"
        form_data = {
            'decompositionType': decomposition_type,
            'datasetId': dataset_id
        }
        files = {
            'files[]': (file_path, open(file_path, 'rb'))
        }
        response = requests.post(url, headers=self.headers, data=form_data, files=files)
        return response.json()

    def customize(self, name, dataset_id, parent_category_id=None, prompt_text=None, is_structured_prompt=None):
        url = f"{self.API_BASE_URL}/public/customize"
        data = json.dumps({
            "name": name,
            "datasetId": dataset_id,
            "parentCategoryId": parent_category_id,
            "promptText": prompt_text,
            "isStructuredPrompt": is_structured_prompt
        })
        response = requests.post(url, data=data, headers=self.headers)
        return response.json()

    def get_next_text_block(self, dataset_id):
        url = f"{self.API_BASE_URL}/public/getNextTextBlock"
        params = {'datasetId': dataset_id}
        response = requests.get(url, params=params, headers=self.headers)

        if response.status_code != 200:
            return {"error": response.text}, response.status_code

        return response.json()

    def annotate(self, id, specified_entities, category_ids, is_delete):
        url = f"{self.API_BASE_URL}/public/annotate"
        data = json.dumps({
            "id": id,
            "specifiedEntities": specified_entities,
            "categoryIds": category_ids,
            "isDelete": is_delete
        })
        response = requests.post(url, data=data, headers=self.headers)
        return response.json()

    def train(self, dataset_id):
        url = f"{self.API_BASE_URL}/public/train"
        data = json.dumps({
            "id": dataset_id
        })
        response = requests.post(url, data=data, headers=self.headers)
        return response.json()

    def predict(self, dataset_id, text):
        url = f"{self.API_BASE_URL}/public/predict"
        data = json.dumps({
            "id": dataset_id,
            "text": text
        })
        response = requests.post(url, data=data, headers=self.headers)
        return response.json()