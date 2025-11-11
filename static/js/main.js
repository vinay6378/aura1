// ====================================
// AURA - Enhanced Animation System
// Featuring anime.js + GSAP + Three.js
// ====================================

document.addEventListener('DOMContentLoaded', function() {
  
  // ====================================
  // PAGE LOADER WITH ANIME.JS
  // ====================================
  const pageLoader = document.createElement('div');
  pageLoader.className = 'page-loader';
  pageLoader.innerHTML = `
    <div class="loader-logo">
      <div class="loader-ring"></div>
      <div class="loader-ring"></div>
      <div class="loader-ring"></div>
    </div>
  `;
  document.body.prepend(pageLoader);

  // Animate loader rings with anime.js
  if (typeof anime !== 'undefined') {
    anime({
      targets: '.loader-ring',
      rotate: 360,
      duration: 1000,
      loop: true,
      easing: 'linear',
      delay: anime.stagger(200)
    });

    // Hide loader after page loads
    window.addEventListener('load', () => {
      anime({
        targets: '.page-loader',
        opacity: 0,
        duration: 800,
        easing: 'easeOutQuad',
        complete: () => {
          pageLoader.classList.add('hidden');
          setTimeout(() => pageLoader.remove(), 500);
          initPageAnimations();
        }
      });
    });
  } else {
    // Fallback if anime.js doesn't load
    window.addEventListener('load', () => {
      setTimeout(() => {
        pageLoader.classList.add('hidden');
        setTimeout(() => pageLoader.remove(), 500);
        initPageAnimations();
      }, 800);
    });
  }

  // ====================================
  // SMOOTH SCROLLING - LENIS
  // ====================================
  const lenis = new Lenis({
    duration: 1.2,
    easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
    direction: 'vertical',
    gestureDirection: 'vertical',
    smooth: true,
    mouseMultiplier: 1,
    smoothTouch: false,
    touchMultiplier: 2,
    infinite: false,
  });

  function raf(time) {
    lenis.raf(time);
    requestAnimationFrame(raf);
  }
  requestAnimationFrame(raf);

  // ====================================
  // GSAP + SCROLLTRIGGER SETUP
  // ====================================
  gsap.registerPlugin(ScrollTrigger);
  ScrollTrigger.defaults({
    scroller: document.body
  });

  // ====================================
  // 3D PARTICLES WITH THREE.JS
  // ====================================
  if (typeof THREE !== 'undefined') {
    const canvas = document.createElement('canvas');
    canvas.id = 'particles-canvas';
    document.body.prepend(canvas);

    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    const renderer = new THREE.WebGLRenderer({ canvas, alpha: true, antialias: true });
    
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(window.devicePixelRatio);
    camera.position.z = 5;

    // Create particle system
    const particleCount = 500;
    const particles = new THREE.BufferGeometry();
    const positions = new Float32Array(particleCount * 3);
    const colors = new Float32Array(particleCount * 3);

    for (let i = 0; i < particleCount * 3; i += 3) {
      positions[i] = (Math.random() - 0.5) * 20;
      positions[i + 1] = (Math.random() - 0.5) * 20;
      positions[i + 2] = (Math.random() - 0.5) * 10;

      // Purple to pink gradient
      const color = new THREE.Color();
      color.setHSL(Math.random() * 0.1 + 0.75, 1, 0.6);
      colors[i] = color.r;
      colors[i + 1] = color.g;
      colors[i + 2] = color.b;
    }

    particles.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    particles.setAttribute('color', new THREE.BufferAttribute(colors, 3));

    const particleMaterial = new THREE.PointsMaterial({
      size: 0.05,
      vertexColors: true,
      transparent: true,
      opacity: 0.6,
      blending: THREE.AdditiveBlending
    });

    const particleSystem = new THREE.Points(particles, particleMaterial);
    scene.add(particleSystem);

    // Animate particles
    function animateParticles() {
      requestAnimationFrame(animateParticles);
      
      particleSystem.rotation.x += 0.0005;
      particleSystem.rotation.y += 0.001;

      const positions = particleSystem.geometry.attributes.position.array;
      for (let i = 1; i < positions.length; i += 3) {
        positions[i] += Math.sin(Date.now() * 0.001 + i) * 0.001;
      }
      particleSystem.geometry.attributes.position.needsUpdate = true;

      renderer.render(scene, camera);
    }
    animateParticles();

    // Handle window resize
    window.addEventListener('resize', () => {
      camera.aspect = window.innerWidth / window.innerHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(window.innerWidth, window.innerHeight);
    });
  }

  // ====================================
  // CUSTOM CURSOR
  // ====================================
  const cursor = document.getElementById('custom-cursor');
  const cursorDot = document.getElementById('cursor-dot');
  const isTouchDevice = 'ontouchstart' in window || navigator.maxTouchPoints > 0;

  if (cursor && cursorDot && !isTouchDevice) {
    document.body.classList.add('no-cursor');
    cursor.style.opacity = '0';
    cursorDot.style.opacity = '0';

    let mouseX = 0, mouseY = 0;
    let cursorX = 0, cursorY = 0;
    let dotX = 0, dotY = 0;

    document.addEventListener('mousemove', (e) => {
      mouseX = e.clientX;
      mouseY = e.clientY;
      
      if (cursor.style.opacity === '0') {
        cursor.style.opacity = '1';
        cursorDot.style.opacity = '1';
      }
    });

    function animateCursor() {
      const speed = 0.15;
      const dotSpeed = 0.3;

      cursorX += (mouseX - cursorX) * speed;
      cursorY += (mouseY - cursorY) * speed;
      dotX += (mouseX - dotX) * dotSpeed;
      dotY += (mouseY - dotY) * dotSpeed;

      cursor.style.left = cursorX + 'px';
      cursor.style.top = cursorY + 'px';
      cursorDot.style.left = dotX + 'px';
      cursorDot.style.top = dotY + 'px';

      requestAnimationFrame(animateCursor);
    }
    animateCursor();

    const interactiveElements = document.querySelectorAll('a, button, .btn, .card, .service-card, .feature-box, input, textarea, select');
    interactiveElements.forEach(el => {
      el.addEventListener('mouseenter', () => {
        cursor.classList.add('cursor-hover');
        cursorDot.classList.add('cursor-hover');
      });
      el.addEventListener('mouseleave', () => {
        cursor.classList.remove('cursor-hover');
        cursorDot.classList.remove('cursor-hover');
      });
    });

    document.addEventListener('mouseleave', () => {
      cursor.style.opacity = '0';
      cursorDot.style.opacity = '0';
    });
  } else if (isTouchDevice) {
    if (cursor) cursor.style.display = 'none';
    if (cursorDot) cursorDot.style.display = 'none';
  }

  // ====================================
  // INIT PAGE ANIMATIONS
  // ====================================
  function initPageAnimations() {
    
    // Animate logo with anime.js
    if (typeof anime !== 'undefined') {
      anime({
        targets: '.aura-logo',
        scale: [0, 1],
        rotate: [-180, 0],
        opacity: [0, 1],
        duration: 1200,
        easing: 'easeOutElastic(1, .8)'
      });

      anime({
        targets: '.aura-text',
        translateX: [-50, 0],
        opacity: [0, 1],
        duration: 800,
        delay: 300,
        easing: 'easeOutQuad'
      });

      // Animate nav items
      anime({
        targets: '.nav-item',
        translateY: [-20, 0],
        opacity: [0, 1],
        duration: 600,
        delay: anime.stagger(100, {start: 400}),
        easing: 'easeOutQuad'
      });
    }

    // Hero section animations
    const heroSection = document.querySelector('.hero-section');
    if (heroSection) {
      gsap.from('.hero-section h1', {
        opacity: 0,
        y: 80,
        scale: 0.9,
        duration: 1.2,
        delay: 0.2,
        ease: 'power3.out'
      });

      gsap.from('.hero-section .lead', {
        opacity: 0,
        y: 60,
        duration: 1,
        delay: 0.5,
        ease: 'power3.out'
      });

      gsap.from('.hero-section .btn', {
        opacity: 0,
        y: 40,
        scale: 0.9,
        duration: 0.8,
        delay: 0.8,
        stagger: 0.2,
        ease: 'back.out(1.7)'
      });
    }

    // Service cards with anime.js
    if (typeof anime !== 'undefined') {
      anime({
        targets: '.service-card',
        translateY: [100, 0],
        opacity: [0, 1],
        scale: [0.8, 1],
        rotate: [5, 0],
        duration: 1000,
        delay: anime.stagger(200, {start: 600}),
        easing: 'easeOutElastic(1, .8)'
      });

      // Add 3D hover effect to service cards
      document.querySelectorAll('.service-card').forEach(card => {
        card.addEventListener('mouseenter', () => {
          anime({
            targets: card,
            scale: 1.05,
            rotateY: 5,
            rotateX: -5,
            duration: 400,
            easing: 'easeOutQuad'
          });
        });

        card.addEventListener('mouseleave', () => {
          anime({
            targets: card,
            scale: 1,
            rotateY: 0,
            rotateX: 0,
            duration: 400,
            easing: 'easeOutQuad'
          });
        });
      });

      // Feature boxes
      anime({
        targets: '.feature-box',
        translateY: [60, 0],
        opacity: [0, 1],
        duration: 800,
        delay: anime.stagger(100, {start: 800}),
        easing: 'easeOutQuad'
      });

      // Badges animation
      anime({
        targets: '.badge',
        scale: [0, 1],
        opacity: [0, 1],
        duration: 600,
        delay: anime.stagger(50),
        easing: 'easeOutElastic(1, .6)'
      });

      // Stats counter with anime.js
      document.querySelectorAll('.stat-number').forEach(stat => {
        const text = stat.textContent;
        const hasPlus = text.includes('+');
        const hasPercent = text.includes('%');
        const hasSlash = text.includes('/');
        const number = parseInt(text.replace(/\D/g, ''));

        if (!isNaN(number)) {
          const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
              if (entry.isIntersecting) {
                anime({
                  targets: { value: 0 },
                  value: number,
                  duration: 2000,
                  round: 1,
                  easing: 'easeOutExpo',
                  update: function(anim) {
                    let val = Math.ceil(anim.animations[0].currentValue);
                    if (hasPlus) val += '+';
                    if (hasPercent) val += '%';
                    if (hasSlash) val += '/7';
                    stat.textContent = val;
                  }
                });
                observer.unobserve(entry.target);
              }
            });
          }, { threshold: 0.5 });
          
          observer.observe(stat);
        }
      });
    }

    // GSAP ScrollTrigger animations
    const navbar = document.querySelector('.navbar');
    if (navbar) {
      ScrollTrigger.create({
        start: 'top -50',
        end: 99999,
        toggleClass: { className: 'scrolled', targets: '.navbar' }
      });
    }

    gsap.utils.toArray('.section-title').forEach((title) => {
      gsap.from(title, {
        scrollTrigger: {
          trigger: title,
          start: 'top 85%',
          toggleActions: 'play none none reverse'
        },
        opacity: 0,
        y: 50,
        scale: 0.9,
        duration: 0.8,
        ease: 'power3.out'
      });
    });

    gsap.utils.toArray('.section-subtitle').forEach((subtitle) => {
      gsap.from(subtitle, {
        scrollTrigger: {
          trigger: subtitle,
          start: 'top 85%',
          toggleActions: 'play none none reverse'
        },
        opacity: 0,
        y: 30,
        duration: 0.8,
        delay: 0.2,
        ease: 'power3.out'
      });
    });

    // Partner cards
    const partnerCards = document.querySelectorAll('.partner-card');
    partnerCards.forEach((card, index) => {
      gsap.from(card, {
        scrollTrigger: {
          trigger: card,
          start: 'top 85%',
          toggleActions: 'play none none reverse'
        },
        opacity: 0,
        x: index % 2 === 0 ? -100 : 100,
        rotation: index % 2 === 0 ? -10 : 10,
        duration: 1,
        ease: 'power3.out'
      });
    });

    // CTA section
    const ctaSection = document.querySelector('.cta-section');
    if (ctaSection) {
      gsap.from('.cta-section h2', {
        scrollTrigger: {
          trigger: '.cta-section',
          start: 'top 80%',
          toggleActions: 'play none none reverse'
        },
        opacity: 0,
        scale: 0.9,
        y: 50,
        duration: 1,
        ease: 'back.out(1.7)'
      });

      gsap.from('.cta-section .lead', {
        scrollTrigger: {
          trigger: '.cta-section',
          start: 'top 80%',
          toggleActions: 'play none none reverse'
        },
        opacity: 0,
        y: 30,
        duration: 0.8,
        delay: 0.3,
        ease: 'power3.out'
      });

      gsap.from('.cta-section .btn', {
        scrollTrigger: {
          trigger: '.cta-section',
          start: 'top 80%',
          toggleActions: 'play none none reverse'
        },
        opacity: 0,
        y: 30,
        scale: 0.9,
        duration: 0.8,
        delay: 0.5,
        stagger: 0.15,
        ease: 'back.out(1.7)'
      });
    }

    // Stats section
    const statSection = document.querySelector('.stats-section');
    if (statSection) {
      gsap.from('.stat-item', {
        scrollTrigger: {
          trigger: '.stats-section',
          start: 'top 80%',
          toggleActions: 'play none none reverse'
        },
        opacity: 0,
        y: 50,
        scale: 0.8,
        duration: 0.8,
        stagger: 0.15,
        ease: 'power3.out'
      });
    }

    // Button hover effects with anime.js
    if (typeof anime !== 'undefined') {
      document.querySelectorAll('.btn').forEach(btn => {
        btn.addEventListener('mouseenter', () => {
          anime({
            targets: btn,
            scale: 1.05,
            duration: 300,
            easing: 'easeOutQuad'
          });
        });

        btn.addEventListener('mouseleave', () => {
          anime({
            targets: btn,
            scale: 1,
            duration: 300,
            easing: 'easeOutQuad'
          });
        });
      });
    }

    // Social links hover
    const socialLinks = document.querySelectorAll('.social-link');
    socialLinks.forEach(link => {
      link.addEventListener('mouseenter', () => {
        gsap.to(link, {
          y: -5,
          scale: 1.2,
          duration: 0.3,
          ease: 'power2.out'
        });
      });

      link.addEventListener('mouseleave', () => {
        gsap.to(link, {
          y: 0,
          scale: 1,
          duration: 0.3,
          ease: 'power2.out'
        });
      });
    });

    // Footer links
    const footerLinks = document.querySelectorAll('.footer-link');
    footerLinks.forEach(link => {
      link.addEventListener('mouseenter', () => {
        gsap.to(link, {
          x: 5,
          duration: 0.3,
          ease: 'power2.out'
        });
      });

      link.addEventListener('mouseleave', () => {
        gsap.to(link, {
          x: 0,
          duration: 0.3,
          ease: 'power2.out'
        });
      });
    });

    // Smooth scroll for anchor links
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
      link.addEventListener('click', function(e) {
        const href = this.getAttribute('href');
        if (href && href.startsWith('#')) {
          e.preventDefault();
          const target = document.querySelector(href);
          if (target) {
            lenis.scrollTo(target, {
              offset: -80,
              duration: 1.5
            });
          }
        }
      });
    });

    // Images fade in
    gsap.utils.toArray('img').forEach(img => {
      gsap.from(img, {
        scrollTrigger: {
          trigger: img,
          start: 'top 85%',
          toggleActions: 'play none none reverse'
        },
        opacity: 0,
        scale: 0.8,
        duration: 1,
        ease: 'power3.out'
      });
    });

    // Feature icons with magnetic effect
    document.querySelectorAll('.feature-icon').forEach(icon => {
      icon.addEventListener('mouseenter', () => {
        gsap.to(icon, {
          scale: 1.15,
          rotate: 10,
          duration: 0.4,
          ease: 'elastic.out(1, 0.3)'
        });
      });

      icon.addEventListener('mouseleave', () => {
        gsap.to(icon, {
          scale: 1,
          rotate: 0,
          duration: 0.4,
          ease: 'elastic.out(1, 0.3)'
        });
      });
    });
  }

  console.log('✨ Aura - Enhanced animations initialized with anime.js, GSAP & Three.js');
});
