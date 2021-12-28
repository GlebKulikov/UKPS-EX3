import os
import  random as rnd
import string
import pytest
import petfriends


pf = petfriends.API()
_, key = pf.get_api_key(email, passwrod)
_, my_pets = pf.get_list_of_pets(key, "my_pets")

@pytest.mark.skip
def generate_names():
    name =[]
    for i in range(1):
        name.append(''.join(rnd.choice(string.ascii_letters) for x in range(10)))
    return name[0]

@pytest.mark.api
def test_get_api_for_valid_user(email=email, password=passwrod):
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result

@pytest.mark.api
@pytest.mark.parametrize("email, password", argvalues=[(nv_email,nv_password)])
def test_get_api_for_novalid_user(email, password):
    status, result = pf.get_api_key(email, password)
    assert status == 403

@pytest.mark.api
def test_get_all_pets_with_valid_key(filter=''):
    _,auth_key = pf.get_api_key(email, password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0

@pytest.mark.api
def test_get_all_pets_with_novalid_key(filter=''):
    auth_key = {"key": "novalidkey"}
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 403

@pytest.mark.api
@pytest.mark.parametrize("name, animal_type, age", argvalues=[(generate_names(),generate_names(), rnd.randint(0,100))])
def test_post_creat_pet_with_valid_key(name,
                                       animal_type,
                                       age):
    _, auth_key = pf.get_api_key(email, password)
    status, result = pf.post_creat_pet(auth_key, name, animal_type, age)
    assert status  == 200
    assert result['name'] == name


@pytest.mark.parametrize("name, animal_type, age", argvalues=[(generate_names(),'zzqweq', None)])
def test_post_creat_pet_with_novalid_data(name,animal_type, age):
    _, auth_key = pf.get_api_key(email, password)
    status, result = pf.post_creat_pet(auth_key, name, animal_type, age)
    assert status  == 400


@pytest.mark.parametrize("name, animal_type, age", argvalues=[('Mypka2','KoWka', 3)])
def test_post_creat_pet_with_novalid_key(name, animal_type, age):
    auth_key = {"key": "novalidkey"}
    status, result = pf.post_creat_pet(auth_key, name, animal_type, age)
    assert status  == 403

@pytest.mark.parametrize("pet_id, pet_photo", argvalues=[(id,photo)])
def test_post_set_photo_pet_with_valid_key(pet_id, pet_photo):
    _, auth_key = pf.get_api_key(email, password)
    pet_photo=os.path.join(os.path.dirname(__file__), pet_photo)
    status, result = pf.post_set_photo_pet(auth_key, pet_id, pet_photo)
    assert status  == 200
    assert result['id'] == pet_id

@pytest.mark.api
@pytest.mark.parametrize("pet_id, pet_photo", argvalues=[(id,photo)])
def test_post_set_photo_pet_with_novalid_key(pet_id, pet_photo):
    auth_key = {"key": "novalidkey"}
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    status, result = pf.post_set_photo_pet(auth_key, pet_id, pet_photo)
    assert status  == 403

@pytest.mark.parametrize("name, animal_type,age,pet_photo", argvalues=[('Vasya','Dvor', str(rnd.randint(0,100)), photo)])
def test_post_new_pet_with_valid_data(name, animal_type,
                                      age, pet_photo):
    _,auth_key = pf.get_api_key(email, passwrod)
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    status, result = pf.post_add_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name


@pytest.mark.parametrize("name, animal_type,age,pet_photo", argvalues=[('Vasya','Dvor', str(rnd.randint(0,100)), photo)])
def test_post_new_pet_with_novalid_key(name, animal_type,
                                      age, pet_photo):
    auth_key = {"key": "novalidkey"}
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    status, result = pf.post_add_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 403


@pytest.mark.parametrize("pet_id", argvalues=[(get_rnd_pet_id())])
def test_delete_pet_with_valid_key(pet_id):
    _,auth_key = pf.get_api_key(email, passwrod)
    status, _ = pf.delete_pet(auth_key, pet_id)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    assert status == 200
    assert pet_id not in my_pets.values()


@pytest.mark.foo
@pytest.mark.parametrize("pet_id", argvalues=[(get_rnd_pet_id())])
def test_delete_pet_with_novalid_key(pet_id):
    auth_key = {"key": "novalidkey"}
    status, result = pf.delete_pet(auth_key, pet_id)
    assert status == 403

@pytest.mark.api
def test_put_pet_with_valid_key(pet_id=0,name='Котяра', animal_type='Кот',
                                  age = rnd.randint(0,100)):
   _,auth_key = pf.get_api_key(email, password)
   _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
   sum_pets = len(my_pets['pets'])
   pet_id =rnd.choice(my_pets['pets'])
   if sum_pets == 0:
       raise Exception("Bаш список питомцев пуст")
   else:
       status, result = pf.put_pet(auth_key, pet_id['id'], name, animal_type, age)
       assert status == 200
       assert result['name'] == name


@pytest.mark.api
def test_put_pet_with_novalid_data(pet_id='zz',name='asdasdqwe', animal_type='wqe12cxzc',
                                  age = rnd.randint(0,100)):
   _,auth_key = pf.get_api_key(email, password)
   status, result = pf.put_pet(auth_key,pet_id, name, animal_type, age)
   assert status == 400


@pytest.fixture()
def get_pet_id():
    pet_id = rnd.choice(my_pets['pets'])
    return pet_id['id']

@pytest.mark.foo
def test_put_pet_with_novalid_key(get_pet_id,name='eqweqweqw', animal_type='231asdxzc',
                                  age = rnd.randint(0,100)):
   auth_key = {"key": "novalidkey"}
   status, result = pf.put_pet(auth_key,get_pet_id, name, animal_type, age)
   assert status == 403
