"""bookinder_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from bookinder import views

from django.conf.urls import url, include
from rest_framework import routers
from rest_framework.authtoken import views as authtoken_view

router = routers.DefaultRouter()
router.register(r'users_profiles', views.UserProfileViewSet)
router.register(r'users', views.UserViewSet)
router.register(r'books', views.BookViewSet)
router.register(r'library', views.LibraryViewSet, base_name="library")
router.register(r'matches', views.MatchViewSet, base_name="matches")
router.register(r'matches_read', views.MatchReadViewSet,
                base_name="matches_read")
router.register(r'create_matches', views.CreateMatches,
                base_name="create_matches")

urlpatterns = [
    url(r'^', include(router.urls), name='home'),
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
    url(r'^api-token-auth/', authtoken_view.obtain_auth_token)
]


