from django.test import TestCase
from api.models import Animal, Breed, Pet

# Create your tests here.

class AnimalModelTest(TestCase):
    def setUp(self):
        pet = Pet.objects.create(name="dog pet")
        breed = Breed.objects.create(name="dog breed", pet=pet)
        Animal.objects.create(name="dog", price=1233.45, breed=breed)
        
    def test_model_update(self):
        animal_len = Animal.objects.count()
        self.assertEqual(animal_len, 1)