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

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic.base import RedirectView
from django.urls import include, path, reverse_lazy
from rest_framework import routers
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token
from bulletin import views
from message import views as message_views


admin.site.site_header = 'Bulletin Board Admin'

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
    path('health/', include('health_check.urls', namespace='health_check')),
    path('', RedirectView.as_view(url=reverse_lazy('admin:index')))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
