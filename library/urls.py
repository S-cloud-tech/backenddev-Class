from django.urls import path, include
from . import views

app_name = "library"

urlpatterns = [
    # Main Page endpoint
    path("", views.library_home, name="library_home"),

    # Book endpoints
    path("books/", views.available_books, name="available_books"),
    path("books/<int:pk>/", views.book_detail, name="book_detail"),
    path("add_book/", views.add_book, name="add_book"),

    # Category endpoints
    path("category/", views.all_category, name="all_category"),

    # Borrower endpoints
    # path("borrowers/", views.borrow_book.as_view(), name="borrower-list"),
    # path("borrowers/<int:pk>/", views.BorrowerDetailView.as_view(), name="borrower-detail"),

    # Borrow & Return endpoints
    path("borrow/", views.borrow_book, name="borrow-book"),
    path("return/", views.return_book, name="return-book"),

    # Fine endpoints
    # path("fines/", views.FineListView.as_view(), name="fine-list"),

    # API endpoints
    path("api/", include("library.api.urls")), 
]
