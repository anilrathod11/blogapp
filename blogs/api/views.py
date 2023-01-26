from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework import status
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly,IsAdminUser
from blogs.api.permissions import IsAdminOrReadOnly,IsReviewUserOrReadOnly
from rest_framework.views import APIView
from blogs.api.serializers import BlogSerializer, CategorySerializer,CommentSerializer,ImageSerializer
from blogs.models import Blog, Category,CommentOnBlog,ContentWriterPerformance,RandomPicture
from user_app.models import CustomeUser
from sub_plan_app.models import Subscription
# from blogs.api.send_mail import send_mail
from blogs.tasks import send_mail_func
from blogs.tasks import test_func

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
        try:
            user = CustomeUser.objects.get(pk=request.user.id)
            if user.role == "Author" or user.role == "Writer" or user.role == "Admin":
                request.data["author"] = request.user.id
                serializer = BlogSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response({"message":"Blog object created successfully","created_object":serializer.data},status=status.HTTP_201_CREATED)
                else:
                    return Response(serializer.errors)
            else:
                return Response({'message':"Only author and writer can post blog"},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message":e.args}, status=status.HTTP_400_BAD_REQUEST)

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
    
class AdminToAssignReviewer(APIView):
    permission_classes = [IsAdminUser]
    def put(self, request):
        try:
            blog = Blog.objects.get(pk=request.data["blog"])
        except Blog.DoesNotExist:
            return Response({'message':"Blog not found with given id"},status=status.HTTP_404_NOT_FOUND)
        try:
            user = CustomeUser.objects.get(pk=request.data["reviewer"])
        except Exception as e:
            # print(e)
            return Response({'message':"With given reviewer_id reviewer not present"},status=status.HTTP_400_BAD_REQUEST)   
        if user.role == "Reviewer":
            blog.reviewer = user
            blog.status = request.data["status"]
            blog.save()
            serializer = BlogSerializer(blog)
            message='Hi, Admin this side, I am going to add blog for review to you please check it!'
            mail_subject='Blog to review'
            send_mail_func.delay(message,mail_subject,
                                user.email)
            # send_mail(html="",text='Hi, Admin this side, I am going to add blog for review to you please check it!',subject='Blog to review',from_email='anil.pune11@gmail.com',to_emails=['rathodanil6512@gmail.com'])
            return Response({"message":"Blog assign to reviewer successfull","updated_data":serializer.data},status=status.HTTP_200_OK)
        else:
            return Response({'message':"Invalid Reviewer"},status=status.HTTP_400_BAD_REQUEST)
    
class ReviewerAV(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        try:
            user = CustomeUser.objects.get(pk=request.user.id)
        except CustomeUser.DoesNotExist():
            return Response({'message':"Only authenticated user can access this resources"},status=status.HTTP_400_BAD_REQUEST)
        if user.role == "Reviewer":
            blogs = Blog.objects.filter(reviewer=user)
            serializer = BlogSerializer(blogs,many=True)
            return Response({"list_of_blog_to_review":serializer.data},status=status.HTTP_200_OK)
        else:
            return Response({'message':"Only Reviewer can access this resource"}, status=status.HTTP_400_BAD_REQUEST)
class CommentAV(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        if request.user.role == "Reviewer" or request.user.role == "Author":
            comments = CommentOnBlog.objects.filter(commented_by=request.user)
            serializer = CommentSerializer(comments,many=True)
            return Response({"list_of_comment":serializer.data},status=status.HTTP_200_OK)
        else:
            return Response({"message":"Only reviewer and author can see all comments"},status=status.HTTP_400_BAD_REQUEST)
    def post(self, request):
        if request.user.role == "Reviewer" or request.user.role == "Author" or request.user.role == "Admin":
            try:
                blog = Blog.objects.get(pk=request.data["blog_id"])
            except Blog.DoesNotExist():
                return Response({'message':"With given blog_id blog not found"},status=status.HTTP_404_NOT_FOUND)
            request.data['commented_by'] = request.user.id
            request.data['blog'] = blog.id
            serializer = CommentSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                blog.status = request.data["status"]
                blog.save()
                return Response({"message":"Comment on blog is created successfully","created_object":serializer.data},status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors)
        else:
            return Response({'message':"Only admin, reviewer and author can comment on blog"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET",])
@permission_classes([IsAuthenticated])
def author_blog_comment(request,pk):
    try:
        blog = Blog.objects.get(pk=pk)
    except Blog.DoesNotExist():
        return Response({"message":"Blog not found with given blog id"}, status=status.HTTP_404_NOT_FOUND)
    if request.method == "GET" and request.user.role == "Author":
        try:
            blog_comment = CommentOnBlog.objects.filter(blog=blog)
        except CommentOnBlog.DoesNotExist():
            return Response({"message":"with blog id comment notg present"},status=status.HTTP_404_NOT_FOUND)
        serializer = CommentSerializer(blog_comment,many=True)
        return Response({"list_of_comment_on_blog":serializer.data},status=status.HTTP_200_OK)
    else:
        return Response({"message":"Only author can access this resource"},status=status.HTTP_400_BAD_REQUEST)
        
        
class UploadPicture(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        image_object = RandomPicture.objects.all()
        # serializer = StreamPlatformSerializer(platform,many=True,context={'request': request})
        serializer = ImageSerializer(image_object,many=True)
        return Response({"list_of_image":serializer.data},status=status.HTTP_200_OK)
    def post(self, request):
        serializer = ImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"Image object created successfully","created_object":serializer.data},status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)
        
@api_view(["GET",])
@permission_classes([IsAuthenticated])
def get_active_blog(request):
    try:
        sub_validity = Subscription.objects.get(user=request.user)
    # except Subscription.DoesNotExist():
    except Exception as e:
        return Response({"message":"You are not prime member, pls buy subscription or you can continue with our public blogs"}, status=status.HTTP_404_NOT_FOUND)
    if request.method == "GET":
        if (sub_validity.archive != True or sub_validity.free_trail == True):
            active_blog = Blog.objects.filter(status="Active")
            serializer = BlogSerializer(active_blog,many=True)
            return Response({"list_of_active_blog":serializer.data},status=status.HTTP_200_OK)
        else:
            return Response({"message":"Subscription Expired!"},status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"message":"Only reader can read active blog"},status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET',])
@permission_classes([IsAuthenticated])
def get_public_active_blog(request):
    try:
        public_blog = Blog.objects.filter(status="Active",public=True)
    except Blog.DoesNotExist():
        return Response({'message':"Public Active blog does not exit"}, status=status.HTTP_404_NOT_FOUND)
    serializer = BlogSerializer(public_blog,many=True)
    return Response({'public_active_blog':serializer.data}, status=status.HTTP_200_OK)
        
# @api_view(["GET",])
# @permission_classes([IsAuthenticated])
# def free_trail(request):