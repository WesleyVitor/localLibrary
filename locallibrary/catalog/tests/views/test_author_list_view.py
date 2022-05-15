from django.test import TestCase
from django.urls import reverse

from catalog.models import Author


class AuthorListViewTest(TestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        
        num_authors = 13
        
        for author_id in range(num_authors):
            Author.objects.create(
                first_name=f'João {author_id}',
                last_name= f'Santos {author_id}'
            )

    #Teste para saber se existe uma view relacionada à uma URL
    def test_view_exists_at_url(self):
        response = self.client.get('/catalog/author/')
        self.assertEqual(response.status_code, 200)

    #Teste para saber se existe uma URL relacionada à um nome
    def test_call_url_by_name(self):
        response = self.client.get(reverse('authors'))
        self.assertEqual(response.status_code, 200)
    #Teste para saber se o template correto foi usado
    def test_template_correct_is_used(self):
        response = self.client.get(reverse('authors'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'authors/authors_template_list.html')
    
    #Verificar o número de paginação é 10
    def test_pagination_ten(self):
        response = self.client.get(reverse('authors'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertEqual(len(response.context['author_list']), 10)
    
    #Verificar se são mostrado todos os itens
    def test_view_all_authors(self):
        response = self.client.get(reverse('authors') + '?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertEqual(len(response.context['author_list']), 3)