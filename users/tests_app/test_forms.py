from users.forms import LoginForm
from django.test import TestCase

class LoginFormTest(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.valid_data = {
            "username": "narmin",
            "password": "checktest123"
        }
        cls.invalid_data = {
            "username": "nar",
            "password": ""
        }
        cls.form = LoginForm

    def test_form_with_valid_data(self):
        form = self.form(data=self.valid_data)
        self.assertTrue(form.is_valid())

    def test_form_with_invalid_data(self):
        form = LoginForm(data=self.invalid_data)
        self.assertFalse(form.is_valid())
        self.assertIn("password", form.errors)
        self.assertIn("This field is required.", form.errors['password'])        

    @classmethod
    def tearDownClass(cls):
        pass