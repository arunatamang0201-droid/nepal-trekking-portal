// Custom JavaScript for Nepal Trekking Portal

// Wait for DOM to load
document.addEventListener('DOMContentLoaded', function() {
    
    // Initialize tooltips if Bootstrap is loaded
    if (typeof bootstrap !== 'undefined') {
        var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }
    
    // Form validation for registration
    const registerForm = document.getElementById('registerForm');
    if (registerForm) {
        registerForm.addEventListener('submit', function(e) {
            const password = document.getElementById('password').value;
            const confirmPassword = document.getElementById('confirm_password').value;
            
            if (password !== confirmPassword) {
                e.preventDefault();
                alert('Passwords do not match!');
            }
            
            if (password.length < 8) {
                e.preventDefault();
                alert('Password must be at least 8 characters long!');
            }
        });
    }
    
    // Login form validation
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', function(e) {
            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;
            
            if (!username || !password) {
                e.preventDefault();
                alert('Please fill in all fields!');
            }
        });
    }
    
    // Contact form validation
    const contactForm = document.getElementById('contactForm');
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            const email = document.getElementById('email').value;
            const message = document.getElementById('message').value;
            
            if (!isValidEmail(email)) {
                e.preventDefault();
                alert('Please enter a valid email address!');
            }
            
            if (message.length < 10) {
                e.preventDefault();
                alert('Message must be at least 10 characters long!');
            }
        });
    }
    
    // Booking form validation and price calculation
    const bookingForm = document.getElementById('bookingForm');
    if (bookingForm) {
        const peopleInput = document.getElementById('number_of_people');
        const trekDate = document.getElementById('trek_date');
        
        // Calculate total price
        if (peopleInput) {
            peopleInput.addEventListener('input', updateTotalPrice);
        }
        
        // Validate date (cannot be in past)
        if (trekDate) {
            const today = new Date().toISOString().split('T')[0];
            trekDate.setAttribute('min', today);
        }
        
        bookingForm.addEventListener('submit', function(e) {
            if (!document.getElementById('terms').checked) {
                e.preventDefault();
                alert('You must agree to the terms and conditions!');
            }
        });
    }
    
    // Email validation helper function
    function isValidEmail(email) {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(email);
    }
    
    // Update total price in booking form
    function updateTotalPrice() {
        const people = parseInt(document.getElementById('number_of_people').value) || 1;
        const pricePerPerson = parseFloat(document.querySelector('.display-6')?.textContent.replace('$', '')) || 0;
        const totalDisplay = document.getElementById('totalDisplay');
        
        if (totalDisplay) {
            totalDisplay.innerHTML = `<span>Total (${people} person${people > 1 ? 's' : ''}):</span> <strong>$${people * pricePerPerson}</strong>`;
        }
    }
    
    // Add smooth scrolling to all links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    // Add to favorites functionality (if needed)
    const favButtons = document.querySelectorAll('.favorite-btn');
    favButtons.forEach(btn => {
        btn.addEventListener('click', function() {
            this.classList.toggle('text-danger');
            const icon = this.querySelector('i');
            if (icon.classList.contains('far')) {
                icon.classList.remove('far');
                icon.classList.add('fas');
            } else {
                icon.classList.remove('fas');
                icon.classList.add('far');
            }
        });
    });
    
    // Search functionality (basic)
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        searchInput.addEventListener('keyup', function() {
            const searchTerm = this.value.toLowerCase();
            const cards = document.querySelectorAll('.card');
            
            cards.forEach(card => {
                const title = card.querySelector('.card-title')?.textContent.toLowerCase() || '';
                if (title.includes(searchTerm)) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    }
    
    // Password strength indicator
    const passwordInput = document.getElementById('password');
    if (passwordInput) {
        passwordInput.addEventListener('input', function() {
            const strength = checkPasswordStrength(this.value);
            showPasswordStrength(strength);
        });
    }
    
    function checkPasswordStrength(password) {
        let strength = 0;
        if (password.length >= 8) strength++;
        if (password.match(/[a-z]+/)) strength++;
        if (password.match(/[A-Z]+/)) strength++;
        if (password.match(/[0-9]+/)) strength++;
        if (password.match(/[$@#&!]+/)) strength++;
        return strength;
    }
    
    function showPasswordStrength(strength) {
        let strengthText = '';
        let strengthClass = '';
        
        switch(strength) {
            case 0:
            case 1:
                strengthText = 'Weak';
                strengthClass = 'text-danger';
                break;
            case 2:
            case 3:
                strengthText = 'Medium';
                strengthClass = 'text-warning';
                break;
            case 4:
            case 5:
                strengthText = 'Strong';
                strengthClass = 'text-success';
                break;
        }
        
        let strengthElement = document.getElementById('password-strength');
        if (!strengthElement) {
            strengthElement = document.createElement('div');
            strengthElement.id = 'password-strength';
            passwordInput.parentNode.appendChild(strengthElement);
        }
        
        strengthElement.textContent = 'Password strength: ' + strengthText;
        strengthElement.className = 'mt-2 ' + strengthClass;
    }
    
    // Auto-hide alerts after 5 seconds
    setTimeout(function() {
        const alerts = document.querySelectorAll('.alert');
        alerts.forEach(alert => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);

          // ========== TRAVEL BOOKING FUNCTIONS ==========
    // Check if we're on the travel booking page
    if (document.getElementById('travelBookingForm')) {
        console.log('Travel booking page detected');
        
        const travelPeopleInput = document.getElementById('travel_people');
        const travelTotalDisplay = document.getElementById('travelTotal');
        const travelPriceInput = document.getElementById('travel_price');
        const travelDateInput = document.getElementById('travel_date');
        const travelForm = document.getElementById('travelBookingForm');
        
        // Get price from hidden input
        let travelPricePerPerson = 0;
        if (travelPriceInput) {
            travelPricePerPerson = parseFloat(travelPriceInput.value);
        }
        
        // Function to update total price
        function updateTravelTotal() {
            if (travelPeopleInput && travelTotalDisplay) {
                const people = parseInt(travelPeopleInput.value) || 1;
                const total = people * travelPricePerPerson;
                travelTotalDisplay.textContent = total;
            }
        }
        
        // Update total when number of people changes
        if (travelPeopleInput) {
            travelPeopleInput.addEventListener('input', updateTravelTotal);
        }
        
        // Set minimum date to today
        if (travelDateInput) {
            const today = new Date();
            const yyyy = today.getFullYear();
            const mm = String(today.getMonth() + 1).padStart(2, '0');
            const dd = String(today.getDate()).padStart(2, '0');
            const todayFormatted = yyyy + '-' + mm + '-' + dd;
            travelDateInput.setAttribute('min', todayFormatted);
        }
        
        // Form validation before submit
        if (travelForm) {
            travelForm.addEventListener('submit', function(e) {
                const termsChecked = document.getElementById('terms').checked;
                const travelDate = travelDateInput ? travelDateInput.value : '';
                const people = travelPeopleInput ? parseInt(travelPeopleInput.value) : 0;
                
                let errors = [];
                
                if (!travelDate) {
                    errors.push('Please select a travel date');
                }
                
                if (people < 1) {
                    errors.push('Number of people must be at least 1');
                }
                
                if (!termsChecked) {
                    errors.push('You must agree to the terms and conditions');
                }
                
                if (errors.length > 0) {
                    e.preventDefault();
                    alert('Please fix the following:\n- ' + errors.join('\n- '));
                }
            });
        }
    }
        // ========== TREK BOOKING PAGE FUNCTIONS ==========
    // Check if we're on the trek booking page
    if (document.getElementById('trekBookingForm')) {
        console.log('Trek booking page loaded');
        
        // Get all the elements we need
        const trekDateInput = document.getElementById('trek_date');
        const trekPeopleInput = document.getElementById('trek_people');
        const trekTotalDisplay = document.getElementById('trekTotal');
        const trekTotalSummary = document.getElementById('trekTotalDisplay');
        const trekPriceInput = document.getElementById('trek_price');
        const termsCheckbox = document.getElementById('terms');
        const trekBookingForm = document.getElementById('trekBookingForm');
        
        // Get price from hidden input
        let trekPricePerPerson = 0;
        if (trekPriceInput) {
            trekPricePerPerson = parseFloat(trekPriceInput.value);
        }
        
        // Function 1: Set minimum date to today
        function setTrekMinDate() {
            if (trekDateInput) {
                const today = new Date();
                const yyyy = today.getFullYear();
                const mm = String(today.getMonth() + 1).padStart(2, '0');
                const dd = String(today.getDate()).padStart(2, '0');
                const todayFormatted = yyyy + '-' + mm + '-' + dd;
                trekDateInput.setAttribute('min', todayFormatted);
            }
        }
        
        // Function 2: Calculate and update total price
        function updateTrekTotal() {
            if (trekPeopleInput && trekTotalDisplay && trekTotalSummary) {
                const people = parseInt(trekPeopleInput.value) || 1;
                const total = people * trekPricePerPerson;
                trekTotalDisplay.textContent = total;
                trekTotalSummary.innerHTML = '<span>Total (' + people + ' person' + (people > 1 ? 's' : '') + '):</span> <strong>$' + total + '</strong>';
            }
        }
        
        // Function 3: Validate form before submit
        function validateTrekForm(event) {
            const travelDate = trekDateInput ? trekDateInput.value : '';
            const people = trekPeopleInput ? parseInt(trekPeopleInput.value) : 0;
            const termsChecked = termsCheckbox ? termsCheckbox.checked : false;
            
            let errors = [];
            
            if (!travelDate) errors.push('Please select a travel date');
            if (people < 1) errors.push('Number of people must be at least 1');
            if (!termsChecked) errors.push('You must agree to the terms and conditions');
            
            if (travelDate) {
                const selectedDate = new Date(travelDate);
                const today = new Date();
                today.setHours(0, 0, 0, 0);
                if (selectedDate < today) errors.push('Travel date cannot be in the past');
            }
            
            if (errors.length > 0) {
                event.preventDefault();
                alert('Please fix the following:\n- ' + errors.join('\n- '));
                return false;
            }
            return true;
        }
        
        // Function 4: Show loading state on submit
        function showTrekLoading() {
            const submitBtn = trekBookingForm.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm"></span> Processing...';
            }
        }
        
        // Attach all event listeners for trek booking
        setTrekMinDate();
        if (trekPeopleInput) trekPeopleInput.addEventListener('input', updateTrekTotal);
        if (trekBookingForm) {
            trekBookingForm.addEventListener('submit', validateTrekForm);
            trekBookingForm.addEventListener('submit', showTrekLoading);
        }
    }

    // ========== TRAVEL BOOKING PAGE FUNCTIONS ==========
    // Check if we're on the travel booking page
    if (document.getElementById('travelBookingForm')) {
        console.log('Travel booking page loaded');
        
        // Get all the elements we need
        const travelDateInput = document.getElementById('travel_date');
        const travelPeopleInput = document.getElementById('travel_people');
        const travelTotalDisplay = document.getElementById('travelTotal');
        const travelTotalSummary = document.getElementById('travelTotalDisplay');
        const travelPriceInput = document.getElementById('travel_price');
        const termsCheckbox = document.getElementById('terms');
        const travelBookingForm = document.getElementById('travelBookingForm');
        
        // Get price from hidden input
        let travelPricePerPerson = 0;
        if (travelPriceInput) {
            travelPricePerPerson = parseFloat(travelPriceInput.value);
        }
        
        // Function 1: Set minimum date to today
        function setTravelMinDate() {
            if (travelDateInput) {
                const today = new Date();
                const yyyy = today.getFullYear();
                const mm = String(today.getMonth() + 1).padStart(2, '0');
                const dd = String(today.getDate()).padStart(2, '0');
                const todayFormatted = yyyy + '-' + mm + '-' + dd;
                travelDateInput.setAttribute('min', todayFormatted);
            }
        }
        
        // Function 2: Calculate and update total price
        function updateTravelTotal() {
            if (travelPeopleInput && travelTotalDisplay && travelTotalSummary) {
                const people = parseInt(travelPeopleInput.value) || 1;
                const total = people * travelPricePerPerson;
                travelTotalDisplay.textContent = total;
                travelTotalSummary.innerHTML = '<span>Total (' + people + ' person' + (people > 1 ? 's' : '') + '):</span> <strong>$' + total + '</strong>';
            }
        }
        
        // Function 3: Validate form before submit
        function validateTravelForm(event) {
            const travelDate = travelDateInput ? travelDateInput.value : '';
            const people = travelPeopleInput ? parseInt(travelPeopleInput.value) : 0;
            const termsChecked = termsCheckbox ? termsCheckbox.checked : false;
            
            let errors = [];
            
            if (!travelDate) errors.push('Please select a travel date');
            if (people < 1) errors.push('Number of people must be at least 1');
            if (!termsChecked) errors.push('You must agree to the terms and conditions');
            
            if (travelDate) {
                const selectedDate = new Date(travelDate);
                const today = new Date();
                today.setHours(0, 0, 0, 0);
                if (selectedDate < today) errors.push('Travel date cannot be in the past');
            }
            
            if (errors.length > 0) {
                event.preventDefault();
                alert('Please fix the following:\n- ' + errors.join('\n- '));
                return false;
            }
            return true;
        }
        
        // Function 4: Show loading state on submit
        function showTravelLoading() {
            const submitBtn = travelBookingForm.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm"></span> Processing...';
            }
        }
        
        // Attach all event listeners for travel booking
        setTravelMinDate();
        if (travelPeopleInput) travelPeopleInput.addEventListener('input', updateTravelTotal);
        if (travelBookingForm) {
            travelBookingForm.addEventListener('submit', validateTravelForm);
            travelBookingForm.addEventListener('submit', showTravelLoading);
        }
    }
});