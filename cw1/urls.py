from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from cw1app import views

# set up routers
router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'professors', views.ProfessorViewSet)
router.register(r'modules', views.ModuleViewSet)
router.register(r'moduleinstances', views.ModuleInstanceViewSet)
router.register(r'ratings', views.RatingViewSet)

# wire API together using routers, with additional routes for authentication
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('', include('cw1app.urls')),
    path('', views.api_root),
    path('user-login', views.user_login),
    path('user-logout', views.user_logout),
    path("admin/", admin.site.urls),
]