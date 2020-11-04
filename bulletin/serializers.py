from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    """User REST serializer
    """

    class Meta:
        """User REST serializer metadata
        """

        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'date_joined')
        read_only_fields = ('id',)
