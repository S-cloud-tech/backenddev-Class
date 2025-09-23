from django.test import TestCase
from django.urls import reverse
from django.db.models import Sum
from library.models import Book, Category

class HomeViewTests(TestCase):
    def setUp(self):
        # Create categories
        self.cat1 = Category.objects.create(name="Fiction")
        self.cat2 = Category.objects.create(name="Science")
        self.cat3 = Category.objects.create(name="History")

        # Create books with read_count
        book1 = Book.objects.create(
            title="Book One", author="Author A", isbn="1111111111111", read_count=10
        )
        book2 = Book.objects.create(
            title="Book Two", author="Author B", isbn="2222222222222", read_count=20
        )
        book3 = Book.objects.create(
            title="Book Three", author="Author C", isbn="3333333333333", read_count=5
        )

        # Assign categories
        book1.category.add(self.cat1)
        book2.category.add(self.cat2)
        book3.category.add(self.cat1, self.cat3)

    def test_homepage_most_read_books(self):
        response = self.client.get(reverse("home")) 
        self.assertEqual(response.status_code, 200)
        most_read_books = response.context["most_read_books"]

        # Check order: highest read_count first
        self.assertEqual(most_read_books[0].title, "Book Two")
        self.assertEqual(most_read_books[1].title, "Book One")
        self.assertEqual(most_read_books[2].title, "Book Three")

    def test_homepage_recommended_categories(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        recommended_categories = response.context["recommended_categories"]

        # Fiction: book1(10) + book3(5) = 15
        # Science: book2(20)
        # History: book3(5)

        self.assertEqual(recommended_categories[0].name, "Science")  # 20 reads
        self.assertEqual(recommended_categories[1].name, "Fiction")  # 15 reads
        self.assertEqual(recommended_categories[2].name, "History")  # 5 reads

    def test_zero_reads_excluded(self):
        recommended_categories = (
            Category.objects.annotate(total_reads=Sum("books__read_count"))
            .filter(total_reads__gt=0)
            .order_by("-total_reads")
        )
        names = [c.name for c in recommended_categories]

        # ✅ History has 0 reads, so it should not appear
        self.assertNotIn("History", names)
