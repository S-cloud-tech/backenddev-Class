from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Count
from .models import *
from .forms import *

def library_home(request):
    # 1. Number of books borrowed (all time)
    total_borrowed = BorrowRecord.objects.count()

    # 2. Number of books read (returned books)
    total_read = BorrowRecord.objects.filter(returned_date__isnull=False).count()

    # 3. Trending books (top 5 by borrow count)
    # trending_books = (
    #     Book.objects.annotate(borrow_count=Count("borrow_record"))
    #     .order_by("-borrow_count")[:5]
    # )

    # 4. Top authors (based on borrow counts of their books)
    # top_authors = (
    #     Book.objects.annotate(borrow_count=Count("book__borrow"))
    #     .order_by("-borrow_count")[:5]
    # )

    # 5. Recommendations (books user hasn’t borrowed but others did)
    recommendations = []
    if request.user.is_authenticated:
        borrowed_books = BorrowRecord.objects.filter(borrower=request.user).values_list(
            "book_id", flat=True
        )
        recommendations = (
            Book.objects.exclude(id__in=borrowed_books)
            .annotate(borrow_count=Count("borrow"))
            .order_by("-borrow_count")[:5]
        )

    context = {
        "total_borrowed": total_borrowed,
        "total_read": total_read,
        "recommendations": recommendations,
    }
    return render(request, "home/index.html")

# 1. List all available books
def available_books(request):
    books = Book.objects.all()
    return render(request, "book/book_list.html", {"books": books})

def add_book(request):
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(request, "library:book_list", {"books": Book.objects.all()})
        else:
            return render(request, "book/book_form.html", {"form": form})
    else:
        form = BookForm()
    return render(request, "book/book_form.html", {"form": form})

def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect("library:book_list")
    else:
        form = BookForm(instance=book)
    return render(request, "book/book_form.html", {"form": form})

def all_category(request):
    category = Category.objects.all()

    return render(request, "book/book_category.html", {"category": category})


# 2. View details of a book
def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    return render(request, "book/book_detail.html", {"book": book})

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



