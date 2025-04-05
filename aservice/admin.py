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
    list_display = ('id', 'position', 'specialization', 'user')



