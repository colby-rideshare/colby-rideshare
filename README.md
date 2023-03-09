# Colby Rideshare

Colby Rideshare is a web application designed to help members of the Colby community find rides to and from campus. The app is built using Django and Bootstrap and is deployed to Heroku under the domain https://www.colbyrideshare.live.

## Features

- User registration and login
- User profile management
- Ride creation and management
- Ride search and filtering
- Email notifications for ride requests and updates
- Google Maps Directions integration for location and route display
- Google Place Autocomplete integration for location input
- AWS S3 for image storage

## Technologies Used

- Front-end: Bootstrap, HTML, CSS, JavaScript
- Back-end: Django
- Database: PostgreSQL
- Deployment: Heroku
- Email Service: Gmail
- Map Service: Google Maps
- Image Storage: AWS S3
- Analytics Tracking: PostHog

## Getting Started

To run the app locally, follow these steps:

1. Clone the repository

```git clone https://github.com/max-duchesne/carpool-app.git```

2. Install dependencies

```pip install -r requirements.txt```

3. Create an admin user

```python manage.py createsuperuser```

4. Run the local server

```python manage.py runserver```

5. Open app in browser

That's it! You can now open the app by visiting http://localhost:8000/ in your browser
