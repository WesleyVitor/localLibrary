from django.urls import path, include
from catalog import views
authorspatterns = [
    path('', views.AuthorListView.as_view(), name="authors"),
    path('<int:pk>', views.AuthorDetailView.as_view(), name="author-detail"),
    path('create/', views.AuthorCreate.as_view(), name="author_create"),
    path('<int:pk>/update', views.AuthorUpdate.as_view(), name="author_update"),
    path('<int:pk>/delete', views.AuthorDelete.as_view(), name="author_delete"),
]

urlpatterns = [
    path("", views.index, name="index"),
    path("books/", views.BookListView.as_view(), name="books"),
    path(r"^book/(?P<pk>\d+)$", views.BookDetailView.as_view(), name="book-detail"),
    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
    path('borrowed/', views.LoadnedBooksOnLoad.as_view(), name='borrowed'),
    path('book/<uuid:pk>/renew/', views.renew_book_librarian, name='renew-book-librarian'),
    path('author/', include(authorspatterns)),

]