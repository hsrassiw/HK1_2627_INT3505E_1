import unittest

from flask import json

from openapi_server.models.create_pet_input import CreatePetInput  # noqa: E501
from openapi_server.models.error import Error  # noqa: E501
from openapi_server.models.pet import Pet  # noqa: E501
from openapi_server.models.pet_page import PetPage  # noqa: E501
from openapi_server.models.pet_status import PetStatus  # noqa: E501
from openapi_server.models.update_pet_input import UpdatePetInput  # noqa: E501
from openapi_server.test import BaseTestCase


class TestPetsController(BaseTestCase):
    """PetsController integration test stubs"""

    def test_create_pets(self):
        """Test case for create_pets

        Thêm thú cưng mới
        """
        create_pet_input = {"name":"Milu","tag":"dog"}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': 'Bearer special-key',
        }
        response = self.client.open(
            '/v1/pets',
            method='POST',
            headers=headers,
            data=json.dumps(create_pet_input),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_pet(self):
        """Test case for delete_pet

        Xoá thú cưng
        """
        headers = { 
            'Accept': 'application/problem+json',
            'Authorization': 'Bearer special-key',
        }
        response = self.client.open(
            '/v1/pets/{pet_id}'.format(pet_id=1),
            method='DELETE',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_list_pets(self):
        """Test case for list_pets

        Liệt kê thú cưng
        """
        query_string = [('limit', 20),
                        ('offset', 0),
                        ('status', openapi_server.PetStatus())]
        headers = { 
            'Accept': 'application/json',
            'Authorization': 'Bearer special-key',
        }
        response = self.client.open(
            '/v1/pets',
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_show_pet_by_id(self):
        """Test case for show_pet_by_id

        Xem chi tiết thú cưng
        """
        headers = { 
            'Accept': 'application/json',
            'Authorization': 'Bearer special-key',
        }
        response = self.client.open(
            '/v1/pets/{pet_id}'.format(pet_id=1),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_update_pet(self):
        """Test case for update_pet

        Cập nhật một phần thú cưng
        """
        update_pet_input = {"name":"Milu","tag":"cat","status":"available"}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': 'Bearer special-key',
        }
        response = self.client.open(
            '/v1/pets/{pet_id}'.format(pet_id=1),
            method='PATCH',
            headers=headers,
            data=json.dumps(update_pet_input),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
