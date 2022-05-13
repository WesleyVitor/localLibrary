from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from typing import Any
from .models import Author, Book, BookInstance, Genre
from .forms import RenewBookForm

from django.views import generic
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

import datetime
from django.urls import reverse, reverse_lazy


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


class LoanedBooksByUserListView(PermissionRequiredMixin,LoginRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = 'books/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    permission_required = 'catalog.can_mark_returned'
    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')
    
class LoadnedBooksOnLoad(PermissionRequiredMixin,LoginRequiredMixin,generic.ListView):
    model = BookInstance
    template_name = 'books/bookinstance_list_borrowed.html'
    permission_required = 'catalog.can_view_all_borrowed'

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')


class AuthorListView(generic.ListView):
    model = Author
    template_name = 'authors/authors_template_list.html'


class AuthorCreate(PermissionRequiredMixin,generic.CreateView):
    permission_required = 'can_view_all_borrowed'
    model = Author
    fields = '__all__'
    success_url = reverse_lazy('authors')
    template_name = 'authors/author_form.html'
    initial = {'date_of_death': '05/01/2018'}

class AuthorUpdate(PermissionRequiredMixin,generic.UpdateView):
    permission_required = 'can_view_all_borrowed'
    model = Author
    success_url = reverse_lazy('authors')
    template_name = 'authors/author_form.html'
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']

class AuthorDelete(PermissionRequiredMixin,generic.DeleteView):
    permission_required = 'can_view_all_borrowed'
    model = Author
    success_url = reverse_lazy('authors')
    template_name = 'authors/author_confirm_delete.html'

class AuthorDetailView(PermissionRequiredMixin, generic.DetailView):
    permission_required = 'can_view_all_borrowed'
    model = Author
    template_name: str = 'authors/author_detail.html'


@permission_required('catalog.can_view_all_borrowed')
def renew_book_librarian(request, pk):

    book_instance = get_object_or_404(BookInstance, pk=pk)

    if request.method == 'POST':
        form = RenewBookForm(request.POST)

        if form.is_valid():
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()

            return HttpResponseRedirect(reverse('borrowed'))
    
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)

        form = RenewBookForm(initial={'renewal_date':proposed_renewal_date})

        context = {
            'form':form,
            'book_instance':book_instance
        }

        return render(request, 'books/book_renew_librarian.html', context)