import json
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder
import settings

class API():
    def __init__(self):
        self.base_url = "https://petfriends1.herokuapp.com/"


    def get_api_key(self, email: str,password: str) -> json:
        headers = {
            'email': email,
            'password': password
        }
        res = requests.get(self.base_url + 'api/key', headers=headers)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def get_list_of_pets(self, auth_key: json, filter: str = "") -> json:
        headers = {'auth_key': auth_key['key']}
        filter = {'filter': filter}
        res = requests.get(self.base_url + 'api/pets', headers=headers, params=filter)
        status = res.status_code
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def put_pet(self, auth_key: json,
                pet_id: str,
                name: str,
                animal_type: str,
                age: int, ) -> json:

        headers = {'auth_key': auth_key['key']}
        data = {
            "name": name,
            "animal_type": animal_type,
            "age": age}
        res = requests.put(self.base_url + 'api/pets/' + pet_id, headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def delete_pet(self, auth_key: json, pet_id: int) -> json:
        headers = {'auth_key': auth_key['key']}
        res = requests.delete(self.base_url + 'api/pets/' + str(pet_id), headers=headers)
        status = res.status_code
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result


    def post_set_photo_pet(self, auth_key: json,
                       pet_id: str,
                       pet_photo: str)-> json:

        data = MultipartEncoder(
            fields={
                    'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpg')
                    })
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}
        res = requests.post(self.base_url + 'api/pets/set_photo/'+ pet_id, headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def post_add_pet(self, auth_key: json,
                       name: str,
                       animal_type: str,
                       age: str,
                       pet_photo: str)-> json:

        data = MultipartEncoder(
            fields={'name': name,
                    'animal_type': animal_type,
                    'age': age,
                    'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpg')
                    })
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}
        res = requests.post(self.base_url + 'api/pets', headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def post_creat_pet(self, auth_key: json,
                       name: str,
                       animal_type: str,
                       age: int)  -> json:

        headers= {'auth_key': auth_key['key']}
        data = {
            "name": name,
            "animal_type": animal_type,
            "age": age,
        }
        res = requests.post(self.base_url + 'api/create_pet_simple', headers = headers, data=data)
        status = res.status_code
        result =""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

