# Carpool Management App — Specification

## Overview
The **Carpool Management App** is an internal web-based tool built using **Django**.  
It allows teams or groups to create and manage carpool events through a public, shareable link (unique slug).  
There are no user accounts or logins; access is granted through the event’s unique URL.

## Objectives
- Simplify coordination for carpools to events.
- Allow anyone with the event link to view, add, or modify entries.
- Avoid authentication complexity — the unique slug serves as the key to access.

## Core Features

### 1. Create Event
- Form fields:
  - **Event name** (string)
  - **Date** (optional)
  - **Location** (optional)
- On creation:
  - Generate a **unique slug** for public access (e.g., `/event/{slug}`)
- Redirect to the public event page after creation.

### 2. Add Cars
- Each car belongs to a specific event.
- Fields:
  - **Driver name**
  - **Car name / label**
  - **Capacity**
  - **Notes** (optional)
- Cars are displayed in a list on the event page.

### 3. Add Members
- Members can join a car or list themselves as **unassigned**.
- Fields:
  - **Name**
  - **Contact (optional)**
  - **Linked car** (foreign key, nullable)
- A member can be linked to a car (self-join) or remain unassigned.


## Access Control
- There is **no login system**.
- Access is determined **solely by the unique event slug**.
- Anyone with the event link can:
  - View the event details.
  - Add, edit, or delete cars and members.


## Data Model

### Event
| Field | Type | Notes |
|-------|------|-------|
| id | AutoField | Primary key |
| name | CharField | Event title |
| date | DateField | Optional |
| location | CharField | Optional |
| slug | SlugField | Unique, used for public access |

### Car
| Field | Type | Notes |
|-------|------|-------|
| id | AutoField | Primary key |
| event | ForeignKey(Event) | Cascade delete |
| driver_name | CharField | Required |
| car_name | CharField | Optional label |
| capacity | IntegerField | Optional |
| notes | TextField | Optional |

### Member
| Field | Type | Notes |
|-------|------|-------|
| id | AutoField | Primary key |
| event | ForeignKey(Event) | Cascade delete |
| name | CharField | Required |
| contact | CharField | Optional |
| car | ForeignKey(Car, nullable=True) | Member assigned to a car |
| joined_member | ForeignKey('self', nullable=True) | Optional self-join for grouping (if needed) |

## Views / Pages

### `/`
- Event creation form.
- Displays link to the newly created event after submission.

### `/event/<slug>/`
- Public event dashboard.
- Lists:
  - Event details (name, date, location)
  - Cars and their members
  - Unassigned members
- Includes forms to:
  - Add a car
  - Add a member
  - Reassign or remove a member

## Behavior & Constraints
- No authentication or sessions.
- All updates happen directly through POST forms.
- Validation occurs client-side and server-side.
- SQLite will be used for simplicity.


## Tech Stack
- **Backend:** Django 5.x
- **Database:** SQLite
- **Frontend:** HTML + Alpine.js (optional for interactivity)
- **Deployment:** Local or internal server (e.g., runserver / Docker)


## Future Enhancements (Optional)
- Editable event details.
- Password-protected slug.
- Email invites to participants.
- Export carpool list (CSV/PDF).


