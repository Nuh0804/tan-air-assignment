from djoser.serializers import UserCreateSerializer, UserSerializer
   

class UserCreaterSerializer(UserCreateSerializer):
   class Meta(UserCreateSerializer.Meta):
      fields = ['id', 'username', 'password', 'email', 'first_name', 'last_name']

class CurrentUserSerializer(UserSerializer):
   class Meta(UserSerializer.Meta):
      fields = ['email', 'id', 'username','first_name', 'last_name']
      

