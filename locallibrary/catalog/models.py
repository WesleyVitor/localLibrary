from modulefinder import LOAD_CONST
from django.db import models
from django.urls import reverse
import uuid
class Genre(models.Model):
    name = models.CharField(max_length=200, help_text='Enter a book genre (e.g. Science Fiction)')

    def __str__(self) -> str:
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    sumary = models.TextField(max_length=1000, help_text='Enter a brief description of the book')
    isbn = models.CharField(verbose_name="ISBN", max_length=13, help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    genre = models.ManyToManyField(Genre, help_text='Select a genre for this book')
    language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True)

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):
        return reverse("book-detail", args=[str(self.id)])
    
    def display_genre(self):
        return ", ".join(genre.name for genre in self.genre.all()[:3])
    
    display_genre.short_description = 'Genre'
    
class BookInstance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)
    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(max_length=1, blank=True, 
    null=True, choices=LOAN_STATUS,help_text='Book availability')

    class Meta:
        ordering = ["due_back"]
    
    def __str__(self) -> str:
        return f'{self.id} ({self.book.title})'

class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField(verbose_name="Died",null=True, blank=True)

    class Meta:
        ordering = ["last_name", "first_name"]
    
    def __str__(self) -> str:
        return f"{self.last_name}, {self.first_name}"

    def get_absolute_url(self):
        return reverse("author-detail", args=[str(self.id)])

class Language(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name


