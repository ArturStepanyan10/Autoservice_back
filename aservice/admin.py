# from django.contrib import admin
# from django.contrib.auth.hashers import make_password
#
# from .models import User, Service, Appointment, Car, Reviews
#
#
# @admin.register(Service)
# class ServiceAdmin(admin.ModelAdmin):
#     list_display = ('id', 'title', 'description')
#     list_display_links = ('title', )
#     ordering = ('id',)
#
#
# @admin.register(Appointment)
# class AppointmentAdmin(admin.ModelAdmin):
#     list_display = (
#         'id',
#         'user',
#         'date',
#         'time',
#         'status',
#         'service',
#         'worker',
#         'car',
#         'last_name',
#         'first_name')
#     ordering = ('-id',)
#     list_display_links = ('user', 'date', 'time', 'car')
#
#
# @admin.register(Reviews)
# class ReviewsAdmin(admin.ModelAdmin):
#     list_display = ('id', 'user', 'service', 'rating', 'content', 'is_published', 'created_at', 'updated_at')
#     ordering = ('-id',)
#     list_display_links = ('user', 'service',)
#
#
# @admin.register(User)
# class UserAdmin(admin.ModelAdmin):
#     list_display = ('email', 'first_name', 'last_name', 'role')
#
#     def get_queryset(self, request):
#         qs = super().get_queryset(request)
#         return qs.filter(role='ROLE_WORKER')
#
#     def save_model(self, request, obj, form, change):
#         if not change and obj.password:
#             obj.password = make_password(obj.password)
#             print(obj.password)
#         elif change:
#             orig = self.model.objects.get(id=obj.id)
#             if orig.password != obj.password:
#                 obj.password = make_password(obj.password)
#         super().save_model(request, obj, form, change)
#
#
# @admin.register(Car)
# class CarAdmin(admin.ModelAdmin):
#     list_display = ('id', 'brand', 'model', 'year', 'vin', 'photo')
#     list_display_links = ('brand', 'model')
#
#
