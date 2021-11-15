from django.test import TestCase
from users.models import Subscribe


class SubscribeModelTest(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.data1 = {
            "email": "nnn@gmail.com"
        }
        cls.data2 = {
            "email":"mmm@gmail.com"
        }
        cls.info1 = Subscribe.objects.create(**cls.data1)
        cls.info2 = Subscribe.objects.create(**cls.data2)

    def test_created_data(self):
        self.assertEqual(self.info1.email, self.data1['email'])
        self.assertEqual(self.info2.email, self.data2['email'])

    @classmethod
    def tearDownClass(cls):
        pass