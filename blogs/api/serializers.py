from rest_framework import serializers
from blogs.models import Blog,Category,CommentOnBlog
from blogs.models import RandomPicture

class ImageSerializer(serializers.ModelSerializer):
        class Meta:
            model = RandomPicture
            fields = '__all__'
            
class BlogSerializer(serializers.ModelSerializer):
    # review_user = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Blog
        fields = ["id","title","content","author","reviewer","status","category","public"]
        # read_only_fields = ['content', 'title','category']

class CategorySerializer(serializers.ModelSerializer):
    # review_user = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Category
        fields = ["id","name"]
        
class CommentSerializer(serializers.ModelSerializer):
    # review_user = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = CommentOnBlog
        fields = "__all__"