from django.urls import path
from . import views

app_name = "library_api"

urlpatterns = [
    path("category/", views.CategoryListView.as_view(), name="category-list"),
    path("category/<int:pk>/", views.CategoryDetailView.as_view(), name="category-detail"),
    path("books/", views.BookListView.as_view(), name="book-list"),
    path("books/<int:pk>/", views.BookDetailView.as_view(), name="book-detail"),
    path("borrowers/", views.BorrowerListView.as_view(), name="borrower-list"),
    path("borrowers/<int:pk>/", views.BorrowerDetailView.as_view(), name="borrower-detail"),
    path("borrow/", views.BorrowBookView.as_view(), name="borrow-book"),
    path("return/", views.ReturnBookView.as_view(), name="return-book"),
    path("fines/", views.FineListView.as_view(), name="fine-list"),
]
