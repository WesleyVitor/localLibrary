from unittest import expectedFailure
from django.test import TestCase

from catalog.models import Author

class AuthorModelTest(TestCase):

    @classmethod
    def setUpTestData(cls) -> None: # Uma vez antes de todos os testes
        Author.objects.create(first_name='Matheus', last_name='Santos')
    
    def test_first_name_label(self):
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field('first_name').verbose_name
        self.assertEqual(field_label, 'first name')  
    
    def test_last_name_label(self):
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field('last_name').verbose_name
        self.assertEqual(field_label, 'last name')
    
    def test_first_name_max_length(self):
        author = Author.objects.get(id=1)
        field_max_length = author._meta.get_field('first_name').max_length
        self.assertEqual(field_max_length,100)
    
    def test_last_name_max_length(self):
        author = Author.objects.get(id=1)
        field_max_length = author._meta.get_field('last_name').max_length
        self.assertEqual(field_max_length,100)

    def test_object_name_is_last_name_comma_first_name(self):
        author = Author.objects.get(id=1)
        expect_object_name = f'{author.last_name}, {author.first_name}'
        self.assertEqual(str(author), expect_object_name)
    
    def test_get_absolute_url(self):
        author = Author.objects.get(id=1)
        expected_url = '/catalog/author/1'
        self.assertEqual(author.get_absolute_url(), expected_url)