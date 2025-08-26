from django.urls import path, include
from . import views

app_name = "library"

urlpatterns = [
    # Book endpoints
    path("books/", views.available_books, name="book-list"),
    path("books/<int:pk>/", views.book_detail, name="book-detail"),

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
