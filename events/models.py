from django.db import models
from django.utils.text import slugify
import uuid


class Event(models.Model):
    """Event model for carpool events."""
    name = models.CharField(max_length=200, help_text="Event title")
    date = models.DateField(null=True, blank=True, help_text="Event date")
    location = models.CharField(max_length=500, blank=True, help_text="Event location")
    slug = models.SlugField(unique=True, max_length=50, help_text="Unique slug for public access")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            # Generate a unique slug
            base_slug = slugify(self.name)[:40]  # Limit base slug length
            unique_slug = f"{base_slug}-{uuid.uuid4().hex[:8]}"
            self.slug = unique_slug
        super().save(*args, **kwargs)


class Car(models.Model):
    """Car model for each carpool vehicle."""
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='cars')
    driver_name = models.CharField(max_length=100, help_text="Driver's name")
    car_name = models.CharField(max_length=100, blank=True, help_text="Car name/label")
    capacity = models.PositiveIntegerField(null=True, blank=True, help_text="Number of seats available")
    notes = models.TextField(blank=True, help_text="Additional notes")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        car_display = f"{self.driver_name}'s car"
        if self.car_name:
            car_display += f" ({self.car_name})"
        return car_display
    
    @property
    def available_spots(self):
        """Calculate available spots in the car."""
        if self.capacity is None:
            return None
        current_members = self.members.count()
        return max(0, self.capacity - current_members)


class Member(models.Model):
    """Member model for carpool participants."""
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='members')
    name = models.CharField(max_length=100, help_text="Member's name")
    contact = models.CharField(max_length=200, blank=True, help_text="Contact information (optional)")
    car = models.ForeignKey(Car, on_delete=models.SET_NULL, null=True, blank=True, related_name='members', help_text="Assigned car")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['created_at']
        unique_together = ['event', 'name']  # Prevent duplicate names in same event
    
    def __str__(self):
        return self.name
    
    @property
    def is_unassigned(self):
        """Check if member is unassigned to any car."""
        return self.car is None
