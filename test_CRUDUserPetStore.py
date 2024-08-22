#Лекция 3.4. ALLURE
import pytest
import requests
import jsonschema
from jsonschema import validate

@pytest.mark.regression
def test_user_operations(base_url, user_id):
    # Update user

    update_data = {
        "id": user_id,
        "username": "test_api_331",
        "firstName": "test",
        "lastName": "testoviv",
        "email": "GIGIG@email.com",
        "password": "1q2w3e4r",
        "phone": "+44444444",
        "userStatus": 0
    }

    update_user = requests.put(f'{base_url}/user/test_api_331', json=update_data)

    print('\nUpdate user response ' + update_user.text)
    assert update_user.status_code == 200

    print(update_user.headers)
    assert update_user.headers['Content-Type'] == 'application/json'

    # Get user

    get_user = requests.get(f'{base_url}/user/test_api_331')

    print('\nGet user info' + get_user.text)
    assert get_user.status_code == 200
    print(get_user.headers)
    assert get_user.headers['Content-Type'] == 'application/json'

    # !!! Ниже часть про перевод json в python и проверку данных на апдейт

    user_info = get_user.json()
    assert user_info['username'] == update_data['username']
    assert user_info['email'] == update_data['email']
    assert user_info['phone'] == update_data['phone']

    schema = {
        "type": "object",
        "properties": {
            "id": {"type": "integer"},
            "username": {"type": "string"},  #тут делаем ошибку меняя стрингу на интегер
            "firstName": {"type": "string"},
            "lastName": {"type": "string"},
            "email": {"type": "string", "format": "email"},
            "password": {"type": "string"},
            "phone": {"type": "string"},
            "userStatus": {"type": "integer"}
        },
        "required": ["id", "username", "firstName", "lastName", "email", "password", "phone", "userStatus"],
        "additionalProperties": False
    }
    try:
        validate(instance=user_info, schema=schema)
        print('JSON schema validation success')

    except jsonschema.exceptions.ValidationError as e:
        print('Error validation JSON schema')
        print(e)
        raise e


@pytest.mark.skip
def test_2():
    print('Second Test')


a = 333


@pytest.mark.skipif(a != 234, reason="is`n equal 234, skip test")
def test_a():
    assert a == 234


@pytest.mark.xfail(reason="Expected fail test")
def test_a2():
    assert a == 234


@pytest.mark.parametrize("test_data", [123, 234, 345])
def test_a3(test_data):
    assert test_data == 234



#Домашка с @pytest.mark.parametrize
# import pytest
# import requests
# from randimage import get_random_image
# from PIL import Image
# import tempfile
# import numpy as np
# import jsonschema
# from jsonschema import validate
#
# @pytest.fixture(scope="module", autouse=True)
# def base_url():
#     base_url = "https://petstore.swagger.io/v2"
#     return base_url
#
# @pytest.fixture(scope="module", autouse=True) #мб не сессионно???
# def pet_id():
#     pet_id = 123454321
#     return pet_id
#
# @pytest.fixture(scope="module", autouse=True) #мб не сессионно???
# def data(pet_id):
#     data = {
#         "id": pet_id,
#         "category": {
#             "id": 0,
#             "name": "string"
#         },
#         "name": "Peeesik",
#         "photoUrls": [
#             "string"
#         ],
#         "tags": [
#             {
#                 "id": 0,
#                 "name": "string"
#             }
#         ],
#         "status": "available"
#     }
#     return data
# @pytest.fixture(scope="module", autouse=True)
# def update_pet_data(pet_id):
#     update_pet_data = {
#         "id": pet_id,
#         "category": {
#             "id": 0,
#             "name": "string"
#         },
#         "name": "Peeesik",
#         "photoUrls": [
#             "string"
#         ],
#         "tags": [
#             {
#                 "id": 0,
#                 "name": "string"
#             }
#         ],
#         "status": "booked"
#     }
#     return update_pet_data
#
#
# def test_creation_of_pet(base_url, pet_id, data): #или вывести в setup?
#
#     create_pet = requests.post(f'{base_url}/pet', json=data) #нужна ли эта строка? с учётом скоблок в функции
#
#     print('\nTest of create pet')
#     print('Text: ' + create_pet.text)
#     print('Status: ' + str(create_pet.status_code))
#     assert create_pet.status_code == 200
#
# #print("1. Tests of uploading images")
# @pytest.mark.parametrize("img_format", ['PNG', 'JPEG'])
# def test_upload_pet_image_format(base_url, pet_id, img_format):
#
#     img_size = (128, 128)
#     img = get_random_image(img_size)
#     img = (img * 255).astype(np.uint8)
#
#     additional_metadata = 'Random image upload'
#
#     # Save image to temporary file
#     with tempfile.NamedTemporaryFile(suffix=f'.{img_format}', delete=False) as temp_image_file:
#         image_path = temp_image_file.name
#         image = Image.fromarray(img)
#         image.save(image_path, format=img_format.upper())
#
#     # Upload the image
#     with open(image_path, 'rb') as file:
#         upload_image_pet = requests.post(
#             f'{base_url}/pet/{pet_id}/uploadImage',
#             data={'additionalMetadata': additional_metadata},
#             files={'file': file}
#         )
#
#     print('\n1.1. Upload pet image: checking format of images')
#     print('Text: ' + upload_image_pet.text)
#     print('Status: ' + str(upload_image_pet.status_code))
#     assert upload_image_pet.status_code == 200
#
# @pytest.mark.parametrize("additional_metadata", ['Random image upload', '112324', ''])
# def test_upload_image_metadata(base_url, pet_id, additional_metadata):
#
#     img_size = (128, 128)
#     img = get_random_image(img_size)
#     img = (img * 255).astype(np.uint8)
#
#     with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_image_file:
#         image_path = temp_image_file.name
#         image = Image.fromarray(img)
#         image.save(image_path)
#
#     with open(image_path, 'rb') as file:
#         upload_image_pet = requests.post(
#             f'{base_url}/pet/{pet_id}/uploadImage',
#             data={'additionalMetadata': additional_metadata},
#             files={'file': file}
#         )
#
#     print('\nUpload pet image: checking additional data')
#     print('Text: ' + upload_image_pet.text)
#     print('Status: ' + str(upload_image_pet.status_code))
#     assert upload_image_pet.status_code == 200
#
#
# @pytest.mark.parametrize("img_size, expected_status", [
#     ((256, 512), 200),
#     ((512, 1024), 200),
#     ((1024, 1024), 200),
#     ((1, 1), 200), #мб убрать нахрен
#     ((0, 0), 400)
# ])
# def test_upload_pet_image_sizes_statuses(base_url, pet_id, img_size, expected_status):
#
#     def upload_image(file, metadata):
#         return requests.post(
#             f'{base_url}/pet/{pet_id}/uploadImage',
#             data={'additionalMetadata': metadata},
#             files={'file': file}
#         )
#
#     if img_size == (0, 0):
#         response = upload_image(('empty.png', b'', 'image/png'), 'Testing with (0, 0) image')
#         print('\nAttempted upload with image size (0, 0)')
#     else:
#         img = get_random_image(img_size)
#         img = (img * 255).astype(np.uint8)
#         additional_metadata = 'Random image upload'
#
#         with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_image_file:
#             image_path = temp_image_file.name
#             Image.fromarray(img).save(image_path)
#
#         with open(image_path, 'rb') as file:
#             response = upload_image(file, additional_metadata)
#
#         print(f'\nUpload pet image with size {img_size}')
#
#     print('\nUpload pet image: image size VS status code')
#     print('Text: ' + response.text)
#     print('Status: ' + str(response.status_code))
#     assert response.status_code == expected_status
#
#
# def test_update_pet_data(base_url, update_pet_data):
#
#     update_pet = requests.put(f'{base_url}/pet', json=update_pet_data)
#
#     print('\nUpdate pet data')
#     print('Text: ' + update_pet.text)
#     print('Status: ' + str(update_pet.status_code))
#     assert update_pet.status_code == 200
#     print('Headers: ' + str(update_pet.headers))
#     assert update_pet.headers['Content-Type'] == 'application/json'
#
#     # Find by pet_id
# def test_find_by_pet_id(base_url, pet_id, update_pet_data):
#     find_pet = requests.get(f'{base_url}/pet/{pet_id}')
#
#     print('\nFind pet by pet ID')
#     print('Text: ' + find_pet.text)
#     print('Status: ' + str(find_pet.status_code))
#     assert find_pet.status_code == 200
#     print('Headers: ' + str(find_pet.headers))
#     assert find_pet.headers['Content-Type'] == 'application/json'
#
#     pet_info = find_pet.json()
#     assert pet_info['status'] == update_pet_data['status']
#     assert pet_info['id'] == update_pet_data['id']
#
#     schema = {
#         "type": "object",
#         "properties": {
#             "id": {"type": "integer"},
#             "category": {
#                 "type": "object",
#                 "properties": {
#                     "id": {"type": "integer"},
#                     "name": {"type": "string"}
#                 },
#                 "required": ["id", "name"]
#             },
#             "name": {"type": "string"},
#             "photoUrls": {
#                 "type": "array",
#                 "items": {"type": "string"}
#             },
#             "tags": {
#                 "type": "array",
#                 "items": {
#                     "type": "object",
#                     "properties": {
#                         "id": {"type": "integer"},
#                         "name": {"type": "string"}
#                     },
#                     "required": ["id", "name"]
#                 }
#             },
#             "status": {"type": "string"}
#         },
#         "required": ["id", "category", "name", "photoUrls", "tags", "status"]
#     }
#
#     try:
#         validate(instance=pet_info, schema=schema)
#         print('JSON schema validation success')
#
#     except jsonschema.exceptions.ValidationError as e:
#         print('Error validation JSON schema')
#         print(e)
#         raise e
#
# def test_delete_pet(base_url, pet_id): #мб убрать в teardown?
#     delete_pet = requests.delete(f'{base_url}/pet/{pet_id}')
#
#     print('\nDelete pet')
#     print('Text:' + delete_pet.text)
#     print('Status: ' + str(delete_pet.status_code))
#     assert delete_pet.status_code == 200

#Лекция 3.3. Маркировка Mark
# import pytest
# import requests
# import jsonschema
# from jsonschema import validate
#
#
# @pytest.mark.regression
# def test_user_operations(base_url, user_id):
#     # Update user
#
#     update_data = {
#         "id": user_id,
#         "username": "test_api_331",
#         "firstName": "test",
#         "lastName": "testoviv",
#         "email": "GIGIG@email.com",
#         "password": "1q2w3e4r",
#         "phone": "+44444444",
#         "userStatus": 0
#     }
#
#     update_user = requests.put(f'{base_url}/user/test_api_331', json=update_data)
#
#     print('\nUpdate user response ' + update_user.text)
#     assert update_user.status_code == 200
#
#     print(update_user.headers)
#     assert update_user.headers['Content-Type'] == 'application/json'
#
#     # Get user
#
#     get_user = requests.get(f'{base_url}/user/test_api_331')
#
#     print('\nGet user info' + get_user.text)
#     assert get_user.status_code == 200
#     print(get_user.headers)
#     assert get_user.headers['Content-Type'] == 'application/json'
#
#     # !!! Ниже часть про перевод json в python и проверку данных на апдейт
#
#     user_info = get_user.json()
#     assert user_info['username'] == update_data['username']
#     assert user_info['email'] == update_data['email']
#     assert user_info['phone'] == update_data['phone']
#
#     schema = {
#         "type": "object",
#         "properties": {
#             "id": {"type": "integer"},
#             "username": {"type": "string"},  #тут делаем ошибку меняя стрингу на интегер
#             "firstName": {"type": "string"},
#             "lastName": {"type": "string"},
#             "email": {"type": "string", "format": "email"},
#             "password": {"type": "string"},
#             "phone": {"type": "string"},
#             "userStatus": {"type": "integer"}
#         },
#         "required": ["id", "username", "firstName", "lastName", "email", "password", "phone", "userStatus"],
#         "additionalProperties": False
#     }
#     try:
#         validate(instance=user_info, schema=schema)
#         print('JSON schema validation success')
#
#     except jsonschema.exceptions.ValidationError as e:
#         print('Error validation JSON schema')
#         print(e)
#         raise e
#
#
# @pytest.mark.skip
# def test_2():
#     print('Second Test')
#
#
# a = 333
#
#
# @pytest.mark.skipif(a != 234, reason="is`n equal 234, skip test")
# def test_a():
#     assert a == 234
#
#
# @pytest.mark.xfail(reason="Expected fail test")
# def test_a2():
#     assert a == 234
#
#
# @pytest.mark.parametrize("test_data", [123, 234, 345])
# def test_a3(test_data):
#     assert test_data == 234

#Лекция 3.2. использование CONFTEST

# import pytest
# import requests
# import jsonschema
# from jsonschema import validate
#
# def test_user_operations(base_url, user_id):
#
#     # Update user
#
#     update_data = {
#         "id": user_id,
#         "username": "test_api_331",
#         "firstName": "test",
#         "lastName": "testoviv",
#         "email": "GIGIG@email.com",
#         "password": "1q2w3e4r",
#         "phone": "+44444444",
#         "userStatus": 0
#     }
#
#     update_user = requests.put(f'{base_url}/user/test_api_331', json=update_data)
#
#     print('\nUpdate user response ' + update_user.text)
#     assert update_user.status_code == 200
#
#     print(update_user.headers)
#     assert update_user.headers['Content-Type'] == 'application/json'
#
#     # Get user
#
#     get_user = requests.get(f'{base_url}/user/test_api_331')
#
#     print('\nGet user info' + get_user.text)
#     assert get_user.status_code == 200
#     print(get_user.headers)
#     assert get_user.headers['Content-Type'] == 'application/json'
#
#     # !!! Ниже часть про перевод json в python и проверку данных на апдейт
#
#     user_info = get_user.json()
#     assert user_info['username'] == update_data['username']
#     assert user_info['email'] == update_data['email']
#     assert user_info['phone'] == update_data['phone']
#
#     schema = {
#         "type": "object",
#         "properties": {
#             "id": {"type": "integer"},
#             "username": {"type": "string"},  #тут делаем ошибку меняя стрингу на интегер
#             "firstName": {"type": "string"},
#             "lastName": {"type": "string"},
#             "email": {"type": "string", "format": "email"},
#             "password": {"type": "string"},
#             "phone": {"type": "string"},
#             "userStatus": {"type": "integer"}
#         },
#         "required": ["id", "username", "firstName", "lastName", "email", "password", "phone", "userStatus"],
#         "additionalProperties": False
#     }
#     try:
#         validate(instance=user_info, schema=schema)
#         print('JSON schema validation success')
#
#     except jsonschema.exceptions.ValidationError as e:
#         print('Error validation JSON schema')
#         print(e)
#         raise e
# def test_2():
#     print('Second Test')

# Лекция 3.1 использование @pytest.fixture без Conftest

#
# import pytest
# import requests
# import jsonschema
# from jsonschema import validate
#
# @pytest.fixture(scope="module")
# def base_url():
#     base_url = "https://petstore.swagger.io/v2"
#     return  base_url
#
# @pytest.fixture(scope="module")
# def user_id():
#     user_id = 1234321
#     return user_id
#
#
# #Setup
#
# @pytest.fixture(scope="module", autouse=True)
#
# def setup(base_url, user_id):
#
#     data = {
#         "id": user_id,
#         "username": "test_api_331",
#         "firstName": "test",
#         "lastName": "testoviv",
#         "email": "qwe@email.com",
#         "password": "1q2w3e4r",
#         "phone": "+898765434",
#         "userStatus": 0
#     }
#
#     create_user = requests.post(f'{base_url}/user', json=data)
#
#     print('Create User Response ' + create_user.text)
#     assert create_user.status_code == 200
#     print(create_user.headers)
#     assert create_user.headers['Content-Type'] == 'application/json'
#
#     yield
#     #Delete user
#
#     delete_user = requests.delete(f'{base_url}/user/test_api_331')
#     print('\nDelete User Response' + delete_user.text)
#     assert delete_user.status_code == 200
#     print(delete_user.headers)
#     assert delete_user.headers['Content-Type'] == 'application/json'
#
#
# def test_user_operations(base_url, user_id):
#
#     # Update user
#
#     update_data = {
#         "id": user_id,
#         "username": "test_api_331",
#         "firstName": "test",
#         "lastName": "testoviv",
#         "email": "GIGIG@email.com",
#         "password": "1q2w3e4r",
#         "phone": "+44444444",
#         "userStatus": 0
#     }
#
#     update_user = requests.put(f'{base_url}/user/test_api_331', json=update_data)
#
#     print('\nUpdate user response ' + update_user.text)
#     assert update_user.status_code == 200
#
#     print(update_user.headers)
#     assert update_user.headers['Content-Type'] == 'application/json'
#
#     # Get user
#
#     get_user = requests.get(f'{base_url}/user/test_api_331')
#
#     print('\nGet user info' + get_user.text)
#     assert get_user.status_code == 200
#     print(get_user.headers)
#     assert get_user.headers['Content-Type'] == 'application/json'
#
#     # !!! Ниже часть про перевод json в python и проверку данных на апдейт
#
#     user_info = get_user.json()
#     assert user_info['username'] == update_data['username']
#     assert user_info['email'] == update_data['email']
#     assert user_info['phone'] == update_data['phone']
#
#     schema = {
#         "type": "object",
#         "properties": {
#             "id": {"type": "integer"},
#             "username": {"type": "string"},  #тут делаем ошибку меняя стрингу на интегер
#             "firstName": {"type": "string"},
#             "lastName": {"type": "string"},
#             "email": {"type": "string", "format": "email"},
#             "password": {"type": "string"},
#             "phone": {"type": "string"},
#             "userStatus": {"type": "integer"}
#         },
#         "required": ["id", "username", "firstName", "lastName", "email", "password", "phone", "userStatus"],
#         "additionalProperties": False
#     }
#     try:
#         validate(instance=user_info, schema=schema)
#         print('JSON schema validation success')
#
#     except jsonschema.exceptions.ValidationError as e:
#         print('Error validation JSON schema')
#         print(e)
#         raise e
# def test_2():
#     print('Second Test')


# Лекция 3 Setup & Teardown

# import pytest
# import requests
# import jsonschema
# from jsonschema import validate
#
# base_url = "https://petstore.swagger.io/v2"
# user_id = 1234321
#
# #Setup
#
# def setup_module():
#     data = {
#         "id": user_id,
#         "username": "test_api_331",
#         "firstName": "test",
#         "lastName": "testoviv",
#         "email": "qwe@email.com",
#         "password": "1q2w3e4r",
#         "phone": "+898765434",
#         "userStatus": 0
#     }
#
#     create_user = requests.post(f'{base_url}/user', json=data)
#
#     print('Create user response ' + create_user.text)
#     assert create_user.status_code == 200
#     print(create_user.headers)
#     assert create_user.headers['Content-Type'] == 'application/json'
#
# #Teardown
#
# def teardown_module():
#     delete_user = requests.delete(f'{base_url}/user/test_api_331')
#     print('\nDelete user request' + delete_user.text)
#     assert delete_user.status_code == 200
#     print(delete_user.headers)
#     assert delete_user.headers['Content-Type'] == 'application/json'
#
#
# def test_user_operations():
#
#     # Update user
#
#     update_data = {
#         "id": user_id,
#         "username": "test_api_331",
#         "firstName": "test",
#         "lastName": "testoviv",
#         "email": "GIGIG@email.com",
#         "password": "1q2w3e4r",
#         "phone": "+44444444",
#         "userStatus": 0
#     }
#
#     update_user = requests.put(f'{base_url}/user/test_api_331', json=update_data)
#
#     print('\nUpdate user response ' + update_user.text)
#     assert update_user.status_code == 200
#
#     print(update_user.headers)
#     assert update_user.headers['Content-Type'] == 'application/json'
#
#     # Get user
#
#     get_user = requests.get(f'{base_url}/user/test_api_331')
#
#     print('\nGet user info' + get_user.text)
#     assert get_user.status_code == 200
#     print(get_user.headers)
#     assert get_user.headers['Content-Type'] == 'application/json'
#
#     # !!! Ниже часть про перевод json в python и проверку данных на апдейт
#
#     user_info = get_user.json()
#     assert user_info['username'] == update_data['username']
#     assert user_info['email'] == update_data['email']
#     assert user_info['phone'] == update_data['phone']
#
#     schema = {
#         "type": "object",
#         "properties": {
#             "id": {"type": "integer"},
#             "username": {"type": "string"},  #тут делаем ошибку меняя стрингу на интегер
#             "firstName": {"type": "string"},
#             "lastName": {"type": "string"},
#             "email": {"type": "string", "format": "email"},
#             "password": {"type": "string"},
#             "phone": {"type": "string"},
#             "userStatus": {"type": "integer"}
#         },
#         "required": ["id", "username", "firstName", "lastName", "email", "password", "phone", "userStatus"],
#         "additionalProperties": False
#     }
#     try:
#         validate(instance=user_info, schema=schema)
#         print('JSON schema validation success')
#
#     except jsonschema.exceptions.ValidationError as e:
#         print('Error validation JSON schema')
#         print(e)
#         raise e
# def test_2():
#     print('Second Test')
#


#Домашка 2 с валидацией ответов по JSON schema
# import requests
# from randimage import get_random_image
# from PIL import Image
# import tempfile
# import numpy as np
# import jsonschema
# from jsonschema import validate
#
#
#
# def test_operations_with_pets():
#     # Creation of pet
#     img_size = (128, 128)
#     img = get_random_image(img_size)
#
#     img = (img * 255).astype(np.uint8)
#
#     base_url = "https://petstore.swagger.io/v2"
#
#     pet_id = 123454321
#
#     pet_name = 'Peeesik'
#
#     data = {
#         "id": pet_id,
#         "category": {
#             "id": 0,
#             "name": "string"
#         },
#         "name": pet_name,
#         "photoUrls": [
#             "string"
#         ],
#         "tags": [
#             {
#                 "id": 0,
#                 "name": "string"
#             }
#         ],
#         "status": "available"
#
#     }
#
#     create_pet = requests.post(f'{base_url}/pet', json=data)
#
#     print('\nCreate pet')
#     print('Text: '+ create_pet.text)
#     print('Status: ' + str(create_pet.status_code))
#     assert create_pet.status_code == 200
#
#     # Upload pet image
#
#     additional_metadata = 'Random image upload'
#
#     # Save image to temporary file
#     with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_image_file:
#         image_path = temp_image_file.name
#         image = Image.fromarray(img)
#         image.save(image_path)
#
#     # Upload the image
#     with open(image_path, 'rb') as file:
#         upload_image_pet = requests.post(
#             f'{base_url}/pet/{pet_id}/uploadImage',
#             data={'additionalMetadata': additional_metadata},
#             files={'file': file}
#         )
#
#     print('\nUpload pet image')
#     print('Text: ' + upload_image_pet.text)
#     print('Status: ' + str(upload_image_pet.status_code))
#     assert upload_image_pet.status_code == 200
#
#     # Upd pet status
#
#     update_pet_data = {
#         "id": pet_id,
#         "category": {
#             "id": 0,
#             "name": "string"
#         },
#         "name": pet_name,
#         "photoUrls": [
#             "string"
#         ],
#         "tags": [
#             {
#                 "id": 0,
#                 "name": "string"
#             }
#         ],
#         "status": "booked"
#     }
#
#     update_pet = requests.put(f'{base_url}/pet', json=update_pet_data)
#
#     print('\nUpdate pet')
#     print('Text: ' + update_pet.text)
#     print('Status: ' + str(update_pet.status_code))
#     assert update_pet.status_code == 200
#     print('Headers: ' + str(update_pet.headers))
#     assert update_pet.headers['Content-Type'] == 'application/json'
#
#
#     # Find by pet_id
#
#     find_pet = requests.get(f'{base_url}/pet/{pet_id}')
#
#     print('\nFind pet by pet ID')
#     print('Text: ' + find_pet.text)
#     print('Status: ' + str(find_pet.status_code))
#     assert find_pet.status_code == 200
#     print('Headers: ' + str(find_pet.headers))
#     assert find_pet.headers['Content-Type'] == 'application/json'
#
#     pet_info = find_pet.json()
#     assert pet_info['status'] == update_pet_data['status']
#     assert pet_info['id'] == update_pet_data['id']
#
#     schema = {
#         "type": "object",
#         "properties": {
#             "id": {"type": "integer"},
#             "category": {
#                 "type": "object",
#                 "properties": {
#                     "id": {"type": "integer"},
#                     "name": {"type": "string"}
#                 },
#                 "required": ["id", "name"]
#             },
#             "name": {"type": "string"},
#             "photoUrls": {
#                 "type": "array",
#                 "items": {"type": "string"}
#             },
#             "tags": {
#                 "type": "array",
#                 "items": {
#                     "type": "object",
#                     "properties": {
#                         "id": {"type": "integer"},
#                         "name": {"type": "string"}
#                     },
#                     "required": ["id", "name"]
#                 }
#             },
#             "status": {"type": "string"}
#         },
#         "required": ["id", "category", "name", "photoUrls", "tags", "status"]
#     }
#
#     try:
#         validate(instance=pet_info, schema=schema)
#         print('JSON schema validation success')
#
#     except jsonschema.exceptions.ValidationError as e:
#         print('Error validation JSON schema')
#         print(e)
#         raise e
#
#     #Delete pet
#
#     delete_pet = requests.delete(f'{base_url}/pet/{pet_id}')
#
#     print('\nDelete pet')
#     print('Text:' + delete_pet.text)
#     print('Status: ' + str(delete_pet.status_code))
#     assert delete_pet.status_code == 200


# Лекция 2
# import requests
# import jsonschema
# from jsonschema import validate
#
# base_url = "https://petstore.swagger.io/v2"
# user_id = 1234321
#
#
# def test_user_operations():
#     # Create user
#
#     data = {
#         "id": user_id,
#         "username": "test_api_331",
#         "firstName": "test",
#         "lastName": "testoviv",
#         "email": "qwe@email.com",
#         "password": "1q2w3e4r",
#         "phone": "+898765434",
#         "userStatus": 0
#     }
#
#     create_user = requests.post(f'{base_url}/user', json=data)
#
#     print('Create user response ' + create_user.text)
#     assert create_user.status_code == 200
#     print(create_user.headers)
#     assert create_user.headers['Content-Type'] == 'application/json'
#
#     # Update user
#
#     update_data = {
#         "id": user_id,
#         "username": "test_api_331",
#         "firstName": "test",
#         "lastName": "testoviv",
#         "email": "GIGIG@email.com",
#         "password": "1q2w3e4r",
#         "phone": "+44444444",
#         "userStatus": 0
#     }
#
#     update_user = requests.put(f'{base_url}/user/test_api_331', json=update_data)
#
#     print('\nUpdate user response ' + update_user.text)
#     assert update_user.status_code == 200
#
#     print(update_user.headers)
#     assert update_user.headers['Content-Type'] == 'application/json'
#
#     # Get user
#
#     get_user = requests.get(f'{base_url}/user/test_api_331')
#
#     print('\nGet user info' + get_user.text)
#     assert get_user.status_code == 200
#     print(get_user.headers)
#     assert get_user.headers['Content-Type'] == 'application/json'
#
#     # !!! Ниже часть про перевод json в python и проверку данных на апдейт
#
#     user_info = get_user.json()
#     assert user_info['username'] == update_data['username']
#     assert user_info['email'] == update_data['email']
#     assert user_info['phone'] == update_data['phone']
#
#     schema = {
#         "type": "object",
#         "properties": {
#             "id": {"type": "integer"},
#             "username": {"type": "string"},  #тут делаем ошибку меняя стрингу на интегер
#             "firstName": {"type": "string"},
#             "lastName": {"type": "string"},
#             "email": {"type": "string", "format": "email"},
#             "password": {"type": "string"},
#             "phone": {"type": "string"},
#             "userStatus": {"type": "integer"}
#         },
#         "required": ["id", "username", "firstName", "lastName", "email", "password", "phone", "userStatus"],
#         "additionalProperties": False
#     }
#     try:
#         validate(instance=user_info, schema=schema)
#         print('JSON schema validation success')
#
#     except jsonschema.exceptions.ValidationError as e:
#         print('Error validation JSON schema')
#         print(e)
#         raise e
#
#     # Delete user
#
#     delete_user = requests.delete(f'{base_url}/user/test_api_331')
#     print('\nDelete user request' + delete_user.text)
#     assert delete_user.status_code == 200
#     print(delete_user.headers)
#     assert delete_user.headers['Content-Type'] == 'application/json'

# Домашка
# import requests
# from randimage import get_random_image
# from PIL import Image
# import tempfile
# import numpy as np
#
#
# def test_operations_with_pets():
#     # Creation of pet
#     img_size = (128, 128)
#     img = get_random_image(img_size)
#
#     img = (img * 255).astype(np.uint8)
#
#     base_url = "https://petstore.swagger.io/v2"
#
#     pet_id = 123454321
#
#     pet_name = 'Peeesik'
#
#     data = {
#         "id": pet_id,
#         "category": {
#             "id": 0,
#             "name": "string"
#         },
#         "name": pet_name,
#         "photoUrls": [
#             "string"
#         ],
#         "tags": [
#             {
#                 "id": 0,
#                 "name": "string"
#             }
#         ],
#         "status": "available"
#     }
#
#     create_pet = requests.post(f'{base_url}/pet', json=data)
#
#     print(create_pet.text)
#     print(create_pet.status_code)
#     assert create_pet.status_code == 200
#
#     # Upload pet image
#
#     additional_metadata = 'Random image upload'
#
#     # Save image to temporary file
#     with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_image_file:
#         image_path = temp_image_file.name
#         image = Image.fromarray(img)
#         image.save(image_path)
#
#     # Upload the image
#     with open(image_path, 'rb') as file:
#         upload_image_pet = requests.post(
#             f'{base_url}/pet/{pet_id}/uploadImage',
#             data={'additionalMetadata': additional_metadata},
#             files={'file': file}
#         )
#
#     print(upload_image_pet.text)
#     print(upload_image_pet.status_code)
#     assert upload_image_pet.status_code == 200
#
#     # Upd pet status
#
#     update_pet_data = {
#         "id": pet_id,
#         "category": {
#             "id": 0,
#             "name": "string"
#         },
#         "name": pet_name,
#         "photoUrls": [
#             "string"
#         ],
#         "tags": [
#             {
#                 "id": 0,
#                 "name": "string"
#             }
#         ],
#         "status": "booked"
#     }
#
#     update_pet = requests.put(f'{base_url}/pet', json=update_pet_data)
#
#     print(update_pet.text)
#     print(update_pet.status_code)
#     assert update_pet.status_code == 200
#     print(update_pet.headers)
#     assert update_pet.headers['Content-Type'] == 'application/json'
#
#
#     # Find by pet_id
#
#     find_pet = requests.get(f'{base_url}/pet/{pet_id}')
#
#     print(find_pet.text)
#     print(find_pet.status_code)
#     print(find_pet.headers)
#     assert find_pet.status_code == 200
#     assert find_pet.headers['Content-Type'] == 'application/json'
#
#     # Delete pet
#
#     delete_pet = requests.delete(f'{base_url}/pet/{pet_id}')
#
#     print(delete_pet.text)
#     print(delete_pet.status_code)
#     assert delete_pet.status_code == 200

# Лекция 1
#
# import requests
#
# base_url = "https://petstore.swagger.io/v2"
#
# user_id = 1234321
#
# def test_user_operations():
#     #Create user
#
#     data = {
#         "id": user_id,
#         "username": "test_api_23",
#         "firstName": "test",
#         "lastName": "testoviv",
#         "email": "qwe@email.com",
#         "password": "1q2w3e4r",
#         "phone": "+898765434",
#         "userStatus": 0
#     }
#
#     create_user = requests.post(f'{base_url}/user', json=data)
#
#     print('Create user response ' + create_user.text)
#     assert create_user.status_code == 200
#     print(create_user.headers)
#     assert create_user.headers['Content-Type'] == 'application/json'
#
#     # Update user
#
#     update_data = {
#         "id": user_id,
#         "username": "test_api_23",
#         "firstName": "test",
#         "lastName": "testoviv",
#         "email": "GIGIG@email.com",
#         "password": "1q2w3e4r",
#         "phone": "+44444444",
#         "userStatus": 0
#     }
#
#     update_user = requests.put(f'{base_url}/user/test_api_23', json=update_data)
#
#     print('\nUpdate user response ' + update_user.text)
#     assert update_user.status_code == 200
#
#     print(update_user.headers)
#     assert update_user.headers['Content-Type'] == 'application/json'
#
#     # Get user
#
#     get_user = requests.get(f'{base_url}/user/test_api_23')
#
#     print('\nGet user info' + get_user.text)
#     assert get_user.status_code == 200
#     print(get_user.headers)
#     assert get_user.headers['Content-Type'] == 'application/json'
#     user_info = get_user.json()
#     assert user_info['username'] == update_data['username']
#     assert user_info['email'] == update_data['email']
#     assert user_info['phone'] == update_data['phone']
#
#
#     # Delete user
#
#     delete_user = requests.delete(f'{base_url}/user/test_api_23')
#
#     print('\nDelete user request' + delete_user.text)
#     assert delete_user.status_code == 200
#     print(delete_user.headers)
#     assert delete_user.headers['Content-Type'] == 'application/json'
#
#
#
#
#
#
#
#
