"""bulletin URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions, routers
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token
from bulletin import __author__, __email__, __version__, views
from message import views as message_views


admin.site.site_header = 'Bulletin Board Admin'

# pylint: disable=invalid-name
schema_view = get_schema_view(
    openapi.Info(
        title="Bulletin API",
        default_version='v' + __version__,
        description="Chat service API",
        contact=openapi.Contact(name=__author__, email=__email__)
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

router = routers.DefaultRouter()
router.register('users', views.UserViewSet)
router.register('messages', message_views.MessageViewSet)
router.register('topics', message_views.TopicViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api-token-auth/', obtain_jwt_token, name='jwt-auth'),
    path('api-token-refresh/', refresh_jwt_token, name='jwt-refresh'),
    path('docs/', schema_view.with_ui('redoc', cache_timeout=0), name='redocs'),
    re_path(r'swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger_ui')
]
