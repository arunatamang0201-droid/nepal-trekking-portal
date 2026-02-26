# app.py - Main Flask Application File

from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os

# Initialize Flask app
app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = 'your-secret-key-here-change-this-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///trekking.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db = SQLAlchemy(app)

# Initialize login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Database Models
class User(UserMixin, db.Model):
    """User Model for storing user information"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    full_name = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship with bookings
    bookings = db.relationship('Booking', backref='user', lazy=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Trek(db.Model):
    """Trek Model for storing trekking package information"""
    __tablename__ = 'treks'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String(100), unique=True, nullable=False)
    region = db.Column(db.String(50), nullable=False)  # Everest, Annapurna, Langtang
    duration = db.Column(db.Integer, nullable=False)  # in days
    difficulty = db.Column(db.String(20), nullable=False)  # Easy, Moderate, Difficult
    max_altitude = db.Column(db.Integer)  # in meters
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text)
    itinerary = db.Column(db.Text)
    includes = db.Column(db.Text)
    excludes = db.Column(db.Text)
    image_url = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship with bookings
    bookings = db.relationship('Booking', backref='trek', lazy=True)

class Booking(db.Model):
    """Booking Model for storing trek bookings"""
    __tablename__ = 'bookings'
    
    id = db.Column(db.Integer, primary_key=True)
    booking_date = db.Column(db.DateTime, default=datetime.utcnow)
    trek_date = db.Column(db.Date, nullable=False)
    number_of_people = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, confirmed, cancelled
    special_requests = db.Column(db.Text)
    
    # Foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    trek_id = db.Column(db.Integer, db.ForeignKey('treks.id'), nullable=False)

class TravelPackage(db.Model):
    """Travel Package Model for city tours and holiday packages"""
    __tablename__ = 'travel_packages'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String(100), unique=True, nullable=False)
    destination = db.Column(db.String(50), nullable=False)  # Kathmandu, Pokhara, etc.
    duration = db.Column(db.Integer, nullable=False)  # in days
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text)
    itinerary = db.Column(db.Text)
    includes = db.Column(db.Text)
    excludes = db.Column(db.Text)
    image_url = db.Column(db.String(200))
    package_type = db.Column(db.String(50))  # Cultural, Adventure, Relaxation
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship with bookings (if you want to book travel packages too)
    travel_bookings = db.relationship('TravelBooking', backref='package', lazy=True)

class TravelBooking(db.Model):
    """Booking for travel packages"""
    __tablename__ = 'travel_bookings'
    
    id = db.Column(db.Integer, primary_key=True)
    booking_date = db.Column(db.DateTime, default=datetime.utcnow)
    travel_date = db.Column(db.Date, nullable=False)
    number_of_people = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='pending')
    
    # Foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    package_id = db.Column(db.Integer, db.ForeignKey('travel_packages.id'), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/')
def index():
    """Home page route"""
    # Get featured treks (3 most recent)
    featured_treks = Trek.query.order_by(Trek.created_at.desc()).limit(3).all()
    return render_template('index.html', featured_treks=featured_treks)

@app.route('/about')
def about():
    """About page route"""
    return render_template('about.html')

@app.route('/treks')
def treks():
    """All treks listing page"""
    region = request.args.get('region')
    difficulty = request.args.get('difficulty')
    
    # Filter treks based on query parameters
    query = Trek.query
    
    if region:
        query = query.filter_by(region=region)
    if difficulty:
        query = query.filter_by(difficulty=difficulty)
    
    treks = query.all()
    return render_template('treks.html', treks=treks)

@app.route('/trek/<slug>')
def trek_detail(slug):
    """Individual trek detail page"""
    trek = Trek.query.filter_by(slug=slug).first_or_404()
    return render_template('trek_detail.html', trek=trek)

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration route"""
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        full_name = request.form.get('full_name')
        phone = request.form.get('phone')
        
        # Check if user already exists
        user_exists = User.query.filter((User.username == username) | (User.email == email)).first()
        
        if user_exists:
            flash('Username or email already exists', 'danger')
            return redirect(url_for('register'))
        
        # Create new user
        new_user = User(
            username=username,
            email=email,
            full_name=full_name,
            phone=phone
        )
        new_user.set_password(password)
        
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login route"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'danger')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    """User logout route"""
    logout_user()
    flash('You have been logged out', 'info')
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    """User dashboard route"""
    # Get trek bookings for the current user
    trek_bookings = Booking.query.filter_by(user_id=current_user.id).all()
    
    # Get travel bookings for the current user
    travel_bookings = TravelBooking.query.filter_by(user_id=current_user.id).all()
    
    return render_template('dashboard.html', 
                           trek_bookings=trek_bookings, 
                           travel_bookings=travel_bookings)

@app.route('/book/<int:trek_id>', methods=['GET', 'POST'])
@login_required
def book_trek(trek_id):
    """Trek booking route"""
    trek = Trek.query.get_or_404(trek_id)
    
    if request.method == 'POST':
        trek_date = datetime.strptime(request.form.get('trek_date'), '%Y-%m-%d').date()
        people = int(request.form.get('number_of_people'))
        special_requests = request.form.get('special_requests')
        
        total_price = trek.price * people
        
        booking = Booking(
            trek_date=trek_date,
            number_of_people=people,
            total_price=total_price,
            special_requests=special_requests,
            user_id=current_user.id,
            trek_id=trek.id
        )
        
        db.session.add(booking)
        db.session.commit()
        
        flash('Booking successful! We will contact you soon.', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('booking.html', trek=trek)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    """Contact page route"""
    if request.method == 'POST':
        # Here you would typically send an email or save to database
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        
        flash('Thank you for your message. We will get back to you soon!', 'success')
        return redirect(url_for('contact'))
    
    return render_template('contact.html')

@app.route('/cancel-booking/<int:booking_id>')
@login_required
def cancel_booking(booking_id):
    """Cancel a booking"""
    booking = Booking.query.get_or_404(booking_id)
    
    # Ensure user can only cancel their own bookings
    if booking.user_id != current_user.id:
        flash('Unauthorized action', 'danger')
        return redirect(url_for('dashboard'))
    
    booking.status = 'cancelled'
    db.session.commit()
    
    flash('Booking cancelled successfully', 'success')
    return redirect(url_for('dashboard'))

# Travel Packages Routes
@app.route('/travel')
def travel():
    """All travel packages listing page"""
    destination = request.args.get('destination')
    package_type = request.args.get('type')
    
    query = TravelPackage.query
    
    if destination:
        query = query.filter_by(destination=destination)
    if package_type:
        query = query.filter_by(package_type=package_type)
    
    packages = query.all()
    return render_template('travel.html', packages=packages)

@app.route('/travel/<slug>')
def travel_detail(slug):
    """Individual travel package detail page"""
    package = TravelPackage.query.filter_by(slug=slug).first_or_404()
    return render_template('travel_detail.html', package=package)

@app.route('/book-travel/<int:package_id>', methods=['GET', 'POST'])
@login_required
def book_travel(package_id):
    """Travel package booking route"""
    package = TravelPackage.query.get_or_404(package_id)
    
    if request.method == 'POST':
        travel_date = datetime.strptime(request.form.get('travel_date'), '%Y-%m-%d').date()
        people = int(request.form.get('number_of_people'))
        
        total_price = package.price * people
        
        booking = TravelBooking(
            travel_date=travel_date,
            number_of_people=people,
            total_price=total_price,
            user_id=current_user.id,
            package_id=package.id
        )
        
        db.session.add(booking)
        db.session.commit()
        
        flash('Travel package booked successfully!', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('book_travel.html', package=package)

# Static Pages Routes
@app.route('/privacy')
def privacy():
    """Privacy Policy page"""
    return render_template('privacy.html')

@app.route('/terms')
def terms():
    """Terms and Conditions page"""
    return render_template('terms.html')

@app.route('/cancel-travel-booking/<int:booking_id>')
@login_required
def cancel_travel_booking(booking_id):
    """Cancel a travel booking"""
    booking = TravelBooking.query.get_or_404(booking_id)
    
    # Ensure user can only cancel their own bookings
    if booking.user_id != current_user.id:
        flash('Unauthorized action', 'danger')
        return redirect(url_for('dashboard'))
    
    booking.status = 'cancelled'
    db.session.commit()
    
    flash('Travel booking cancelled successfully', 'success')
    return redirect(url_for('dashboard'))

# Initialize database and create sample data
@app.cli.command("init-db")
def init_db():
    """Initialize the database with sample data"""
    db.create_all()
    
    # Sample trek data
    sample_treks = [
        {
            'name': 'Everest Base Camp Trek',
            'slug': 'everest-base-camp',
            'region': 'Everest',
            'duration': 14,
            'difficulty': 'Moderate',
            'max_altitude': 5545,
            'price': 1500.00,
            'description': 'Trek to the base of the world\'s highest mountain. This classic trek offers stunning views of Everest, Lhotse, and Nuptse. Experience Sherpa culture in Namche Bazaar and visit ancient Buddhist monasteries.',
            'itinerary': 'Day 1: Fly to Lukla (2,800m)\nDay 2: Trek to Phakding (2,652m)\nDay 3: Trek to Namche Bazaar (3,440m)\nDay 4: Acclimatization day in Namche\nDay 5: Trek to Tengboche (3,867m)\nDay 6: Trek to Dingboche (4,410m)\nDay 7: Acclimatization day\nDay 8: Trek to Lobuche (4,940m)\nDay 9: Trek to Gorakshep (5,170m), hike to Everest Base Camp (5,364m)\nDay 10: Hike Kala Patthar (5,545m), trek to Pheriche\nDay 11: Trek to Namche\nDay 12: Trek to Lukla\nDay 13: Fly back to Kathmandu\nDay 14: Buffer day',
            'includes': 'Airport pickups and drops, All permits (Sagarmatha National Park fee, TIMS card), Teahouse accommodation during trek, All meals (breakfast, lunch, dinner) during trek, Experienced English-speaking guide, Porter service (2 trekkers: 1 porter), First aid kit, All government taxes and office service charge',
            'excludes': 'International airfare, Nepal visa fee, Lunch and dinner in Kathmandu, Travel insurance, Personal expenses (drinks, hot shower, battery charging, wifi), Tips for guide and porter',
            'image_url': '/static/images/everest.jpg'
        },
        {
            'name': 'Annapurna Circuit Trek',
            'slug': 'annapurna-circuit',
            'region': 'Annapurna',
            'duration': 16,
            'difficulty': 'Moderate',
            'max_altitude': 5416,
            'price': 1400.00,
            'description': 'One of the world\'s greatest treks, the Annapurna Circuit takes you around the entire Annapurna massif. Experience dramatic landscapes from subtropical forests to high deserts, cross the famous Thorong La pass, and visit the holy pilgrimage site of Muktinath.',
            'itinerary': 'Day 1: Drive from Kathmandu to Besisahar to Ngadi\nDay 2: Trek to Jagat\nDay 3: Trek to Dharapani\nDay 4: Trek to Chame\nDay 5: Trek to Pisang\nDay 6: Trek to Manang\nDay 7: Acclimatization day in Manang\nDay 8: Trek to Yak Kharka\nDay 9: Trek to Thorong Phedi\nDay 10: Cross Thorong La Pass (5,416m) to Muktinath\nDay 11: Trek to Kagbeni\nDay 12: Trek to Marpha\nDay 13: Trek to Ghasa\nDay 14: Trek to Tatopani (hot springs)\nDay 15: Trek to Ghorepani\nDay 16: Hike Poon Hill, trek to Nayapul, drive to Pokhara',
            'includes': 'All ground transportation, All permits (ACAP, TIMS), Teahouse accommodation, Three meals daily during trek, Experienced guide, Porter service, Down jacket and sleeping bag (if needed), First aid kit',
            'excludes': 'International flights, Nepal visa, Meals in Kathmandu and Pokhara, Travel insurance, Hot showers, battery charging, wifi, Alcoholic drinks, Tips',
            'image_url': '/static/images/annapurna.jpg'
        },
        {
            'name': 'Langtang Valley Trek',
            'slug': 'langtang-valley',
            'region': 'Langtang',
            'duration': 10,
            'difficulty': 'Easy',
            'max_altitude': 3870,
            'price': 900.00,
            'description': 'The Langtang Valley is one of the most beautiful Himalayan valleys, known for its stunning mountain views, rich culture, and diverse wildlife. This trek is perfect for beginners and those with limited time, offering incredible scenery without extreme altitude.',
            'itinerary': 'Day 1: Drive from Kathmandu to Syabrubesi\nDay 2: Trek to Lama Hotel\nDay 3: Trek to Langtang Village\nDay 4: Trek to Kyanjin Gompa\nDay 5: Explore Kyanjin Gompa, hike to Tserko Ri\nDay 6: Trek back to Lama Hotel\nDay 7: Trek to Syabrubesi\nDay 8: Drive back to Kathmandu\nDay 9: Kathmandu sightseeing\nDay 10: Departure',
            'includes': 'All transportation, Langtang National Park permit, TIMS card, Teahouse accommodation, Three meals daily, Experienced guide, Porter service, All government taxes',
            'excludes': 'Nepal visa, International flights, Meals in Kathmandu, Travel insurance, Personal expenses, Tips',
            'image_url': '/static/images/langtang.jpg'
        },
        # Add these after the Langtang trek, before the closing ]
    {
        'name': 'Manaslu Circuit Trek',
        'slug': 'manaslu-circuit',
        'region': 'Manaslu',
        'duration': 18,
        'difficulty': 'Difficult',
        'max_altitude': 5160,
        'price': 1800.00,
        'description': 'A restricted area trek offering pristine wilderness and authentic culture. Circle the world\'s 8th highest mountain through remote villages and high passes.',
        'itinerary': 'Day 1: Drive Kathmandu to Soti Khola\nDay 2: Trek to Machha Khola\nDay 3: Trek to Jagat\nDay 4: Trek to Deng\nDay 5: Trek to Namrung\nDay 6: Trek to Samagaun\nDay 7: Acclimatization day\nDay 8: Trek to Samdo\nDay 9: Trek to Dharamsala/Larkya Phedi\nDay 10: Cross Larkya La Pass to Bimthang\nDay 11: Trek to Tilije\nDay 12: Trek to Dharapani\nDay 13: Drive back to Kathmandu',
        'includes': 'Special restricted area permit, All transportation, Teahouse accommodation, All meals, Experienced guide, Porter service, All taxes',
        'excludes': 'International flights, Nepal visa, Travel insurance, Personal expenses, Tips',
        'image_url': '/static/images/manaslu.jpg'
    },
    {
        'name': 'Ghorepani Poon Hill Trek',
        'slug': 'ghorepani-poon-hill',
        'region': 'Annapurna',
        'duration': 7,
        'difficulty': 'Easy',
        'max_altitude': 3210,
        'price': 700.00,
        'description': 'A short and sweet trek perfect for beginners. Hike to Poon Hill for sunrise views over Annapurna and Dhaulagiri ranges. Experience Gurung culture and rhododendron forests.',
        'itinerary': 'Day 1: Drive Pokhara to Nayapul, trek to Tikhedhunga\nDay 2: Trek to Ghorepani\nDay 3: Early morning hike to Poon Hill, trek to Tadapani\nDay 4: Trek to Ghandruk\nDay 5: Trek to Nayapul, drive to Pokhara\nDay 6: Free day in Pokhara\nDay 7: Drive back to Kathmandu',
        'includes': 'All transportation, ACAP permit, TIMS card, Teahouse accommodation, All meals, English-speaking guide, Porter service',
        'excludes': 'International flights, Nepal visa, Travel insurance, Personal expenses, Tips',
        'image_url': '/static/images/poonhill.jpg'
    },
    {
        'name': 'Upper Mustang Trek',
        'slug': 'upper-mustang',
        'region': 'Mustang',
        'duration': 14,
        'difficulty': 'Moderate',
        'max_altitude': 3810,
        'price': 2200.00,
        'description': 'Explore the forbidden kingdom of Mustang, a hidden desert landscape with ancient caves, monasteries, and Tibetan culture. Feel like you\'ve stepped into Tibet.',
        'itinerary': 'Day 1: Fly Pokhara to Jomsom, trek to Kagbeni\nDay 2: Trek to Chele\nDay 3: Trek to Syangbochen\nDay 4: Trek to Ghami\nDay 5: Trek to Tsarang\nDay 6: Trek to Lo Manthang\nDay 7: Explore Lo Manthang\nDay 8: Trek to Drakmar\nDay 9: Trek to Ghiling\nDay 10: Trek to Chhusang\nDay 11: Trek to Jomsom\nDay 12: Fly back to Pokhara\nDay 13-14: Buffer days',
        'includes': 'Special Mustang permit ($500), All flights, All accommodation, All meals, Experienced guide, Porter service, All taxes',
        'excludes': 'International flights, Nepal visa, Travel insurance, Personal expenses, Tips',
        'image_url': '/static/images/mustang.jpg'
    },
    {
        'name': 'Mardi Himal Trek',
        'slug': 'mardi-himal',
        'region': 'Annapurna',
        'duration': 8,
        'difficulty': 'Moderate',
        'max_altitude': 4500,
        'price': 850.00,
        'description': 'A hidden gem offering spectacular close-up views of Machhapuchhre (Fishtail) and Annapurna. This off-the-beaten-path trek takes you through lush forests and traditional villages to the beautiful Mardi Himal Base Camp.',
        'itinerary': 'Day 1: Drive Pokhara to Kande, trek to Australian Camp\nDay 2: Trek to Forest Camp\nDay 3: Trek to Low Camp\nDay 4: Trek to High Camp\nDay 5: Hike to Mardi Himal Base Camp, return to High Camp\nDay 6: Trek to Siding Village\nDay 7: Trek to Lumre, drive to Pokhara\nDay 8: Free day in Pokhara',
        'includes': 'All transportation, ACAP permit, TIMS card, Teahouse accommodation, All meals, English-speaking guide, Porter service',
        'excludes': 'International flights, Nepal visa, Travel insurance, Personal expenses, Tips',
        'image_url': '/static/images/mardi-himal.jpg'
    },
    {
        'name': 'Gokyo Lakes Trek',
        'slug': 'gokyo-lakes',
        'region': 'Everest',
        'duration': 12,
        'difficulty': 'Moderate',
        'max_altitude': 5360,
        'price': 1350.00,
        'description': 'Experience the stunning turquoise Gokyo Lakes and climb Gokyo Ri for breathtaking views of Everest, Cho Oyu, and Makalu. Cross the famous Cho La pass and visit the magnificent Ngozumpa Glacier.',
        'itinerary': 'Day 1: Fly to Lukla, trek to Phakding\nDay 2: Trek to Namche Bazaar\nDay 3: Acclimatization day\nDay 4: Trek to Dole\nDay 5: Trek to Machhermo\nDay 6: Trek to Gokyo\nDay 7: Hike Gokyo Ri, explore lakes\nDay 8: Trek to Thagnak\nDay 9: Cross Cho La pass to Dzongla\nDay 10: Trek to Lobuche\nDay 11: Trek to Gorakshep, hike Kala Patthar\nDay 12: Trek to Lukla, fly to Kathmandu',
        'includes': 'Flights Kathmandu-Lukla, All permits, Teahouse accommodation, All meals, Experienced guide, Porter service, First aid kit',
        'excludes': 'International flights, Nepal visa, Travel insurance, Personal expenses, Tips',
        'image_url': '/static/images/gokyo.jpg'
    },
    {
        'name': 'Tsum Valley Trek',
        'slug': 'tsum-valley',
        'region': 'Manaslu',
        'duration': 16,
        'difficulty': 'Difficult',
        'max_altitude': 5090,
        'price': 1950.00,
        'description': 'Discover the hidden Tsumbas Valley, a sacred Himalayan pilgrimage site with ancient Buddhist monasteries, mani walls, and unique culture. This restricted area trek offers untouched landscapes and authentic experiences.',
        'itinerary': 'Day 1: Drive Kathmandu to Soti Khola\nDay 2: Trek to Machha Khola\nDay 3: Trek to Jagat\nDay 4: Trek to Philim\nDay 5: Trek to Chumling\nDay 6: Trek to Chhekampar\nDay 7: Trek to Mu Gompa\nDay 8: Explore Mu Gompa area\nDay 9: Trek to Rachen Gompa\nDay 10: Trek to Gumba Lungdang\nDay 11: Trek to Lokpa\nDay 12: Trek to Dharapani\nDay 13-14: Drive back to Kathmandu\nDay 15-16: Buffer days',
        'includes': 'Special restricted area permit, All transportation, Teahouse accommodation, All meals, Experienced guide, Porter service, All taxes',
        'excludes': 'International flights, Nepal visa, Travel insurance, Personal expenses, Tips',
        'image_url': '/static/images/tsum-valley.jpg'
    }
    ]
    
    for trek_data in sample_treks:
        trek = Trek(**trek_data)
        db.session.add(trek)
    
        # Sample travel packages data
    sample_packages = [
        {
            'name': 'Kathmandu Valley Heritage Tour',
            'slug': 'kathmandu-heritage',
            'destination': 'Kathmandu',
            'duration': 4,
            'price': 400.00,
            'description': 'Explore the cultural heart of Nepal. Visit UNESCO World Heritage sites including Pashupatinath, Boudhanath, Swayambhunath, and Kathmandu Durbar Square. Experience the living heritage of the Newar community.',
            'itinerary': 'Day 1: Arrival in Kathmandu, evening cultural show and dinner\nDay 2: Visit Pashupatinath and Boudhanath, afternoon Patan Durbar Square\nDay 3: Visit Swayambhunath (Monkey Temple), Kathmandu Durbar Square, Thamel shopping\nDay 4: Optional Bhaktapur tour, departure',
            'includes': 'Airport transfers, 3 nights hotel with breakfast, Private AC vehicle, English-speaking guide, All entry fees, Welcome dinner',
            'excludes': 'International flights, Nepal visa, Lunch and dinner, Travel insurance, Personal expenses',
            'image_url': '/static/images/kathmandu.jpg',
            'package_type': 'Cultural'
        },
        {
            'name': 'Pokhara Adventure & Relaxation',
            'slug': 'pokhara-adventure',
            'destination': 'Pokhara',
            'duration': 5,
            'price': 500.00,
            'description': 'Experience the magic of Pokhara, the city of lakes. Enjoy stunning views of Annapurna range, boating on Phewa Lake, and optional adventure activities like paragliding and zip-lining.',
            'itinerary': 'Day 1: Drive or fly to Pokhara, lakeside evening\nDay 2: Sunrise at Sarangkot, boating at Phewa Lake, visit Tal Barahi temple\nDay 3: Adventure day - paragliding, zip-lining, or ultralight flight (optional extra)\nDay 4: Visit Davis Falls, Gupteshwor Cave, International Mountain Museum\nDay 5: Free morning, return to Kathmandu',
            'includes': 'Hotel accommodation with breakfast, All ground transportation, Boating at Phewa Lake, Guide for sightseeing, All entry fees',
            'excludes': 'Flights (can be added), Adventure activities, Lunch and dinner, Travel insurance',
            'image_url': '/static/images/pokhara.jpg',
            'package_type': 'Adventure'
        },
        {
            'name': 'Chitwan Jungle Safari',
            'slug': 'chitwan-safari',
            'destination': 'Chitwan',
            'duration': 3,
            'price': 350.00,
            'description': 'Discover wildlife in Chitwan National Park, a UNESCO World Heritage site. Spot rhinos, deer, crocodiles, and if lucky, the Royal Bengal Tiger. Enjoy jungle walks, canoe rides, and cultural programs.',
            'itinerary': 'Day 1: Drive to Chitwan, welcome program, Tharu cultural show\nDay 2: Morning canoe ride, jungle walk, elephant safari, bird watching\nDay 3: Bird watching, drive back to Kathmandu',
            'includes': 'Transportation, Resort accommodation with all meals, All jungle activities, National Park fees, Guide, Cultural program',
            'excludes': 'International flights, Travel insurance, Alcoholic drinks, Personal expenses',
            'image_url': '/static/images/chitwan.jpg',
            'package_type': 'Wildlife'
        },
        {
            'name': 'Lumbini Pilgrimage Tour',
            'slug': 'lumbini-pilgrimage',
            'destination': 'Lumbini',
            'duration': 3,
            'price': 300.00,
            'description': 'Visit the birthplace of Lord Buddha, one of the holiest sites for Buddhists worldwide. Explore monasteries built by different countries, meditate under the Bodhi tree, and feel the peaceful atmosphere.',
            'itinerary': 'Day 1: Fly to Bhairahawa, transfer to Lumbini, visit Maya Devi Temple\nDay 2: Explore monastic zone, visit monasteries of different countries, meditation session\nDay 3: Visit nearby Kushinagar (India) option, return to Kathmandu',
            'includes': 'All transportation, Hotel accommodation with breakfast, English-speaking guide, All entry fees',
            'excludes': 'International flights, India visa (if visiting Kushinagar), Lunch and dinner, Travel insurance',
            'image_url': '/static/images/lumbini.jpg',
            'package_type': 'Pilgrimage'
        },
        {
            'name': 'Nepal Highlights Tour',
            'slug': 'nepal-highlights',
            'destination': 'Multiple Cities',
            'duration': 10,
            'price': 1200.00,
            'description': 'The ultimate Nepal experience combining culture, adventure, and wildlife. Visit Kathmandu, Pokhara, and Chitwan in one comprehensive package. Perfect for first-time visitors.',
            'itinerary': 'Day 1-2: Kathmandu sightseeing\nDay 3-5: Pokhara adventure\nDay 6-8: Chitwan safari\nDay 9: Return to Kathmandu\nDay 10: Departure',
            'includes': 'All transportation, Domestic flights, Hotel accommodation with breakfast, All activities as per itinerary, Experienced guide, All entry fees',
            'excludes': 'International flights, Nepal visa, Travel insurance, Personal expenses, Tips',
            'image_url': '/static/images/nepal-highlights.jpg',
            'package_type': 'Combination'
        },
            # NEW TRAVEL PACKAGES - Add these after Nepal Highlights
    {
        'name': 'Bandipur Heritage Village',
        'slug': 'bandipur-village',
        'destination': 'Bandipur',
        'duration': 3,
        'price': 280.00,
        'description': 'Step back in time in the charming hilltop town of Bandipur. Wander through Newari streets, enjoy panoramic mountain views, and experience traditional village life. Perfect for culture lovers and photographers.',
        'itinerary': 'Day 1: Drive Kathmandu to Bandipur, sunset view\nDay 2: Explore Bandipur - Tundikhel, Siddha Gufa, Thani Mai Temple\nDay 3: Morning walk, drive back to Kathmandu',
        'includes': 'Transportation, Hotel accommodation with breakfast, Guided village tour, All entry fees',
        'excludes': 'Lunch and dinner, Travel insurance, Personal expenses',
        'image_url': '/static/images/bandipur.jpg',
        'package_type': 'Cultural'
    },
    {
        'name': 'Kathmandu to Pokhara Hiking Trail',
        'slug': 'kathmandu-pokhara-hiking',
        'destination': 'Multiple Cities',
        'duration': 7,
        'price': 650.00,
        'description': 'Combine culture and nature on this unique hiking trail from Kathmandu Valley to Pokhara. Walk through traditional villages, terraced farms, and forests while experiencing rural Nepali life.',
        'itinerary': 'Day 1: Drive to Sundarijal, trek to Chisapani\nDay 2: Trek to Nagarkot\nDay 3: Trek to Dhulikhel\nDay 4: Trek to Panauti\nDay 5: Drive to Pokhara\nDay 6: Pokhara sightseeing\nDay 7: Return to Kathmandu',
        'includes': 'All transportation, Accommodation with breakfast, Guide, Porter service, All entry fees',
        'excludes': 'Lunch and dinner, Travel insurance, Personal expenses, Tips',
        'image_url': '/static/images/kathmandu-pokhara-trail.jpg',
        'package_type': 'Adventure'
    },
    {
        'name': 'Nepal Foodie Tour',
        'slug': 'nepal-foodie-tour',
        'destination': 'Multiple Cities',
        'duration': 8,
        'price': 890.00,
        'description': 'A culinary journey through Nepal\'s diverse flavors. Taste authentic Newari, Thakali, and Tibetan dishes, take cooking classes, visit local markets, and learn about Nepal\'s food culture.',
        'itinerary': 'Day 1-2: Kathmandu food tour, cooking class\nDay 3-4: Pokhara lakeside dining, local market visit\nDay 5: Bandipur traditional meal experience\nDay 6-7: Cooking workshops, spice tours\nDay 8: Departure',
        'includes': 'All transportation, Accommodation with breakfast, Food tours, Cooking classes, 2 meals daily, English-speaking guide',
        'excludes': 'International flights, Alcoholic drinks, Travel insurance, Personal expenses',
        'image_url': '/static/images/food-tour.jpg',
        'package_type': 'Special Interest'
    }
    ]
    
    for package_data in sample_packages:
        package = TravelPackage(**package_data)
        db.session.add(package)

    db.session.commit()
    print("Database initialized with sample data!")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)