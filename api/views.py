from rest_framework import viewsets
from .serializers import ClientSerializer, AppointmentSerializer,\
    RescheduleSerializer, NotificationSerializer, UserSerializer
from accounts.models import Client, User
from appointement.models import Appointment, Reschedule, Notification
from rest_framework.decorators import action
from rest_framework.response import Response


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer



class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer

    @action(detail=True, methods=['POST', 'GET'])
    def cancel_appointment(self, request, pk=None):
        query = Appointment.objects.get(pk=pk)
        query.status = 'canceled'
        query.save()
        return Response({'status': 'canceled done'})


class RescheduleViewSet(viewsets.ModelViewSet):
    queryset = Reschedule.objects.all()
    serializer_class = RescheduleSerializer

    def perform_create(self, serializer):
        serializer.save(waited=True)

    @action(detail=True, methods=['POST', 'GET'])
    def accept_reschedule(self, request, pk=None):
        query = Reschedule.objects.get(pk=pk)
        query.accepted = True
        query.app.rescheduled = True
        query.app.date = query.new_date
        query.waited = False
        query.save()
        notification = Notification(note='rescheduling is done', client = query.app.client)
        notification.save()
        return Response({'status': 'rescheduling done'})

    @action(detail=True, methods=['POST', 'GET'])
    def reject_reschedule(self, request, pk=None):
        query = Reschedule.objects.get(pk=pk)
        query.accepted = False
        query.waited = False
        notification = Notification(note='rescheduling is rejected', client=query.app.client)
        notification.save()
        query.save()
        return Response({'status': 'rescheduling rejected'})

    @action(detail=True, methods=['POST'])
    def mark_as(self, request, pk=None):
        note = Notification()
        obj = Appointment.objects.get(pk=pk)
        note.client = obj.client
        if request.POST.get('vale') == "missed":
            obj.mark_as_missed = True
            obj.status = 'missed'
            obj.save()
            note.note = 'Your request is missed.'
        elif request.POST.get('vale') == "approved":
            obj.approved = True
            obj.status = 'approved'
            obj.save()
            note.note = 'Your request is approved.'
        elif request.POST.get('vale') == "finished":
            obj.mark_as_finished = True
            obj.status = 'finished'
            obj.save()
            note.note = 'Your request is finished.'
        note.save()
        return Response({'status': 'action done'})


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
