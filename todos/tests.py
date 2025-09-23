from django.test import TestCase
from .models import Todo

# Create your tests here.
class TodoModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Todo.objects.create(title='first todo', description='First thing to do in the morning')

    def test_title_content(self):
        todo = Todo.objects.get(id=1)
        expected_object_name = f'{todo.title}'
        self.assertEqual(expected_object_name, 'first todo')

    def test_description_content(self):
        todo = Todo.objects.get(id=1)
        expected_object_name = f'{todo.description}'
        self.assertEqual(expected_object_name, 'First thing to do in the morning')
