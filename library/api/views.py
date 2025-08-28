from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from ..models import *
from .serializers import *
from django.utils import timezone


# -------------- CATEGORY VIEWS -----------------
class CategoryListView(generics.ListCreateAPIView):
    queryset =Category.objects.all()
    serializer_class = CategorySerializer


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


# ------------------ BOOK VIEWS ------------------
class BookListView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


# ------------------ BORROWER VIEWS ------------------
class BorrowerListView(generics.ListCreateAPIView):
    queryset = Borrower.objects.all()
    serializer_class = BorrowerSerializer


class BorrowerDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Borrower.objects.all()
    serializer_class = BorrowerSerializer


# ------------------ BORROW & RETURN RECORD ------------------
class BorrowBookView(APIView):
    def post(self, request):
        borrower_id = request.data.get("borrower_id")
        book_id = request.data.get("book_id")

        try:
            borrower = Borrower.objects.get(id=borrower_id)
            book = Book.objects.get(id=book_id)

            if book.available_copies <= 0:
                return Response({"error": "No copies available"}, status=status.HTTP_400_BAD_REQUEST)

            # Create borrow record
            borrow = BorrowRecord.objects.create(
                borrower=borrower,
                book=book,
                borrow_date=timezone.now(),
            )

            # Reduce available copies
            book.available_copies -= 1
            book.save()

            return Response(BorrowRecordSerializer(borrow).data, status=status.HTTP_201_CREATED)

        except Borrower.DoesNotExist:
            return Response({"error": "Borrower not found"}, status=status.HTTP_404_NOT_FOUND)
        except Book.DoesNotExist:
            return Response({"error": "Book not found"}, status=status.HTTP_404_NOT_FOUND)


class ReturnBookView(APIView):
    def post(self, request):
        borrow_id = request.data.get("borrow_id")

        try:
            borrow = BorrowRecord.objects.get(id=borrow_id, return_date__isnull=True)
            borrow.return_date = timezone.now()
            borrow.save()

            # Increase book available copies
            book = borrow.book
            book.available_copies += 1
            book.save()

            # Check overdue fine
            if borrow.return_date > borrow.due_date:
                Fine.objects.create(
                    borrower=borrow.borrower,
                    amount=500.0,  # for now fixed fine (later can be calculated)
                    paid=False,
                )

            return Response({"message": "Book returned successfully"}, status=status.HTTP_200_OK)

        except BorrowRecord.DoesNotExist:
            return Response({"error": "Active borrow not found"}, status=status.HTTP_404_NOT_FOUND)


# ------------------ FINES ------------------
class FineListView(generics.ListAPIView):
    queryset = Fine.objects.all()
    serializer_class = FineSerializer
