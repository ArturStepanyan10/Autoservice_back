from django.contrib import admin

from .models import User, Service, Worker


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'first_name', 'last_name', 'role')
    list_display_links = ('username', )
    ordering = ('id', )


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'price')
    list_display_links = ('title', )


#@admin.register(Worker)
#class WorkerAdmin(admin.ModelAdmin):
    #list_display = ('id', 'first_name', 'last_name', 'email', 'position', 'specialization', 'experience', 'role')
    #list_display_links = ('last_name', )