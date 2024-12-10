
from django.urls import path
from django.views.generic import TemplateView
from .views import CustomTokenObtainPairView
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('login/', CustomTokenObtainPairView.as_view(), name='login'),
    path('refresh/', jwt_views.TokenRefreshView.as_view(), name='refresh'),
    path('', TemplateView.as_view(template_name="core/index.html"))
    

]

