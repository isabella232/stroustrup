from django.forms import ModelForm
from models import Book

class ArticleForm(ModelForm):

    class Meta:
        model = Book
        fields = ['isbn', 'title', 'e_version_exists', 'paperback_version_exists', 'description', 'picture', 'authors', 'tags']