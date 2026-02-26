# Nepal Trekking Portal

A comprehensive web application for trekking and travel in Nepal, built with Flask and Bootstrap.

## Features

- User registration and authentication
- Browse trekking packages
- Filter treks by region and difficulty
- Book trekking packages
- User dashboard to manage bookings
- Responsive design for all devices
- Contact form

## Technologies Used

- **Backend**: Python Flask
- **Database**: SQLite with SQLAlchemy ORM
- **Frontend**: HTML5, CSS3, Bootstrap 5
- **JavaScript**: jQuery, Custom JS
- **Version Control**: Git

## Installation

1. Clone the repository:
bash
git clone https://github.com/arunatamang0201-droid/nepal-trekking-portal.git
cd nepal-trekking-portal

2. Create a virtual environment

Windows:

bash
python -m venv venv
venv\Scripts\activate

Mac/Linux:

bash
python3 -m venv venv
source venv/bin/activate

3. Install required packages

bash
pip install -r requirements.txt

4. Initialize the database

bash
flask init-db

5. Run the application

bash
python app.py

6. Open your browser and go to:

text
http://127.0.0.1:5000

# How to Use

## For Visitors
1. Browse all trekking and travel packages without logging in

2. Use filters to find packages by region, difficulty, or type

3. View detailed information about each package

## For Registered Users
1. Register an account (or login if you already have one)

2. Browse packages and click "View Details"

3. Book your desired package by clicking "Book Now"

4. Fill the booking form with date and number of people

5. View all your bookings in the Dashboard

6. Cancel bookings if needed (pending bookings only)

# Screenshots
## Desktop views

## 📸 Screenshots

### Homepage
![Homepage](screenshots/1-homepage.png)

### Treks Page
![Treks Page](screenshots/2-treks-page.png)

### Travel Page
![Travel Page](screenshots/3-travel-page.png)

### Trek Detail Page
![Trek Detail](screenshots/4-trek-detail.png)

### Travel Detail Page
![Travel Detail](screenshots/5-travel-detail.png)

### Registration Page
![Registration](screenshots/6-register.png)

### Login Page
![Login](screenshots/7-login.png)

### Dashboard
![Dashboard](screenshots/8-dashboard.png)

### Trek Booking Form
![Trek Booking](screenshots/9-booking.png)

### Travel Booking Form
![Travel Booking](screenshots/10-travel-booking.png)

### About Page
![About Page](screenshots/11-about.png)

### Contact Page
![Contact Page](screenshots/12-contact.png)

### Privacy Policy
![Privacy Policy](screenshots/13-privacy.png)

### Terms & Conditions
![Terms & Conditions](screenshots/14-terms.png)

### Mobile Homepage
![Mobile Homepage](screenshots/15-mobile-home.png)

### Mobile Menu
![Mobile Menu](screenshots/16-mobile-menu.png)

### Mobile Treks
![Mobile Treks](screenshots/17-mobile-trek.png)

# Database Schema
## Users Table
id (Primary Key)

username (Unique)

email (Unique)

password_hash

full_name

phone

created_at

## Treks Table
id (Primary Key)

name, slug, region, duration, difficulty

max_altitude, price, description, itinerary

includes, excludes, image_url

## TravelPackages Table
id (Primary Key)

name, slug, destination, duration

price, description, itinerary

includes, excludes, image_url, package_type

## Bookings Table
id (Primary Key)

booking_date, trek_date, number_of_people

total_price, status

user_id (Foreign Key), trek_id (Foreign Key)

## TravelBookings Table
id (Primary Key)

booking_date, travel_date, number_of_people

total_price, status

user_id (Foreign Key), package_id (Foreign Key)

# Testing

## Browser Compatibility
✅ Google Chrome

✅ Mozilla Firefox

✅ Microsoft Edge

✅ Safari

✅ Mobile browsers (iOS/Android)

## Test Results
Feature	Result
User Registration	✅ Working
User Login	✅ Working
Browse Treks (9 packages)	✅ Working
Browse Travel (8 packages)	✅ Working
Filter Treks	✅ Working
Filter Travel	✅ Working
Book Trek	✅ Working
Book Travel	✅ Working
Dashboard	✅ Working
Cancel Booking	✅ Working
Form Validation	✅ Working
Responsive Design	✅ Working

# License
This project is created for educational purposes as part of the Bachelor of Information Technology program.

# Student Information
Name: Aruna Tamang

Student ID: LC00017003269

Course: Web Technologies

# Links
GitHub Repository: https://github.com/arunatamang0201-droid/nepal-trekking-portal

