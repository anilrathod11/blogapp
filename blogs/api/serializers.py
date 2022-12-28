from rest_framework import serializers
from blogs.models import Blog,Category

class BlogSerializer(serializers.ModelSerializer):
    # review_user = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Blog
        fields = "__all__"

class CategorySerializer(serializers.ModelSerializer):
    # review_user = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Category
        fields = "__all__"