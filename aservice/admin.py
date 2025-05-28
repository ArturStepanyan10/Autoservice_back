from django.contrib import admin
from django.contrib.auth.hashers import make_password

from .models import User, Service, Worker, Appointment, Car, Reviews, Specialization, Post


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description')
    list_display_links = ('title', )
    ordering = ('id',)


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'date',
        'time',
        'status',
        'worker',
        'car',
        'last_name',
        'first_name')
    ordering = ('-id',)
    list_display_links = ('user', 'date', 'time', 'car')


@admin.register(Reviews)
class ReviewsAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'service', 'rating', 'content', 'is_published', 'created_at', 'updated_at')
    ordering = ('-id',)
    list_display_links = ('user', 'service',)


@admin.register(Worker)
class WorkerAdmin(admin.ModelAdmin):
    list_display = ('id', 'position', 'specialization', 'get_last_name', 'get_first_name',
                    'get_email')

    def get_last_name(self, obj):
        return obj.user.last_name
    get_last_name.short_description = 'Фамилия'

    def get_first_name(self, obj):
        return obj.user.first_name
    get_first_name.short_description = 'Имя'

    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'E-mail'

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "user":
            kwargs["queryset"] = User.objects.filter(role="ROLE_WORKER")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'role')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(role='ROLE_WORKER')

    def save_model(self, request, obj, form, change):
        if not change and obj.password:
            obj.password = make_password(obj.password)
            print(obj.password)
        elif change:
            orig = self.model.objects.get(id=obj.id)
            if orig.password != obj.password:
                obj.password = make_password(obj.password)
        super().save_model(request, obj, form, change)


@admin.register(Specialization)
class SpecializationAdmin(admin.ModelAdmin):
    list_display = ('id', 'title',)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title',)


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('id', 'brand', 'model', 'year', 'vin', 'photo')
    list_display_links = ('brand', 'model')


