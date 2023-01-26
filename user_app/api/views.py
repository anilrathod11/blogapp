from rest_framework.decorators import api_view,permission_classes
from user_app.api.serializers import RegistrationSerializer,UserSerializer
from rest_framework.response import Response
from rest_framework import status
# from watchlist_app.api.permissions import IsAdminOrReadOnly, IsReviewUserOrReadOnly
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly,IsAdminUser
from rest_framework.authtoken.models import Token
from user_app.models import CustomeUser
# from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.authtoken.views import ObtainAuthToken

class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                       context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        print(request.data)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'role': user.role
        })

@api_view(['POST',])
def logout_view(request):
    if request.method == "POST":
        request.user.auth_token.delete()
        return Response({'message':"User logout successfully"},status=status.HTTP_200_OK)
    
    
@api_view(['POST',])
# @permission_classes([IsAdminOrReadOnly])
def registration_view(request):
    if request.method == "POST":
        serializer = RegistrationSerializer(data=request.data)
        # print(request.data)
        # print(type(request.data))
        data = {}
        if serializer.is_valid():
            account = serializer.save(request.data)
            data['username'] = account.username
            data['email'] = account.email
            # refresh = RefreshToken.for_user(account)
            # data["token"] = {'refresh': str(refresh),'access': str(refresh.access_token)}
            data['token'] = Token.objects.get(user=account).key
            return Response(data,status=status.HTTP_201_CREATED)
        else:
            data = serializer.errors
        return Response(data,status=status.HTTP_400_BAD_REQUEST) 
    
@api_view(['GET',])
@permission_classes((IsAdminUser,))
def user_list_view(request):
    if request.method == "GET":
        users = CustomeUser.objects.all()
        # serializer = StreamPlatformSerializer(platform,many=True,context={'request': request})
        serializer = UserSerializer(users,many=True)
        return Response({"list_of_users":serializer.data},status=status.HTTP_200_OK)
    else:
        return Response({'errors':serializer.errors},status=status.HTTP_404_NOT_FOUND)