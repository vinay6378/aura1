// Enhanced interactive components for Aura website
class InteractiveComponents {
    constructor() {
        this.init();
    }

    init() {
        this.initSmoothScrolling();
        this.initParallaxEffects();
        this.initCountUpAnimations();
        this.initHoverEffects();
        this.initFormInteractions();
        this.initLoadingStates();
        this.initMicroInteractions();
    }

    // Smooth scrolling for anchor links
    initSmoothScrolling() {
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
    }

    // Parallax scrolling effects
    initParallaxEffects() {
        const parallaxElements = document.querySelectorAll('.parallax');
        
        window.addEventListener('scroll', () => {
            const scrolled = window.pageYOffset;
            
            parallaxElements.forEach(element => {
                const speed = element.dataset.speed || 0.5;
                const yPos = -(scrolled * speed);
                element.style.transform = `translateY(${yPos}px)`;
            });
        });
    }

    // Count-up animations for statistics
    initCountUpAnimations() {
        const countElements = document.querySelectorAll('.count-up');
        
        const observerOptions = {
            threshold: 0.5,
            rootMargin: '0px'
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    this.animateCount(entry.target);
                    observer.unobserve(entry.target);
                }
            });
        }, observerOptions);

        countElements.forEach(element => {
            observer.observe(element);
        });
    }

    animateCount(element) {
        const target = parseInt(element.dataset.target);
        const duration = parseInt(element.dataset.duration) || 2000;
        const start = 0;
        const increment = target / (duration / 16);
        let current = start;

        const timer = setInterval(() => {
            current += increment;
            if (current >= target) {
                current = target;
                clearInterval(timer);
            }
            element.textContent = Math.floor(current).toLocaleString();
        }, 16);
    }

    // Enhanced hover effects
    initHoverEffects() {
        // Card hover effects
        document.querySelectorAll('.hover-card').forEach(card => {
            card.addEventListener('mouseenter', function() {
                this.style.transform = 'translateY(-10px) scale(1.02)';
                this.style.boxShadow = '0 20px 40px rgba(0,0,0,0.1)';
            });

            card.addEventListener('mouseleave', function() {
                this.style.transform = 'translateY(0) scale(1)';
                this.style.boxShadow = '0 10px 30px rgba(0,0,0,0.1)';
            });
        });

        // Button ripple effects
        document.querySelectorAll('.btn-ripple').forEach(button => {
            button.addEventListener('click', function(e) {
                const ripple = document.createElement('span');
                const rect = this.getBoundingClientRect();
                const size = Math.max(rect.width, rect.height);
                const x = e.clientX - rect.left - size / 2;
                const y = e.clientY - rect.top - size / 2;

                ripple.style.cssText = `
                    position: absolute;
                    width: ${size}px;
                    height: ${size}px;
                    border-radius: 50%;
                    background: rgba(255,255,255,0.5);
                    left: ${x}px;
                    top: ${y}px;
                    transform: scale(0);
                    animation: ripple 0.6s ease-out;
                    pointer-events: none;
                `;

                this.style.position = 'relative';
                this.style.overflow = 'hidden';
                this.appendChild(ripple);

                setTimeout(() => ripple.remove(), 600);
            });
        });
    }

    // Enhanced form interactions
    initFormInteractions() {
        // Floating labels
        document.querySelectorAll('.form-control').forEach(input => {
            const label = input.previousElementSibling;
            if (label && label.classList.contains('form-label')) {
                input.addEventListener('focus', () => {
                    label.classList.add('focused');
                });

                input.addEventListener('blur', () => {
                    if (!input.value) {
                        label.classList.remove('focused');
                    }
                });

                // Check initial state
                if (input.value) {
                    label.classList.add('focused');
                }
            }
        });

        // Real-time validation
        document.querySelectorAll('.form-control[data-validate]').forEach(input => {
            input.addEventListener('input', () => {
                this.validateField(input);
            });
        });
    }

    validateField(field) {
        const validateType = field.dataset.validate;
        let isValid = true;
        let message = '';

        switch (validateType) {
            case 'email':
                isValid = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(field.value);
                message = 'Please enter a valid email address';
                break;
            case 'phone':
                isValid = /^[\d\s\-\+\(\)]+$/.test(field.value);
                message = 'Please enter a valid phone number';
                break;
            case 'required':
                isValid = field.value.trim().length > 0;
                message = 'This field is required';
                break;
        }

        this.showFieldValidation(field, isValid, message);
    }

    showFieldValidation(field, isValid, message) {
        // Remove existing validation
        const existing = field.parentNode.querySelector('.field-validation');
        if (existing) existing.remove();

        if (!isValid) {
            const validation = document.createElement('div');
            validation.className = 'field-validation text-danger small mt-1';
            validation.textContent = message;
            field.parentNode.appendChild(validation);
            field.classList.add('is-invalid');
        } else {
            field.classList.remove('is-invalid');
            field.classList.add('is-valid');
        }
    }

    // Loading states for buttons
    initLoadingStates() {
        document.querySelectorAll('[data-loading]').forEach(button => {
            button.addEventListener('click', function() {
                const originalText = this.innerHTML;
                const loadingText = this.dataset.loading;
                
                this.disabled = true;
                this.innerHTML = `
                    <span class="spinner-border spinner-border-sm me-2" role="status"></span>
                    ${loadingText}
                `;

                // Simulate loading completion
                setTimeout(() => {
                    this.disabled = false;
                    this.innerHTML = originalText;
                }, 2000);
            });
        });
    }

    // Micro-interactions
    initMicroInteractions() {
        // Typing effect for hero text
        const typingElements = document.querySelectorAll('.typing-effect');
        typingElements.forEach(element => {
            const text = element.textContent;
            element.textContent = '';
            this.typeText(element, text, 50);
        });

        // Fade in elements on scroll
        const fadeElements = document.querySelectorAll('.fade-in-up');
        const fadeObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate__animated', 'animate__fadeInUp');
                    fadeObserver.unobserve(entry.target);
                }
            });
        }, { threshold: 0.1 });

        fadeElements.forEach(element => {
            fadeObserver.observe(element);
        });
    }

    typeText(element, text, speed) {
        let i = 0;
        const timer = setInterval(() => {
            if (i < text.length) {
                element.textContent += text.charAt(i);
                i++;
            } else {
                clearInterval(timer);
            }
        }, speed);
    }
}

// Add CSS for animations
const style = document.createElement('style');
style.textContent = `
    @keyframes ripple {
        to {
            transform: scale(4);
            opacity: 0;
        }
    }

    .hover-card {
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }

    .form-label.focused {
        color: #667eea;
        transform: translateY(-2px);
    }

    .field-validation {
        animation: slideDown 0.3s ease;
    }

    @keyframes slideDown {
        from {
            opacity: 0;
            transform: translateY(-10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    .typing-effect::after {
        content: '|';
        animation: blink 1s infinite;
    }

    @keyframes blink {
        0%, 50% { opacity: 1; }
        51%, 100% { opacity: 0; }
    }
`;
document.head.appendChild(style);

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    new InteractiveComponents();
});

// Export for global use
window.InteractiveComponents = InteractiveComponents;
