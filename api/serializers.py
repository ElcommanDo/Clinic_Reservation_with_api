from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from accounts.models import Client
from django.contrib.auth.models import User
from appointement.models import Appointment, Reschedule, Notification


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(validators=[UniqueValidator(queryset=User.objects.all())])

    class Meta:
        model = User
        fields = ('id', "username", 'email', 'password')
        extra_kwargs = {"password": {"style": {'input_type': 'password'}, "write_only": True, "required": True}}

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class ClientSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Client
        fields = ('id', 'phone', 'address', 'user')

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        print(user_data)
        user = User.objects.create(**user_data)
        user.set_password(user_data['password'])
        user.save()
        client = Client.objects.create(user=user, **validated_data)
        client.save()
        return client


class AppointmentSerializer(serializers.ModelSerializer):
    client = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Appointment
        fields = "__all__"

    def create(self, validated_data):
        client = Client.objects.get(user=self.context['request'].user)
        app = Appointment(client=client, **validated_data)
        app.save()
        return app


class RescheduleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reschedule
        fields = ('id', "app", 'new_date', 'accepted', 'waited')


class NotificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notification
        fields = "__all__"

