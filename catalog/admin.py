from django.contrib import admin
from .models import Author, Genre, Book, BookInstance, Language

# Register your models here.
class AuthorAdmin(admin.ModelAdmin):
	list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
	fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]

admin.site.register(Author, AuthorAdmin)


class BooksInstanceInline(admin.TabularInline):
    model = BookInstance

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
	list_display =('title', 'author','display_genre')
	inlines = [BooksInstanceInline]

#admin.site.register(Book, BookAdmin)

class GenreAdmin(admin.ModelAdmin):
	pass

admin.site.register(Genre, GenreAdmin)




@admin.register(BookInstance) 
class BookInstanceAdmin(admin.ModelAdmin):
	list_display = ('book', 'due_back', 'status', 'id')
	list_filter = ('status', 'due_back')
	fieldsets = (
        (None, {
            'fields': ('book','imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back')
        }),
    )

#admin.site.register(BookInstance, BookInstanceAdmin)

class LanguageAdmin(admin.ModelAdmin):
	pass

admin.site.register(Language, LanguageAdmin)