from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from .models import Event, Car, Member
from .forms import EventCreateForm, CarCreateForm, MemberCreateForm, MemberUpdateForm
import qrcode
from io import BytesIO


def home(request):
    """Home page with event creation form."""
    if request.method == 'POST':
        form = EventCreateForm(request.POST)
        if form.is_valid():
            event = form.save()
            messages.success(request, f'Event "{event.name}" created successfully!')
            return redirect('event_detail', slug=event.slug)
    else:
        form = EventCreateForm()
    
    return render(request, 'events/home.html', {'form': form})


def event_detail(request, slug):
    """Public event dashboard page."""
    event = get_object_or_404(Event, slug=slug)
    
    # Get cars with their members
    cars_queryset = Car.objects.filter(event=event).prefetch_related('members')
    
    # Sort cars: Cars first, then motorcycles with members, then motorcycles without members
    cars = sorted(
        cars_queryset,
        key=lambda car: (
            0 if (car.car_name or '').lower() != 'motorcycle' else (1 if car.members.count() > 0 else 2)
        )
    )
    
    # Get unassigned members
    unassigned_members = Member.objects.filter(event=event, car__isnull=True)
    
    # Count cars and motorcycles
    car_count = sum(1 for car in cars if (car.car_name or '').lower() != 'motorcycle')
    motorcycle_count = sum(1 for car in cars if (car.car_name or '').lower() == 'motorcycle')
    
    # Forms for adding new cars and members
    car_form = CarCreateForm()
    member_form = MemberCreateForm(event=event)
    
    context = {
        'event': event,
        'cars': cars,
        'unassigned_members': unassigned_members,
        'car_count': car_count,
        'motorcycle_count': motorcycle_count,
        'car_form': car_form,
        'member_form': member_form,
    }
    
    return render(request, 'events/event_detail.html', context)


def add_car(request, slug):
    """Add a car to an event."""
    event = get_object_or_404(Event, slug=slug)
    
    if request.method == 'POST':
        form = CarCreateForm(request.POST)
        if form.is_valid():
            car = form.save(commit=False)
            car.event = event
            car.save()
            messages.success(request, f'Car "{car}" added successfully!')
        else:
            messages.error(request, 'Please correct the errors below.')
    
    return redirect('event_detail', slug=slug)


def add_member(request, slug):
    """Add a member to an event."""
    event = get_object_or_404(Event, slug=slug)
    
    if request.method == 'POST':
        form = MemberCreateForm(request.POST, event=event)
        if form.is_valid():
            try:
                member = form.save(commit=False)
                member.event = event
                member.save()
                car_info = f" to {member.car}" if member.car else " as unassigned"
                messages.success(request, f'Member "{member.name}" added{car_info}!')
            except Exception as e:
                if 'UNIQUE constraint failed' in str(e):
                    messages.error(request, f'A member named "{form.cleaned_data["name"]}" already exists in this event.')
                else:
                    messages.error(request, 'An error occurred while adding the member.')
        else:
            messages.error(request, 'Please correct the errors below.')
    
    return redirect('event_detail', slug=slug)


def update_member(request, slug, member_id):
    """Update a member's car assignment."""
    event = get_object_or_404(Event, slug=slug)
    member = get_object_or_404(Member, id=member_id, event=event)
    
    if request.method == 'POST':
        form = MemberUpdateForm(request.POST, instance=member, event=event)
        if form.is_valid():
            old_car = member.car
            form.save()
            new_car = member.car
            
            if old_car != new_car:
                if new_car:
                    messages.success(request, f'"{member.name}" moved to {new_car}!')
                else:
                    messages.success(request, f'"{member.name}" is now unassigned!')
        else:
            messages.error(request, 'Please correct the errors below.')
    
    return redirect('event_detail', slug=slug)


def delete_member(request, slug, member_id):
    """Delete a member from an event."""
    event = get_object_or_404(Event, slug=slug)
    member = get_object_or_404(Member, id=member_id, event=event)
    
    if request.method == 'POST':
        member_name = member.name
        member.delete()
        messages.success(request, f'Member "{member_name}" removed from the event.')
    
    return redirect('event_detail', slug=slug)


def delete_car(request, slug, car_id):
    """Delete a car from an event."""
    event = get_object_or_404(Event, slug=slug)
    car = get_object_or_404(Car, id=car_id, event=event)
    
    if request.method == 'POST':
        car_name = str(car)
        # Members in this car will be unassigned automatically (SET_NULL)
        car.delete()
        messages.success(request, f'Car "{car_name}" removed from the event. Members were moved to unassigned.')
    
    return redirect('event_detail', slug=slug)


def event_qr(request, slug):
    """Generate QR code for the event URL."""
    event = get_object_or_404(Event, slug=slug)
    
    # Build the absolute URL for the event
    event_url = request.build_absolute_uri(reverse('event_detail', kwargs={'slug': slug}))
    
    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(event_url)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Save to BytesIO buffer
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    
    return HttpResponse(buffer, content_type='image/png')
