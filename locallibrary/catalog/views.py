from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from typing import Any
from .models import Author, Book, BookInstance, Genre

from django.views import generic

from django.contrib.auth.decorators import login_required

from django.contrib.auth.mixins import LoginRequiredMixin
@login_required
def index(request: HttpRequest) -> HttpResponse:
    
    num_visits = request.session.get('num_visits',0)
    request.session['num_visits'] = num_visits + 1

    num_books:int = Book.objects.all().count()
    num_book_instance:int = BookInstance.objects.all().count()
    num_book_instance_available:int = BookInstance.objects.filter(status__exact='a').count()
    num_authors:int = Author.objects.all().count()
    num_genre:int = Genre.objects.all().count()
    num_book_sumary_at_tecnology_word = Book.objects.filter(sumary__contains = 'tecnolgy').count()
    context = {
        'num_books':num_books,
        'num_book_instance':num_book_instance,
        'num_book_instance_available':num_book_instance_available,
        'num_authors':num_authors,
        'num_genre':num_genre,
        'num_book_sumary_at_tecnology_word':num_book_sumary_at_tecnology_word,
        'num_visits':num_visits
    }

    return render(request, 'index.html', context=context)

class BookListView(LoginRequiredMixin,generic.ListView):
    model = Book
    #Por padrão a variável que contém ,dentro de templates, para acessar a lista de books é book_list.
    context_object_name = 'my_book_list'

    #Por padrão o template que é gereado é book_list.html
    template_name = 'books/book_template_list.html'

    #Por padrão o queryset é buscar tudo, mas eu posso mudar a sua chamada
    # def get_queryset(self):
    #     return Book.objects.filter(title__icontains='war')[:5]

    # Mudando o contexto que será fornecido para o template gerado
    def get_context_data(self, **kwargs: Any):
        #Pegando o contexto do pai
        context =  super(BookListView, self).get_context_data(**kwargs)
        context['some_data'] = Genre.objects.all().count()
        return context

class BookDetailView(generic.DetailView):
    model = Book
    paginate_by=2
    template_name = 'books/book_detail.html'

class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = 'books/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')
    