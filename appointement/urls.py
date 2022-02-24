from django.urls import path
from . import views

urlpatterns = [
  path('make-appointment/', views.make_appointment, name='make_appointment'),
  path('show-appointments/', views.appointments, name='appointments'),
  path('cancel_appointment/<int:id>/', views.cancel_appointment, name='cancel_appointment'),
  path('reschedule_order/<int:id>/', views.reschedule_order, name='reschedule_order'),
  path('reschedule_accept/<int:id>/', views.reschedule_accept, name='approve_reschedule'),
  path('reschedule_reject/<int:id>/', views.reschedule_reject, name='cancel_reschedule'),
  path('mark-appointment/<int:id>/', views.mark_as, name='mark_as'),

]
