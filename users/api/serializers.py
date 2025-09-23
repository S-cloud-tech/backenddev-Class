from django.contrib.auth.models import User, Group
from django.utils.crypto import get_random_string
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.conf import settings
from rest_framework import serializers

class UserSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "email", "password")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        group = Group.objects.get(name="User")
        user.groups.add(group)
        return user


class LibrarianSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "email")  # no password field exposed

    def create(self, validated_data):
        # generate a random password
        random_password = get_random_string(12)
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=random_password  # temporary
        )

        group, _ = Group.objects.get_or_create(name="Librarian")
        user.groups.add(group)

        user.is_staff = False
        user.save()

        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        reset_link = f"{settings.FRONTEND_URL}/reset-password/{uid}/{token}/"

        send_mail(
            subject="Set your Librarian account password",
            message=f"Hello {user.username},\n\nAn account has been created for you as a Librarian.\n"
                    f"Please set your password using the link below:\n\n{reset_link}\n\n"
                    "If you did not expect this email, please ignore it.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )

        return user