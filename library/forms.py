from django import forms
from .models import *

class BookForm():
    class Meta:
        model = Book
        fields = ["title", "author", "isbn", "category", "description", "total_copies", "is_available"]
