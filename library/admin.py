from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "description"]
    search_fields = ["name"]

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ["title", "author", "isbn", "category"]
    list_filter = ["category"]
    search_fields = ["title", "author", "category"]

@admin.register(Borrower)
class BorrowerAdmin(admin.ModelAdmin):
    list_display = []


@admin.register(BorrowRecord)
class BorrowRecordAdmin(admin.ModelAdmin):
    list_display = ["book", "status", "borrow_date", "due_date", "returned_date"]
    list_filter = ["status", "borrow_date", "due_date"]
    search_fields = ["book_title"]

@admin.register(Fine)
class FineAdmin(admin.ModelAdmin):
    list_display = ["borrow_record", "amount", "paid"]
    list_filter = ["paid",]
