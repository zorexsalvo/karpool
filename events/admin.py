from django.contrib import admin
from .models import Event, Car, Member


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['name', 'date', 'location', 'slug', 'created_at']
    list_filter = ['date', 'created_at']
    search_fields = ['name', 'location', 'slug']
    readonly_fields = ['slug', 'created_at']
    ordering = ['-created_at']


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'event', 'driver_name', 'capacity', 'created_at']
    list_filter = ['event', 'created_at']
    search_fields = ['driver_name', 'car_name', 'event__name']
    readonly_fields = ['created_at']
    ordering = ['-created_at']


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ['name', 'event', 'car', 'contact', 'created_at']
    list_filter = ['event', 'car', 'created_at']
    search_fields = ['name', 'contact', 'event__name']
    readonly_fields = ['created_at']
    ordering = ['-created_at']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('event', 'car')
