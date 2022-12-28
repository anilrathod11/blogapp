from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework import status
# # from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly,IsAdminUser
from blogs.api.permissions import IsAdminOrReadOnly,IsReviewUserOrReadOnly
from rest_framework.views import APIView
from blogs.api.serializers import BlogSerializer, CategorySerializer
from blogs.models import Blog, Category
from user_app.models import CustomeUser

class BlogAV(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    def get(self, request):
        try:
            user = CustomeUser.objects.get(pk=request.user.id)
        except CustomeUser.DoesNotExist:
            return Response({'message':"Only authenticated user can access this resources"}, status=status.HTTP_400_BAD_REQUEST)
        if user.role == "Author":
            blogs = Blog.objects.filter(author=user)
            # serializer = StreamPlatformSerializer(platform,many=True,context={'request': request})
            serializer = BlogSerializer(blogs,many=True)
            return Response({"list_of_author_blogs":serializer.data},status=status.HTTP_200_OK)
        
        elif user.role == "Admin":     
            blogs = Blog.objects.all()
            # serializer = StreamPlatformSerializer(platform,many=True,context={'request': request})
            serializer = BlogSerializer(blogs,many=True)
            return Response({"list_of_blogs":serializer.data},status=status.HTTP_200_OK)
        elif user.role == "Reader":
            blogs = Blog.objects.filter(status="Active")
            # serializer = StreamPlatformSerializer(platform,many=True,context={'request': request})
            serializer = BlogSerializer(blogs,many=True)
            return Response({"list_of_active_blogs":serializer.data},status=status.HTTP_200_OK)
        else:
            print("Rathod")
            return Response({'message':"Only authenticated user can access this resource"}, status=status.HTTP_400_BAD_REQUEST)
    def post(self, request):
        user = CustomeUser.objects.get(pk=request.user.id)
        if user.role == "Author" or user.role == "Writer":
            request.data["author"] = request.user.id
            serializer = BlogSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message":"Blog object created successfully","created_object":serializer.data},status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors)
        else:
            return Response({'message':"Only author and writer can post blog"},status=status.HTTP_400_BAD_REQUEST)
        
class BlogDetailAV(APIView):
    # permission_classes = [IsAdminOrReadOnly]
    def get(self, request, pk):
        try:
            blog = Blog.objects.get(pk=pk)
        except Blog.DoesNotExist:
            return Response({'message':"Blog not found with given id"},status=status.HTTP_404_NOT_FOUND)
        # serializer = StreamPlatformSerializer(stream_platform,context={'request': request})
        serializer = BlogSerializer(blog)
        return Response(serializer.data)
    def put(self,request,pk):
        blog = Blog.objects.get(pk=pk)
        serializer = BlogSerializer(blog,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"Blog updated successfully",'updated_data':serializer.data},status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)
    def delete(self,request,pk):
        try:
            blog = Blog.objects.get(pk=pk)
        except Blog.DoesNotExist:
            return Response({'message':"With given id blog already deleted"},status=status.HTTP_404_NOT_FOUND)
        blog.delete()
        return Response({"message":"Blog deleted successfully"},status=status.HTTP_204_NO_CONTENT) 
    
    
class CategoryAV(APIView):
    permission_classes = [IsAdminOrReadOnly]
    def get(self, request):
        categories = Category.objects.all()
        # serializer = StreamPlatformSerializer(platform,many=True,context={'request': request})
        serializer = CategorySerializer(categories,many=True)
        return Response({"list_of_categories":serializer.data},status=status.HTTP_200_OK)
    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"Category object created successfully","created_object":serializer.data},status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)
        
class CategoryDetailAV(APIView):
    # permission_classes = [IsAdminOrReadOnly]
    def get(self, request, pk):
        try:
            category = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return Response({'message':"Category not found with given id"},status=status.HTTP_404_NOT_FOUND)
        # serializer = StreamPlatformSerializer(stream_platform,context={'request': request})
        serializer = CategorySerializer(category)
        return Response(serializer.data)
    def put(self,request,pk):
        try:
            category = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return Response({'message':"Category not found with given id"},status=status.HTTP_404_NOT_FOUND)
        serializer = CategorySerializer(category,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"Category updated successfully",'updated_data':serializer.data},status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)
    def delete(self,request,pk):
        try:
            category = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return Response({'message':"With given id category already deleted"},status=status.HTTP_404_NOT_FOUND)
        category.delete()
        return Response({"message":"Category deleted successfully"},status=status.HTTP_204_NO_CONTENT) 