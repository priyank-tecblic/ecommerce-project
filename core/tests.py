from django.test import TestCase
from .models import *
from django_seed import Seed
seeder = Seed.seeder()
# Create your tests here.
class FirstTestCases(TestCase):

    def setup(self):
        print("setup called")
    
    def test_product(self):
        print("im here")
        seeder.add_entity(Product,10)
        seeder.execute()
        print("test complete")