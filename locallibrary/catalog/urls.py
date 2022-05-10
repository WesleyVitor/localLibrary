from django.urls import path
from catalog import views
urlpatterns = [
    path("", views.index, name="index"),
    path("books/", views.BookListView.as_view(), name="books"),
    path(r"^book/(?P<pk>\d+)$", views.BookDetailView.as_view(), name="book-detail"),
    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
]