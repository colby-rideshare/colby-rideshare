# Colby Rideshare

Colby Rideshare is a web-based application that helps Colby students find rides to and from campus. The app is built using Django and Bootstrap and is deployed to Heroku with the domain www.colbyrideshare.live.

## Features

- User registration and login
- User profile management
- Ride creation and management
- Ride search and filtering
- Google Maps integration for location search
- Email notifications for ride requests and updates
- AWS S3 integration for image storage
- Analytics tracking with PostHog

## Technologies Used

- Front-end: Bootstrap, HTML, CSS, JavaScript
- Back-end: Django, Python
- Database: PostgreSQL
- Deployment: Heroku
- Email Service: Gmail
- Map Service: Google Maps
- Image Storage: AWS S3
- Analytics Tracking: PostHog

## Getting Started

To run the app locally, follow these steps:

### Prerequisites

- Python 3.9 or higher
- Django 4.0 or higher

### Installation

1. Clone the repository

git clone https://github.com/max-duchesne/carpool-app.git

2. Install dependencies

cd carpool-app
pip install -r requirements.txt

3. Create an admin user

python manage.py createsuperuser

4. Run the local server

python manage.py runserver

That's it! You can now open the app by visiting http://localhost:8000/ in your browser
