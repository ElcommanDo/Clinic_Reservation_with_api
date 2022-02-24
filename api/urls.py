from django.urls import path, include
from . import views
from rest_framework import routers
router = routers.DefaultRouter()
router.register('clients', views.ClientViewSet)
router.register('appointments', views.AppointmentViewSet)
router.register('reschedules', views.RescheduleViewSet)
router.register('notifications', views.NotificationViewSet)
router.register('users', views.UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
