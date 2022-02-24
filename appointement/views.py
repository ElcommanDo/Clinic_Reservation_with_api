from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from .models import Appointment, Reschedule, Notification
from accounts.models import Client
from django.contrib import messages
import datetime


def make_appointment(request):
    client = get_object_or_404(Client, user=request.user)

    if request.method == "POST":

        date = request.POST['date']
        client = Client.objects.get(user=request.user)
        if date < str(datetime.datetime.now()):
            messages.warning(request, 'date is incorrect.')
            return redirect('make_appointment')
        obj = Appointment(client=client, date=date)
        if Appointment.objects.filter(client=client, date=date, status='pending'):
            messages.warning(request, 'request done before.')
            return redirect('make_appointment')
        obj.save()
        messages.success(request, 'appointment is pending.')
        return redirect('home')

    return render(request, 'app/make_appointment.html', {'client': client})

# api created http://127.0.0.1:8000/api/appointments


def cancel_appointment(request, id):
    obj = get_object_or_404(Appointment, id=id)
    obj.status = 'canceled'
    obj.save()
    return redirect('profile')

# api created http://127.0.0.1:8000/api/appointments/{id}/cancel_appointment/


def reschedule_order(request, id):
    appointment = get_object_or_404(Appointment, id=id)
    res = Reschedule(app=appointment, new_date=request.POST.get('new_date'))
    res.waited = True
    res.save()
    messages.success(request, 'Your request send to Admin.')
    return redirect('profile')
# api created http://127.0.0.1:8000/api/reschedules/


def reschedule_accept(request, id):
    obj = get_object_or_404(Reschedule, id=id)
    obj.app.date = obj.new_date
    obj.app.rescheduled = True
    obj.accepted = True
    obj.waited = False
    obj.save()
    note = Notification(note='your reschedule is accepted', client=obj.app.client )
    note.save()

    messages.success(request, 'rescheduling done')
    return redirect('profile')
# api created http://127.0.0.1:8000/api/reschedules/{id}/accept_reschedule/


def reschedule_reject(request, id):
    obj = get_object_or_404(Reschedule, id=id)
    obj.accepted = False
    obj.waited = False
    obj.save()
    messages.success(request, 'rescheduling rejected')
    return redirect('profile')
# api created http://127.0.0.1:8000/api/reschedules/{id}/reject_reschedule/


def appointments(request):
    objs = Appointment.objects.all()
    context = {}
    if request.method == "POST":
        if request.POST.get('val') == "pending":
            objs = Appointment.objects.filter(status='pending')
            context['search'] = 'up'
        elif request.POST.get('val') == "all":
            objs = Appointment.objects.all()
            context['search'] = 'all'

        elif request.POST.get('val') == "closed":
            objs = Appointment.objects.filter(Q(status='finished') | Q(status='missed'))
            context['search'] = 'past'
    context['appointments'] = objs
    return render(request, 'app/appointments.html', context)
# api created http://127.0.0.1:8000/api/appointments/


def mark_as(request, id):
    note = Notification()
    obj = Appointment.objects.get(id=id)
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
    return redirect('appointments')
# api created http://127.0.0.1:8000/api/appointments/{id}/mark_as/

