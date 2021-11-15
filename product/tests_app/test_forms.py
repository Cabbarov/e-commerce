from django.test import TestCase
from product.forms import ReviewForm

class ReviewFormTest(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.valid_data = {
            "name": "narmin",
            "email": "nn@mm.com",
            "description": "good",
            "rate": 4
        }
        cls.invalid_data = {
            "email": "nn@mm.com",
            "description": "nice",
            "rate": 1
        }
        cls.form = ReviewForm

    def test_form_with_valid_data(self):
        form = self.form(data=self.valid_data)
        self.assertTrue(form.is_valid())

    def test_form_with_invalid_data(self):
        form = ReviewForm(data=self.invalid_data)
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)
        self.assertIn("This field is required.", form.errors['name'])   
        print(form.errors)     

    @classmethod
    def tearDownClass(cls):
        pass