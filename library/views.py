from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.utils import timezone
from .models import *

# 1. List all available books
def available_books(request):
    books = Book.objects.filter(is_available=True)
    return render(request, "library/available_books.html", {"books": books})

# 2. View details of a book
def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    return render(request, "library/book_detail.html", {"book": book})

# 3. Borrow a book
def borrow_book(request, book_id, member_id):
    book = get_object_or_404(Book, id=book_id)
    # member = get_object_or_404(Member, id=member_id)

    if book.is_available:
        record = BorrowRecord.objects.create(
            book=book,
            borrow_date=timezone.now(),
            status=BorrowRecord.Status.BORROWED,
        )
        book.is_available = False
        book.save()
        return JsonResponse({"message": f"user borrowed {book.title}"})
    return JsonResponse({"error": "Book is not available"}, status=400)

# 4. Return a book
def return_book(request, record_id):
    record = get_object_or_404(BorrowRecord, id=record_id)
    record.return_date = timezone.now()
    record.status = BorrowRecord.Status.RETURNED
    record.book.is_available = True
    record.book.save()

    # Check overdue
    if record.return_date.date() > record.due_date:
        days_overdue = (record.return_date.date() - record.due_date).days
        Fine.objects.create(
            record=record,
            amount=days_overdue * 5  # Example: 5 units per day
        )
    record.save()
    return JsonResponse({"message": f"{record.book.title} returned successfully"})

# 5. View member fines
# def member_fines(request, member_id):
#     member = get_object_or_404(Member, id=member_id)
#     fines = Fine.objects.filter(record__member=member)
#     return render(request, "library/member_fines.html", {"member": member, "fines": fines})



