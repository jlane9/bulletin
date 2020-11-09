from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    """User REST serializer
    """

    password = serializers.CharField(write_only=True)

    def create(self, validated_data: dict):
        """Create new user
        """

        user = User.objects.create(username=validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()

        return user

    class Meta:
        """User REST serializer metadata
        """

        model = User
        fields = ('id', 'username', 'password', 'first_name', 'last_name', 'email', 'date_joined')
        read_only_fields = ('id',)
