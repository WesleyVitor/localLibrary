from django.contrib import admin
from catalog.models import * 
# Register your models here.

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'date_of_birth')
    fieldsets = (
        ("Name Information", {
            "fields": (
                'first_name','last_name'
            ),
        }),
        ("Other Information",{
                "fields": (
                    'date_of_birth', 'date_of_death')}
        ),
    )

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'display_genre')
    # Chama um método de Book chamado display_genre como tem uma relação many-to-many com genre
    

@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'due_back')
    list_filter = ('status', 'due_back')
    
@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)
    
@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ('name',)

