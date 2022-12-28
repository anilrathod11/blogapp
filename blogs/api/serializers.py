from rest_framework import serializers
from blogs.models import Blog,Category,CommentOnBlog

class BlogSerializer(serializers.ModelSerializer):
    # review_user = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Blog
        fields = "__all__"
        # read_only_fields = ['content', 'title','category']

class CategorySerializer(serializers.ModelSerializer):
    # review_user = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Category
        fields = "__all__"
class CommentSerializer(serializers.ModelSerializer):
    # review_user = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = CommentOnBlog
        fields = "__all__"