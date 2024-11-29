from rest_framework import serializers

from aservice.models import User, Worker


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'first_name',
                  'last_name', 'role', 'phone_number']
        extra_kwargs = {
            'password': {'write_only': True},
            'role': {'read_only': True},
        }

    def create(self, validated_data):
        if 'role' not in validated_data:
            validated_data['role'] = 'ROLE_CLIENT'

        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class WorkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Worker
        fields = ['id', 'position', 'experience', 'specialization', 'user']

    user = UserSerializer()

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_data['role'] = 'ROLE_WORKER'
        user = UserSerializer().create(user_data)

        worker = Worker.objects.create(user=user, **validated_data)
        return worker


