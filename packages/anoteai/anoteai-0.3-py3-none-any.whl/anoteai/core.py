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


# # Example usage:
# if __name__ == "__main__":
    # api_key = '3b884dd8c85b6a7aee62d2e0dea116bb'

    # anote = Anote(api_key)

    # create_response = anote.create_dataset(task_type=0, name='Spam or Not Spam')
    # print("create_response")
    # print(create_response)

#     datasetId = create_response["id"]

#     # Upload a file
#     upload_response = anote.upload(file_path='emails.txt', dataset_id=datasetId, decomposition_type=0)
#     print(upload_response)

#     # Assuming successful upload, customize the public dataset
#     spam_category_response = anote.customize(name='Spam', dataset_id=datasetId)
#     print(spam_category_response)

#     not_spam_category_response = anote.customize(name='Not Spam', dataset_id=datasetId)
#     print(not_spam_category_response)

#     # Get the next parsed text block to annotate
#     next_text_block_response = anote.get_next_text_block(dataset_id=datasetId)
#     next_text_block_id = next_text_block_response['id']
#     print(next_text_block_id)

#     # Annotate the public dataset
#     spam_annotate_response = anote.annotate(id=next_text_block_id, specified_entities=None, category_ids=[spam_category_response["id"]], is_delete=False)
#     print(spam_annotate_response)

#     next_text_block_response = anote.get_next_text_block(dataset_id=datasetId)
#     next_text_block_id = next_text_block_response['id']
#     print(next_text_block_id)

#     not_spam_annotate_response = anote.annotate(id=next_text_block_id, specified_entities=None, category_ids=[not_spam_category_response["id"]], is_delete=False)
#     print(not_spam_annotate_response)

#     # Train public model
#     train_response = anote.train(dataset_id=datasetId)
#     print(train_response)

#     # Wait for training to complete
#     time.sleep(15)  # 120 seconds = 2 minutes

#     newEmail = "The Nigerian prince is expecting your payment of $10,000"

#     predict_response = anote.predict(dataset_id=datasetId, text=newEmail)
#     print(predict_response)
