from rest_framework import serializers
from ..models import *


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"


class BorrowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrower
        fields = "__all__"


class BorrowRecordSerializer(serializers.ModelSerializer):
    borrower = BorrowerSerializer(read_only=True)
    borrower_id = serializers.PrimaryKeyRelatedField(
        queryset=Borrower.objects.all(), source="borrower", write_only=True
    )

    class Meta:
        model = BorrowRecord
        fields = ["id", "borrower", "borrower_id", "book", "borrow_date", "return_date", "status"]


class FineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fine
        fields = "__all__"
