from django.contrib import admin

from .models import User, Service, Worker, Appointment, Car, Reviews


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'price')
    list_display_links = ('title', )
    ordering = ('id',)


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'date', 'time', 'service', 'status', 'worker', 'car', 'total_price')
    ordering = ('-id',)
    list_display_links = ('user', 'date', 'time')


@admin.register(Reviews)
class ReviewsAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'service', 'rating', 'content', 'is_published', 'created_at', 'updated_at')
    ordering = ('-id',)
    list_display_links = ('user', 'service',)


@admin.register(Worker)
class WorkerAdmin(admin.ModelAdmin):
    list_display = ('id', 'position', 'specialization', 'get_last_name', 'get_first_name',
                    'get_email', 'get_phone_number')

    def get_last_name(self, obj):
        return obj.user.last_name
    get_last_name.short_description = 'Фамилия'

    def get_first_name(self, obj):
        return obj.user.first_name
    get_first_name.short_description = 'Имя'

    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'E-mail'

    def get_phone_number(self, obj):
        return obj.user.phone_number
    get_phone_number.short_description = 'Номер телефона'

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





