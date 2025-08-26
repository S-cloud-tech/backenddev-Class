# from django.test import TestCase
# from django.utils import timezone
# from datetime import timedelta
# from ..models import *


# class CategoryModelTest(TestCase):

#     def test_category_str(self):
#         category = Category.objects.create(name="Science", description="Books about science")
#         self.assertEqual(str(category), "Science")


# class BookModelTest(TestCase):

#     def setUp(self):
#         self.category = Category.objects.create(name="Fiction")

#     def test_create_book(self):
#         book = Book.objects.create(
#             title="The Great Gatsby",
#             author="F. Scott Fitzgerald",
#             isbn="1234567890123",
#             category=self.category,
#             total_copies=5,
#             available_copies=5,
#             description="A classic novel",
#             added_on=timezone.now()
#         )
#         self.assertEqual(book.title, "The Great Gatsby")
#         self.assertEqual(book.category.name, "Fiction")
#         self.assertEqual(str(book), "The Great Gatsby by F. Scott Fitzgerald")


# class BorrowRecordModelTest(TestCase):

#     def setUp(self):
#         self.category = Category.objects.create(name="History")
#         self.book = Book.objects.create(
#             title="World History",
#             author="John Doe",
#             isbn="9876543210123",
#             category=self.category,
#             total_copies=3,
#             available_copies=3,
#             added_on=timezone.now()
#         )

#     def test_create_borrow_record_default_status(self):
#         due_date = timezone.now() + timedelta(days=7)
#         record = BorrowRecord.objects.create(
#             book=self.book,
#             due_date=due_date
#         )
#         self.assertEqual(record.status, BorrowRecord.Status.BORROWED)
#         self.assertEqual(str(record), "World History (BORROWED)")

#     def test_borrow_record_status_change(self):
#         due_date = timezone.now() + timedelta(days=7)
#         record = BorrowRecord.objects.create(
#             book=self.book,
#             due_date=due_date
#         )
#         record.status = BorrowRecord.Status.RETURNED
#         record.save()
#         self.assertEqual(record.status, "RETURNED")


# class FineModelTest(TestCase):

#     def setUp(self):
#         self.category = Category.objects.create(name="Philosophy")
#         self.book = Book.objects.create(
#             title="Meditations",
#             author="Marcus Aurelius",
#             isbn="5555555555555",
#             category=self.category,
#             total_copies=2,
#             available_copies=2,
#             added_on=timezone.now()
#         )
#         self.record = BorrowRecord.objects.create(
#             book=self.book,
#             due_date=timezone.now() + timedelta(days=7)
#         )

#     def test_fine_creation(self):
#         fine = Fine.objects.create(borrow_record=self.record, amount=25.00)
#         self.assertEqual(fine.amount, 25.00)
#         self.assertFalse(fine.paid)
#         self.assertEqual(str(fine), f"Fine 25.00 for {self.record}")
