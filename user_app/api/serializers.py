from rest_framework import serializers
from user_app.models import CustomeUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomeUser
        fields = ["id","username","email","role"]
        read_only_fields = ['id']

class RegistrationSerializer(serializers.ModelSerializer):
    password_confirmation = serializers.CharField(style={'input_type':"password"},write_only=True)
    class Meta:
        model = CustomeUser
        fields = '__all__'
        
    def save(self,data):
        # print("Anil Rathod")
        password = self.validated_data['password']
        password_confirmation = self.validated_data['password_confirmation']
        if password != password_confirmation:
            raise serializers.ValidationError({'errors':"Password and password confirmation should be same!"})
        if CustomeUser.objects.filter(email=self.validated_data["email"]).exists():
            raise serializers.ValidationError({'errors':"Email already exit!"})
        # print(self.validated_data)
        account = CustomeUser(email=self.validated_data['email'],username=self.validated_data['username'],
                              role = self.validated_data['role'],date_of_birth = self.validated_data['date_of_birth'])
        # account = CustomeUser.objects.create(data)
        # print(account)
        account.set_password(password)
        account.save()
        return account