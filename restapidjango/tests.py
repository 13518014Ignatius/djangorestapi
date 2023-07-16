# Import Django configurations from settings.py
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

# Import Django
import django
django.setup()

# Other Imports
from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient
from restapidjango.endpoints import authenticate_with_token

# LoginTestCase class
# Purpose: Test the login_request function and all its possible responses
class LoginTestCase(TestCase):
    # Initial setup for every test in LoginTestCase
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", password="testpass")

    # Test #1: login_request success, is logged in, and the token works as intended
    # status code: 200 OK    
    def test_login_success(self):
        response = self.client.post("/login/", {"username": "testuser", "password": "testpass"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("token", response.data)
        token = response.data['token']
        self.assertTrue(authenticate_with_token(token))

    # Test #2: login_request failure due to wrong credentials
    # status code: 400 BAD REQUEST   
    def test_login_wrong_credentials(self):
        response = self.client.post("/login/", {"username": "wronguser", "password": "wrongpass"})
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.data)

# RegisterTestCase class
# Purpose: Test the register_request function and all its possible responses
class RegisterTestCase(TestCase):
    # Initial setup for every test in RegisterTestCase
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="exampleuser", password="examplepass", email="example@example.com")

    # Test #3: register_request success
    # status code: 201 CREATED  
    def test_register_success(self):
        response = self.client.post("/register/", {"username": "testuser", "password": "testpass", "email": "test@example.com"})
        self.assertEqual(response.status_code, 201)
        self.assertIn("success", response.data)

    # Test #4: register_request failure due to missing fields
    # status code: 400 BAD REQUEST
    # error message: Missing fields
    def test_register_missing_fields(self):
        response = self.client.post("/register/", {"username": "", "password": "", "email": ""})
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.data)
        self.assertEqual(response.data["error"], "Missing fields")
        response2 = self.client.post("/register/", {"username": "testuser", "password": "", "email": ""})
        self.assertEqual(response2.status_code, 400)
        self.assertIn("error", response2.data)
        self.assertEqual(response2.data["error"], "Missing fields")
        response3 = self.client.post("/register/", {"username": "", "password": "testpass", "email": ""})
        self.assertEqual(response3.status_code, 400)
        self.assertIn("error", response3.data)
        self.assertEqual(response3.data["error"], "Missing fields")
        response4 = self.client.post("/register/", {"username": "", "password": "", "email": "test@example.com"})
        self.assertEqual(response4.status_code, 400)
        self.assertIn("error", response4.data)
        self.assertEqual(response4.data["error"], "Missing fields")
        response5 = self.client.post("/register/", {"username": "testuser", "password": "testpass", "email": ""})
        self.assertEqual(response5.status_code, 400)
        self.assertIn("error", response5.data)
        self.assertEqual(response5.data["error"], "Missing fields")
        response6 = self.client.post("/register/", {"username": "", "password": "testpass", "email": "test@example.com"})
        self.assertEqual(response6.status_code, 400)
        self.assertIn("error", response6.data)
        self.assertEqual(response6.data["error"], "Missing fields")
        response7 = self.client.post("/register/", {"username": "testuser", "password": "", "email": "test@example.com"})
        self.assertEqual(response7.status_code, 400)
        self.assertIn("error", response7.data)
        self.assertEqual(response7.data["error"], "Missing fields")

    # Test #5: register_request failure due to user already existing
    # status code: 400 BAD REQUEST
    # error message: User already exists
    def test_register_user_already_exists(self):
        response = self.client.post("/register/", {"username": "exampleuser", "password": "examplepass", "email": "test@example.com"})
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.data)
        self.assertEqual(response.data["error"], "User already exists")
        response2 = self.client.post("/register/", {"username": "testuser", "password": "examplepass", "email": "example@example.com"})
        self.assertEqual(response2.status_code, 400)
        self.assertIn("error", response2.data)
        self.assertEqual(response2.data["error"], "User already exists")
        response3 = self.client.post("/register/", {"username": "exampleuser", "password": "examplepass", "email": "example@example.com"})
        self.assertEqual(response3.status_code, 400)
        self.assertIn("error", response3.data)
        self.assertEqual(response3.data["error"], "User already exists")

# ListUsersTestCase class
# Purpose: Test the list_users_request function and all its possible responses
class ListUsersTestCase(TestCase):
    # Initial setup for every test in ListUsersTestCase
    def setUp(self):
        self.client = APIClient()
        User.objects.create_user(username="testuser1", password="testpass1", email="test1@example.com")
        User.objects.create_user(username="testuser2", password="testpass2", email="test2@example.com")

    # Test #6: list_users_request success
    # status code: 200 OK
    def test_list_users(self):
        response = self.client.get("/listusers/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

# AddUserTestCase class
# Purpose: Test the add_user_request function and all its possible responses
class AddUserTestCase(TestCase):
    # Initial setup for every test in AddUserTestCase
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", password="testpass", email="test@example.com")

    # Test #7: add_user_request success
    # status code: 201 CREATED
    def test_add_user_success(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.post("/adduser/", {"username": "newuser", "password": "newpass", "email": "new@example.com"})
        self.assertEqual(response.status_code, 201)
        self.assertIn("success", response.data)

    # Test #8: add_user_request failure due to missing fields
    # status code: 400 BAD REQUEST
    # error message: Missing fields
    def test_add_user_missing_fields(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.post("/adduser/", {"username": "", "password": "", "email": ""})
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.data)
        self.assertEqual(response.data["error"], "Missing fields")
        response2 = self.client.post("/adduser/", {"username": "newuser", "password": "", "email": ""})
        self.assertEqual(response2.status_code, 400)
        self.assertIn("error", response2.data)
        self.assertEqual(response2.data["error"], "Missing fields")
        response3 = self.client.post("/adduser/", {"username": "", "password": "newpass", "email": ""})
        self.assertEqual(response3.status_code, 400)
        self.assertIn("error", response3.data)
        self.assertEqual(response3.data["error"], "Missing fields")
        response4 = self.client.post("/adduser/", {"username": "", "password": "", "email": "new@example.com"})
        self.assertEqual(response4.status_code, 400)
        self.assertIn("error", response4.data)
        self.assertEqual(response4.data["error"], "Missing fields")
        response5 = self.client.post("/adduser/", {"username": "newuser", "password": "newpass", "email": ""})
        self.assertEqual(response5.status_code, 400)
        self.assertIn("error", response5.data)
        self.assertEqual(response5.data["error"], "Missing fields")
        response6 = self.client.post("/adduser/", {"username": "", "password": "newpass", "email": "new@example.com"})
        self.assertEqual(response6.status_code, 400)
        self.assertIn("error", response6.data)
        self.assertEqual(response6.data["error"], "Missing fields")
        response7 = self.client.post("/adduser/", {"username": "newuser", "password": "", "email": "new@example.com"})
        self.assertEqual(response7.status_code, 400)
        self.assertIn("error", response7.data)
        self.assertEqual(response7.data["error"], "Missing fields")
    
    # Test #9: add_user_request failure due to user already existing
    # status code: 400 BAD REQUEST
    # error message: User already exists
    def test_add_user_user_already_exists(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.post("/adduser/", {"username": "testuser", "password": "examplepass", "email": "example@example.com"})
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.data)
        self.assertEqual(response.data["error"], "User already exists")
        response2 = self.client.post("/adduser/", {"username": "exampleuser", "password": "examplepass", "email": "test@example.com"})
        self.assertEqual(response2.status_code, 400)
        self.assertIn("error", response2.data)
        self.assertEqual(response2.data["error"], "User already exists")

    # Test #10: add_user_request failure due to the function being used while not logged on
    # status code: 403 FORBIDDEN
    def test_add_user_unauthenticated(self):
        response = self.client.post("/adduser/", {"username": "testuser", "password": "testpass", "email": "new@example.com"})
        self.assertEqual(response.status_code, 403)

# RemoveUserTestCase class
# Purpose: Test the remove_user_request function and all its possible responses
class RemoveUserTestCase(TestCase):
    # Initial setup for every test in RemoveUserTestCase
    def setUp(self):
        self.client = APIClient()
        User.objects.create_user(username="testuser", password="testpass")

    # Test #11: remove_user_request success
    # status code: 204 NO CONTENT
    def test_remove_user_success(self):
        response = self.client.delete("/removeuser/", {"username": "testuser", "password": "testpass"})
        self.assertEqual(response.status_code, 204)

    # Test #12: remove_user_request failure due to missing fields
    # status code: 400 BAD REQUEST
    # error message: Missing fields
    def test_remove_user_missing_fields(self):
        response = self.client.delete("/removeuser/", {"username": "", "password": "testpass"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["error"], "Missing fields")
        response2 = self.client.delete("/removeuser/", {"username": "testuser", "password": ""})
        self.assertEqual(response2.status_code, 400)
        self.assertEqual(response2.data["error"], "Missing fields")
        response3 = self.client.delete("/removeuser/", {"username": "", "password": ""})
        self.assertEqual(response3.status_code, 400)
        self.assertEqual(response3.data["error"], "Missing fields")

    # Test #13: remove_user_request failure due to wrong password
    # status code: 400 BAD REQUEST
    # error message: Wrong password
    def test_remove_user_wrong_password(self):
        response = self.client.delete("/removeuser/", {"username": "testuser", "password": "passpass"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["error"], "Wrong password")   

    # Test #14: remove_user_request failure due to user not existing
    # status code: 404 NOT FOUND
    # error message: User does not exist
    def test_remove_user_user_does_not_exist(self):
        response = self.client.delete("/removeuser/", {"username": "testtest", "password": "testpass"})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data["error"], "User does not exist")
