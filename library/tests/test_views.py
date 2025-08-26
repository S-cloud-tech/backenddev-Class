# from django.test import TestCase
# from django.urls import reverse
# from django.utils import timezone
# from library.models import Book, BorrowRecord, Fine


# class LibraryViewsTest(TestCase):
#     def setUp(self):
#         # Create a sample book
#         self.book = Book.objects.create(
#             title="Django for Beginners",
#             author="William S. Vincent",
#             isbn="1234567890123",
#             is_available=True,
#         )

#     def test_available_books_view(self):
#         response = self.client.get(reverse("library:available_books"))
#         self.assertEqual(response.status_code, 200)
#         self.assertContains(response, "Django for Beginners")

#     def test_book_detail_view(self):
#         response = self.client.get(reverse("library:book_detail", args=[self.book.id]))
#         self.assertEqual(response.status_code, 200)
#         self.assertContains(response, self.book.title)

#     def test_borrow_book_view(self):
#         response = self.client.get(reverse("library:borrow_book", args=[self.book.id, 1]))
#         self.assertEqual(response.status_code, 200)
#         self.book.refresh_from_db()
#         self.assertFalse(self.book.is_available)  # Book should now be unavailable

#     def test_return_book_view(self):
#         # Borrow first
#         record = BorrowRecord.objects.create(
#             book=self.book,
#             borrow_date=timezone.now(),
#             due_date=timezone.now().date(),
#             status=BorrowRecord.Status.BORROWED,
#         )
#         self.book.is_available = False
#         self.book.save()

#         response = self.client.get(reverse("library:return_book", args=[record.id]))
#         self.assertEqual(response.status_code, 200)

#         record.refresh_from_db()
#         self.assertEqual(record.status, BorrowRecord.Status.RETURNED)
#         self.assertTrue(record.book.is_available)

#     def test_overdue_fine_on_return(self):
#         # Borrow book with past due date
#         past_due_date = timezone.now().date() - timezone.timedelta(days=3)
#         record = BorrowRecord.objects.create(
#             book=self.book,
#             borrow_date=timezone.now() - timezone.timedelta(days=10),
#             due_date=past_due_date,
#             status=BorrowRecord.Status.BORROWED,
#         )
#         self.book.is_available = False
#         self.book.save()

#         response = self.client.get(reverse("library:return_book", args=[record.id]))
#         self.assertEqual(response.status_code, 200)

#         fines = Fine.objects.filter(record=record)
#         self.assertTrue(fines.exists())
#         fine = fines.first()
#         self.assertEqual(fine.amount, 3 * 5)  # 3 days overdue * 5 units
