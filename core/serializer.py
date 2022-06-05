from rest_framework.serializers import ModelSerializer

from .models import AuthToken, Users


class TokenSerializer(ModelSerializer):
    class Meta:
        model = AuthToken
        fields = '__all__'


class UserSerializer(ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__'


class UserDataSerializer(ModelSerializer):
    class Meta:
        model = Users
        fields = ['id', 'created_at', 'date_joined', 'fname', 'lname', 'username', 'user_role_id', 'logical_delete',
                  'status']
