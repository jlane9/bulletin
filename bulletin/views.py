from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from bulletin import serializers


class UserPermissions(IsAuthenticated):
    """Permissions specific to the user model
    """

    def has_permission(self, request: Request, view: viewsets.ModelViewSet):
        """

        :param Request request: HTTP request
        :param viewsets.ModelViewSet view: User REST view
        :return:
        """

        # Allow non-authenticated users the ability to signup
        if request.method == 'POST':
            return True

        elif request.method in ('DELETE', 'PATCH', 'PUT'):

            if 'pk' in view.kwargs:
                return view.kwargs['pk'] == request.user.id
            elif 'id' in view.kwargs:
                return view.kwargs['id'] == request.user.id
            else:
                return False

        return bool(request.user and request.user.is_authenticated)


class UserViewSet(viewsets.ModelViewSet):
    """User REST view
    """

    queryset = User.objects.filter(is_active=True)
    serializer_class = serializers.UserSerializer
    permission_classes = [UserPermissions]
