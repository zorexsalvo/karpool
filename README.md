# Carpool Management App

A Django-based web application for organizing and managing carpool events. No user accounts required - access is granted through unique, shareable event links.

## 🚗 Features

### Core Functionality
- **Create Events**: Simple form to create carpool events with optional date and location
- **Unique Shareable Links**: Each event gets a unique slug for public access
- **Car Management**: Add cars with driver info, capacity, and notes
- **Member Management**: Join events, assign to cars, or remain unassigned
- **Real-time Updates**: Add, remove, and reassign members and cars instantly

### Access Control
- **No Login Required**: Access is controlled solely by the unique event URL
- **Public Sharing**: Anyone with the event link can participate
- **Simple Coordination**: Perfect for teams, groups, and organizations

## 🛠 Tech Stack

- **Backend**: Django 5.2.7
- **Database**: SQLite (development)
- **Frontend**: Bootstrap 5, HTML5, JavaScript
- **Icons**: Bootstrap Icons
- **Package Manager**: uv

## 📋 Requirements

- Python 3.11+
- uv package manager

## 🚀 Quick Start

### Option 1: Docker (Recommended)

#### Prerequisites
- Docker and Docker Compose installed

#### 1. Clone and Build
```bash
git clone <repository-url>
cd carpool
make build
```

#### 2. Start the Application
```bash
make up
```

#### 3. Access the Application
- **Main App**: http://localhost:8000/
- **Admin Interface**: http://localhost:8000/admin/

#### Docker Commands
```bash
make up          # Start the application
make up-d        # Start in background
make down        # Stop the application
make logs        # View logs
make shell       # Open shell in container
make migrate     # Run migrations
make clean       # Clean up containers and volumes
make help        # Show all available commands
```

### Option 2: Local Development

#### Prerequisites
- Python 3.11+
- uv package manager

#### 1. Clone and Setup
```bash
git clone <repository-url>
cd carpool
```

#### 2. Install Dependencies
```bash
uv add django
```

#### 3. Database Setup
```bash
source .venv/bin/activate
python manage.py migrate
python manage.py createsuperuser  # Optional: for admin access
```

#### 4. Run Development Server
```bash
python manage.py runserver 8000
```

#### 5. Access the Application
- **Main App**: http://127.0.0.1:8000/
- **Admin Interface**: http://127.0.0.1:8000/admin/ (if superuser created)

## 📖 Usage

### Creating an Event
1. Visit the home page
2. Fill in the event name (required), date (optional), and location (optional)
3. Click "Create Event" to generate a unique shareable link

### Managing a Carpool Event
1. Share the unique event link with participants
2. **Add Cars**: Use the "Add Car" button to register vehicles with capacity info
3. **Join Event**: Use the "Join Event" form to add participants
4. **Assign Members**: Members can choose a car when joining or be assigned later
5. **Manage Assignments**: Use the arrow buttons to reassign members between cars
6. **Track Capacity**: Visual indicators show available seats in each car

### Key Features in Use
- **Copy Link Button**: One-click copying of the shareable event URL
- **Real-time Capacity**: Shows occupied/available seats for each car
- **Flexible Assignment**: Members can be unassigned, then assigned to cars later
- **Quick Actions**: Delete cars/members with confirmation prompts

## 🗂 Project Structure

```
carpool/
├── carpool_project/          # Django project settings
│   ├── __init__.py
│   ├── settings.py          # Django configuration
│   ├── urls.py              # Main URL routing
│   └── wsgi.py
├── events/                   # Main Django app
│   ├── migrations/          # Database migrations
│   ├── templates/events/    # App templates
│   ├── admin.py            # Admin interface config
│   ├── forms.py            # Django forms
│   ├── models.py           # Data models (Event, Car, Member)
│   ├── urls.py             # App URL routing
│   └── views.py            # Application logic
├── templates/               # Shared templates
│   └── base.html           # Base template with Bootstrap
├── manage.py               # Django management script
├── db.sqlite3             # SQLite database (created after migrations)
└── spec.md                # Original specification
```

## 🎯 Data Models

### Event
- `name`: Event title (required)
- `date`: Event date (optional)
- `location`: Event location (optional)
- `slug`: Unique identifier for URL access (auto-generated)

### Car
- `driver_name`: Driver's name (required)
- `car_name`: Optional car label/name
- `capacity`: Number of available seats (optional)
- `notes`: Additional information (optional)
- `event`: Foreign key to Event

### Member
- `name`: Participant's name (required)
- `contact`: Contact information (optional)
- `car`: Assignment to a specific car (optional)
- `event`: Foreign key to Event

## 🔄 URL Structure

- `/` - Home page (event creation)
- `/event/<slug>/` - Event dashboard
- `/event/<slug>/add-car/` - Add car (POST)
- `/event/<slug>/add-member/` - Add member (POST)  
- `/event/<slug>/member/<id>/update/` - Update member assignment (POST)
- `/event/<slug>/member/<id>/delete/` - Delete member (POST)
- `/event/<slug>/car/<id>/delete/` - Delete car (POST)

## 🎨 UI/UX Features

- **Responsive Design**: Mobile-friendly Bootstrap layout
- **Visual Feedback**: Success/error messages for all actions
- **Intuitive Icons**: Clear visual indicators for different actions
- **Modal Forms**: Clean popup forms for adding cars
- **Confirmation Dialogs**: Prevent accidental deletions
- **Copy-to-Clipboard**: Easy sharing of event links
- **Real-time Updates**: Immediate reflection of changes

## 🔧 Development

### Running Tests
```bash
python manage.py test
```

### Admin Interface
Access the admin at `/admin/` with superuser credentials to:
- Manage events, cars, and members
- View all data across events
- Perform bulk operations

### Database Management
```bash
python manage.py makemigrations  # Create new migrations
python manage.py migrate        # Apply migrations
python manage.py shell         # Django shell for debugging
```

## 📝 Implementation Notes

- **Security**: CSRF protection enabled for all forms
- **Database**: Uses Django ORM with SQLite for simplicity
- **Frontend**: No JavaScript framework - vanilla JS for enhanced UX
- **Validation**: Both client-side and server-side form validation
- **Error Handling**: Comprehensive error messages and user feedback

## 🚀 Future Enhancements

- Password-protected event access
- Email notifications for participants
- Export functionality (CSV, PDF)
- Event editing capabilities
- Mobile app version
- Integration with mapping services

## 📄 License

This project is built as per the specifications in `spec.md` and is ready for internal team use.