from django.db.models.expressions import Col
from django.test import TestCase
from product.models import Color

class ColorModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data1 = {
            "name": "#FF5733"
        }
        cls.data2 = {
            "name":"#CD5C5C"
        }
        cls.info1 = Color.objects.create(**cls.data1)
        cls.info2 = Color.objects.create(**cls.data2)

    def test_created_data(self):
        self.assertEqual(self.info1.name, self.data1['name'])
        self.assertEqual(self.info2.name, self.data2['name'])

    @classmethod
    def tearDownClass(cls):
        pass