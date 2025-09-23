from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from ...models import Book

class Command(BaseCommand):
    help = 'Create user roles and assign permissions'

    def handle(self, *args, **kwargs):
        # Create roles
        user_group, _ = Group.objects.get_or_create(name='User')
        librarian_group, _ = Group.objects.get_or_create(name='Librarian')
        admin_group, _ = Group.objects.get_or_create(name='Admin')

        # Get default permissions
        content_type = ContentType.objects.get_for_model(Book)
        add_book = Permission.objects.get(codename='add_book', content_type=content_type)
        change_book = Permission.objects.get(codename='change_book', content_type=content_type)
        delete_book = Permission.objects.get(codename='delete_book', content_type=content_type)
        view_book = Permission.objects.get(codename='view_book', content_type=content_type)

    
        archive_book = Permission.objects.get(codename='can_archive_book')
        save_book = Permission.objects.get(codename='can_save_book')

        # Assign to groups
        user_group.permissions.set([view_book, save_book]) 

        librarian_group.permissions.set([
            add_book, change_book, view_book, archive_book
        ])

        admin_group.permissions.set([
            add_book, change_book, delete_book, view_book,
            archive_book
        ])

        self.stdout.write(self.style.SUCCESS("Roles and permissions set up successfully!"))
