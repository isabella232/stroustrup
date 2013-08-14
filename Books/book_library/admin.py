from django.contrib import admin
from models import Book, Author, Book_Tag

class BooksInLine(admin.TabularInline):
    model = Book

class TagsInLine(admin.StackedInline):
    model = Book_Tag

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'isbn')

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name')

class Book_TagAdmin(admin.ModelAdmin):
    display = 'tag'
    inlines = [TagsInLine]

admin.site.register(Book, BookAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Book_Tag, Book_TagAdmin)