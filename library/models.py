from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Book(models.Model):
    images = models.ImageField(upload_to="static/images/book/", null=True)
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    isbn = models.CharField(max_length=13, unique=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="books")
    description = models.TextField(blank=True, null=True)
    total_copies = models.PositiveIntegerField(default=1)
    available_copies = models.PositiveIntegerField(default=1)
    is_available = models.BooleanField(default=True)
    added_on = models.DateTimeField()

    def __str__(self):
        return f"{self.title} by {self.author}"

class Borrower(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.name

class BorrowRecord(models.Model):
    class Status(models.TextChoices):
        BORROWED = "BORROWED", "Borrowed"
        RETURNED = "RETURNED", "Returned"
        OVERDUE = "OVERDUE", "Overdue"

    borrower = models.ForeignKey(Borrower, on_delete=models.CASCADE, related_name="borrowed_books")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="borrow_records")
    borrow_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()
    returned_date = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.BORROWED)

    def __str__(self):
        return f"{self.book.title} ({self.status})"

class Fine(models.Model):
    borrow_record = models.OneToOneField(BorrowRecord, on_delete=models.CASCADE, related_name="fine")
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Fine {self.amount:.2f} for {self.borrow_record}"
