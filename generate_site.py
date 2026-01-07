import json
import os
import shutil
from datetime import datetime

# Configuration
JSON_FILE = 'pool-service-website-structure.json'
CONTENT_JSON_FILE = 'all-service-pages-content.json'
LOCATION_CONTENT_JSON_FILE = 'location-pages-content.json'
ABOUT_CONTENT_JSON_FILE = 'about-page-content.json'
BLOG_CONTENT_JSON_FILE = 'pool-care-guide-content.json'
OUTPUT_DIR = 'site'
COMPANY_NAME = "Firewater Pools"
PHONE = "772-269-0249"
ASSETS_DIR = 'assets'
ADDRESS = "Based in Vero Beach"

# HTML Template
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-8W7LC1MCR2"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){{dataLayer.push(arguments);}}
      gtag('js', new Date());

      gtag('config', 'G-8W7LC1MCR2');
    </script>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{seo_title}</title>
    <meta name="description" content="{meta_description}">
    
    <!-- Critical CSS to prevent flash of unstyled content -->
    <style>
        body {{ font-family: 'Outfit', sans-serif; }}
        .hero-pattern {{
            background-color: #334155; 
            background-image: url("{hero_image_url}");
            background-blend-mode: multiply;
            background-size: cover;
            background-position: center;
        }}
        
        /* Desktop nav is hidden on mobile by default */
        @media (max-width: 767px) {{
            nav.md\:flex {{ display: none !important; }}
            .md\:inline-flex {{ display: none !important; }}
        }}

        /* Desktop nav is shown on desktop */
        @media (min-width: 768px) {{
            nav.md\:flex {{ display: flex !important; }}
            .md\:hidden {{ display: none !important; }}
            #mobile-menu {{ display: none !important; }}
        }}

        /* Prevent Dropdown Flash */
        .dropdown-menu {{
            visibility: hidden;
            opacity: 0;
            transform: translateY(-10px);
            transition: all 0.2s ease;
            position: absolute;
            z-index: 50;
        }}
        .group:hover .dropdown-menu {{
            visibility: visible;
            opacity: 1;
            transform: translateY(0);
        }}
        
        #mobile-menu {{
            display: none;
        }}
        #mobile-menu.active {{
            display: flex;
        }}
    </style>

    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {{
            theme: {{
                extend: {{
                    colors: {{
                        primary: '#2563eb',   // Blue 600 (Water)
                        secondary: '#dc2626', // Red 600 (Fire)
                        accent: '#1d4ed8',    // Blue 700
                        dark: '#0f172a',      // Slate 900
                    }},
                    fontFamily: {{
                        sans: ['Outfit', 'sans-serif'],
                    }}
                }}
            }}
        }}
    </script>
    
    <!-- Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    
    {schema_markup}
</head>
<body class="bg-slate-50 text-slate-800 flex flex-col min-h-screen">

    <!-- Header -->
    <header class="bg-white shadow-sm sticky top-0 z-50">
        <div class="container mx-auto px-4 py-4 flex justify-between items-center">
            <a href="/" class="text-2xl font-bold tracking-tight">
                <span class="text-secondary">Fire</span><span class="text-primary">water</span><span class="text-dark">Pools</span>
            </a>
            
            <nav class="hidden md:flex space-x-8 items-center">
                <a href="/" class="text-slate-600 hover:text-primary font-medium transition-colors">Home</a>
                <div class="relative group">
                    <button class="text-slate-600 hover:text-primary font-medium transition-colors flex items-center gap-1 py-4">
                        Services 
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg>
                    </button>
                    <div class="dropdown-menu left-0 mt-0 w-64 bg-white border border-slate-100 rounded-lg shadow-xl top-full">
                        <div class="py-1">
                            {services_dropdown}
                        </div>
                    </div>
                </div>
                
                <div class="relative group">
                    <button class="text-slate-600 hover:text-primary font-medium transition-colors flex items-center gap-1 py-4">
                        Locations 
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg>
                    </button>
                    <div class="dropdown-menu left-0 mt-0 w-64 bg-white border border-slate-100 rounded-lg shadow-xl top-full max-h-[80vh] overflow-y-auto">
                        <div class="py-1">
                            <a href="/service-areas/" class="block px-4 py-2 text-sm font-semibold text-slate-800 bg-slate-50 hover:bg-slate-100">All Locations</a>
                            {locations_dropdown}
                        </div>
                    </div>
                </div>

                <a href="/about/" class="text-slate-600 hover:text-primary font-medium transition-colors">About</a>
                <a href="/contact/" class="text-slate-600 hover:text-primary font-medium transition-colors">Contact</a>
            </nav>
            
            <a href="/free-estimate/" class="hidden md:inline-flex items-center justify-center px-6 py-2.5 border border-transparent text-sm font-semibold rounded-full text-white bg-primary hover:bg-secondary transition-all shadow-md hover:shadow-lg focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary">
                Get Free Estimate
            </a>
            
             <button id="mobile-menu-btn" class="md:hidden text-slate-600 focus:outline-none">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path></svg>
            </button>
        </div>
        
        <!-- Mobile Menu -->
        <div id="mobile-menu" class="md:hidden bg-white border-t border-slate-100 flex-col py-4 px-4 space-y-4 shadow-lg">
            <a href="/" class="text-slate-600 hover:text-primary font-medium">Home</a>
            <div class="border-b border-slate-50 pb-2">
                <p class="text-xs font-bold text-slate-400 uppercase tracking-widest mb-2">Services</p>
                <div class="grid grid-cols-1 gap-2 pl-2">
                    {services_dropdown}
                </div>
            </div>
             <div class="border-b border-slate-50 pb-2">
                <p class="text-xs font-bold text-slate-400 uppercase tracking-widest mb-2">Locations</p>
                <div class="grid grid-cols-1 gap-2 pl-2">
                    <a href="/service-areas/" class="text-slate-600 hover:text-primary py-1">All Locations</a>
                    {locations_dropdown}
                </div>
            </div>
            <a href="/about/" class="text-slate-600 hover:text-primary font-medium">About</a>
            <a href="/contact/" class="text-slate-600 hover:text-primary font-medium">Contact</a>
            <a href="/free-estimate/" class="bg-primary text-white text-center py-3 rounded-lg font-bold">Get Free Estimate</a>
        </div>
    </header>

    <script>
        // Mobile Menu Toggle
        const menuBtn = document.getElementById('mobile-menu-btn');
        const mobileMenu = document.getElementById('mobile-menu');
        
        if (menuBtn && mobileMenu) {{
            menuBtn.addEventListener('click', () => {{
                mobileMenu.classList.toggle('active');
            }});
        }}
    </script>

    <!-- Main Content -->
    <main class="flex-grow">
        <!-- Hero Section -->
        <section class="hero-pattern text-white py-32 md:py-48 relative">
            <div class="bg-gradient-to-t from-slate-900/60 to-transparent absolute inset-0"></div>
            <div class="container mx-auto px-4 relative z-10 text-center max-w-5xl mx-auto">
                <span class="inline-block py-1.5 px-4 rounded-full bg-white/10 backdrop-blur-sm border border-white/20 text-sm font-medium mb-8 animate-fade-in-up uppercase tracking-wider">
                    {badge_text}
                </span>
                <h1 class="text-5xl md:text-7xl font-bold mb-8 leading-tight tracking-tight drop-shadow-sm">{h1}</h1>
                <p class="text-xl md:text-2xl text-slate-100 mb-12 max-w-2xl mx-auto font-light leading-relaxed drop-shadow-sm">
                    {subheadline}
                </p>
                <div class="flex flex-col sm:flex-row gap-5 justify-center">
                    <a href="/free-estimate/" class="inline-flex items-center justify-center px-8 py-4 border border-transparent text-lg font-bold rounded-lg text-white bg-primary hover:bg-secondary transition-all shadow-xl hover:shadow-2xl hover:-translate-y-1">
                        Get Your Free Quote
                    </a>
                </div>
            </div>
        </section>

        {custom_content}
        
    </main>

    <!-- Footer -->
    <footer class="bg-dark text-slate-300 py-16 border-t border-slate-800">
        <div class="container mx-auto px-4">
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-12 mb-12">
                <!-- Column 1: Brand & Contact -->
                <div>
                    <a href="/" class="text-2xl font-bold tracking-tight mb-6 block">
                        <span class="text-secondary">Fire</span><span class="text-primary">water</span><span class="text-white">Pools</span>
                    </a>
                    <p class="text-slate-400 mb-8 leading-relaxed">Based in Vero Beach. Serving the Treasure Coast.</p>
                    
                    <ul class="space-y-4">
                        <li class="flex items-start">
                            <svg class="w-6 h-6 text-primary mr-3 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"></path><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"></path></svg>
                            <span>{address}</span>
                        </li>
                        <li class="flex items-center">
                            <svg class="w-6 h-6 text-primary mr-3 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"></path></svg>
                            <a href="tel:7722690249" class="hover:text-white transition-colors">{phone}</a>
                        </li>
                    </ul>
                </div>
                
                <!-- Column 2: Quick Links -->
                <div class="grid grid-cols-2 gap-8">
                    <div>
                        <h3 class="text-white font-semibold text-lg mb-6">Services</h3>
                        <ul class="space-y-3 text-sm">
                            {services_footer_list}
                        </ul>
                    </div>
                    <div>
                        <h3 class="text-white font-semibold text-lg mb-6">Company</h3>
                        <ul class="space-y-3 text-sm">
                            <li><a href="/about/" class="hover:text-primary transition-colors">About Us</a></li>
                            <li><a href="/service-areas/" class="hover:text-primary transition-colors">Service Areas</a></li>
                            <li><a href="/pool-care-guide/" class="hover:text-primary transition-colors">Pool Care Guide</a></li>
                            <li><a href="/contact/" class="hover:text-primary transition-colors">Contact</a></li>
                        </ul>
                    </div>
                </div>

                <!-- Column 3: Map -->
                <div>
                    <h3 class="text-white font-semibold text-lg mb-6">Our Location</h3>
                    <div class="rounded-xl overflow-hidden shadow-2xl h-80 border border-slate-800">
                        <iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d452585.4171060544!2d-80.4594995!3d27.598998950000002!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x29e4d190fa91bbb9%3A0xb30cef7fe8911386!2sFireWater%20Pool%20and%20Spa!5e0!3m2!1sen!2sca!4v1767312285533!5m2!1sen!2sca" width="100%" height="100%" style="border:0;" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
                    </div>
                </div>
            </div>
            
            </div>
        </div>
    </footer>

    {sticky_call_button}
</body>
</html>
"""

def generate_schema_markup(page_data, is_home=False):
    if not is_home:
        return ""
        
    schema = {
      "@context": "https://schema.org",
      "@type": "LocalBusiness",
      "name": COMPANY_NAME,
      "image": "https://images.unsplash.com/photo-1576013551627-0cc20b96c2a7?ixlib=rb-1.2.1",
      "telephone": PHONE,
      "url": "https://www.firewaterpools.com/",
      "priceRange": "$$",
      "address": {
        "@type": "PostalAddress",
        "addressLocality": "Vero Beach",
        "addressRegion": "FL",
        "addressCountry": "US"
      },
      "geo": {
        "@type": "GeoCoordinates",
        "latitude": "27.6386",
        "longitude": "-80.3973"
      },
      "openingHoursSpecification": {
        "@type": "OpeningHoursSpecification",
        "dayOfWeek": [
          "Monday",
          "Tuesday",
          "Wednesday",
          "Thursday",
          "Friday"
        ],
        "opens": "08:00",
        "closes": "18:00"
      },
      "areaServed": [
        {
          "@type": "City",
          "name": "Vero Beach",
          "sameAs": "https://en.wikipedia.org/wiki/Vero_Beach,_Florida"
        },
        {
          "@type": "AdministrativeArea",
          "name": "Indian River County",
          "sameAs": "https://en.wikipedia.org/wiki/Indian_River_County,_Florida"
        }
      ]
    }
    return f'<script type="application/ld+json">\n{json.dumps(schema, indent=2)}\n</script>'

def generate_detailed_service_content(content_data):
    html = ""
    
    # 1. Problem Statement
    if 'problemStatement' in content_data:
        html += f"""
        <section class="py-16 bg-white">
            <div class="container mx-auto px-4 max-w-4xl text-center">
                <p class="text-xl md:text-2xl text-slate-700 leading-relaxed font-light">
                    "{content_data['problemStatement']}"
                </p>
                <div class="w-16 h-1 bg-primary mx-auto mt-8 rounded-full"></div>
            </div>
        </section>
        """

    # 1.5 Local Owner Section
    if 'localOwner' in content_data:
        owner = content_data['localOwner']
        html += f"""
        <section class="py-20 bg-slate-50 border-y border-slate-100">
            <div class="container mx-auto px-4 max-w-6xl">
                <div class="flex flex-col md:flex-row gap-16 items-center">
                    <div class="md:w-3/5 text-center">
                        <img src="{owner.get('image', '/images/kevin-new.jpg')}" alt="{owner.get('name', 'Kevin')}" class="rounded-2xl shadow-2xl w-full object-cover">
                    </div>
                    <div class="md:w-2/5 text-left">
                        <h2 class="text-4xl font-bold text-slate-900 mb-6 leading-tight">{owner.get('h2', 'Meet the Owner')}</h2>
                        <div class="w-20 h-1 bg-primary rounded-full mb-8"></div>
                        <p class="text-slate-700 leading-relaxed text-lg mb-8">{owner.get('bio', '')}</p>
                        <div class="mt-8">
                            <a href="tel:7722690249" class="inline-flex items-center justify-center px-8 py-4 bg-primary text-white text-lg font-bold rounded-lg hover:bg-secondary transition-all shadow-lg hover:shadow-xl hover:-translate-y-1">
                                Call Kevin
                                <svg class="w-5 h-5 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"></path></svg>
                            </a>
                        </div>
                    </div>
                </div>
            </div>
        </section>
        """

    # 2. Service Details (What's Included)
    if 'serviceDetails' in content_data:
        includes = content_data['serviceDetails'].get('includes', [])
        includes_html = "".join([f'<li class="flex items-start"><svg class="w-6 h-6 text-green-500 mr-3 mt-1 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg><span class="text-slate-700 text-lg">{item}</span></li>' for item in includes])
        
        details_img = content_data.get('detailsImage', {})
        details_src = details_img.get('src', 'https://images.unsplash.com/photo-1572331165267-854da2b00dc1?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80')
        details_alt = details_img.get('alt', 'Pool Service Details')
        
        html += f"""
        <section class="py-20 bg-slate-50">
            <div class="container mx-auto px-4">
                <div class="flex flex-col md:flex-row gap-12 items-center">
                    <div class="md:w-1/2">
                        <img src="{details_src}" alt="{details_alt}" class="rounded-2xl shadow-xl">
                    </div>
                    <div class="md:w-1/2">
                        <h2 class="text-3xl font-bold text-slate-900 mb-4">{content_data['serviceDetails'].get('h2', 'What is included')}</h2>
                        <p class="text-lg text-slate-600 mb-8">{content_data['serviceDetails'].get('intro', '')}</p>
                        <ul class="space-y-4">
                            {includes_html}
                        </ul>
                    </div>
                </div>
            </div>
        </section>
        """

    # 3. Service Options (Pricing/Plans)
    if 'serviceOptions' in content_data:
        options = content_data['serviceOptions'].get('options', [])
        hide_buttons = content_data['serviceOptions'].get('hideButtons', False)
        options_cards = ""
        for opt in options:
            btn_html = ""
            if not hide_buttons:
                btn_html = f'<a href="/free-estimate/" class="block w-full py-3 px-6 bg-slate-100 hover:bg-primary hover:text-white text-slate-700 font-bold rounded-lg text-center transition-colors">Get Quote</a>'
            
            options_cards += f"""
            <div class="bg-white p-8 rounded-xl shadow-md border border-slate-100 hover:shadow-xl transition-all hover:border-primary group">
                <h3 class="text-2xl font-bold text-slate-900 mb-2">{opt['name']}</h3>
                <div class="text-primary font-semibold text-lg mb-4 bg-blue-50 inline-block px-3 py-1 rounded-full">{opt['frequency']}</div>
                <p class="text-slate-600 mb-6">Best for: <span class="font-medium text-slate-800">{opt['bestFor']}</span></p>
                {btn_html}
            </div>
            """
            
        ctas_html = ""
        if 'ctas' in content_data['serviceOptions']:
            ctas_html = '<div class="flex flex-wrap justify-center gap-4 mt-12">'
            for cta in content_data['serviceOptions']['ctas']:
                bg_color = "bg-primary" if cta.get('primary', True) else "bg-slate-700"
                ctas_html += f"""
                <a href="{cta['url']}" class="inline-flex items-center justify-center px-8 py-4 border border-transparent text-lg font-bold rounded-lg text-white {bg_color} hover:bg-secondary transition-all shadow-xl hover:shadow-2xl hover:-translate-y-1">
                    {cta['text']}
                </a>
                """
            ctas_html += '</div>'

        html += f"""
        <section class="py-20 bg-white">
            <div class="container mx-auto px-4">
                <div class="text-center max-w-3xl mx-auto mb-16">
                    <h2 class="text-3xl font-bold text-slate-900 mb-4">{content_data['serviceOptions'].get('h2', 'Our Plans')}</h2>
                    <p class="text-lg text-slate-600">{content_data['serviceOptions'].get('intro', '')}</p>
                </div>
                <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
                    {options_cards}
                </div>
                {ctas_html}
                <p class="text-center text-slate-500 mt-8 italic text-sm">{content_data['serviceOptions'].get('pricingNote', '')}</p>
            </div>
        </section>
        """

    # 4. Local Proof
    if 'localProof' in content_data:
        lp_ctas_html = ""
        if 'ctas' in content_data['localProof']:
            lp_ctas_html = '<div class="flex flex-wrap justify-center gap-4 mt-8">'
            for cta in content_data['localProof']['ctas']:
                bg_color = "bg-primary" if cta.get('primary', True) else "bg-slate-700"
                lp_ctas_html += f"""
                <a href="{cta['url']}" class="inline-flex items-center justify-center px-8 py-4 border border-transparent text-lg font-bold rounded-lg text-white {bg_color} hover:bg-secondary transition-all shadow-xl hover:shadow-2xl hover:-translate-y-1">
                    {cta['text']}
                </a>
                """
            lp_ctas_html += '</div>'

        html += f"""
        <section class="py-20 bg-dark text-white relative overflow-hidden">
            <div class="absolute inset-0 bg-primary/10"></div>
            <div class="container mx-auto px-4 relative z-10 text-center max-w-3xl">
                <h2 class="text-3xl font-bold mb-6">{content_data['localProof'].get('h2', 'Serving Vero Beach')}</h2>
                <p class="text-xl text-slate-300 leading-relaxed">
                    {content_data['localProof'].get('content', '')}
                </p>
                {lp_ctas_html}
            </div>
        </section>
        """

    # 5. Testimonials
    if 'testimonials' in content_data:
        testimonials = content_data.get('testimonials', [])
        test_cards = ""
        for t in testimonials:
            test_cards += f"""
            <div class="bg-slate-50 p-8 rounded-xl relative">
                <div class="text-yellow-400 text-2xl mb-4">★★★★★</div>
                <p class="text-slate-600 mb-6 italic">"{t['quote']}"</p>
                <div>
                    <p class="font-bold text-slate-900">{t['author']}</p>
                    <p class="text-sm text-slate-500">{t['location']}</p>
                </div>
            </div>
            """
            
        google_review_widget = ""
        if content_data.get('googleReviewsLink'):
            link = content_data['googleReviewsLink']
            google_review_widget = f"""
            <div class="col-span-full flex justify-center mt-12">
                <a href="{link}" target="_blank" rel="noopener" class="inline-flex items-center gap-4 bg-white border border-slate-200 p-6 rounded-2xl shadow-sm hover:shadow-md transition-all group w-full max-w-md">
                    <div class="w-8 h-8 flex-shrink-0">
                        <svg viewBox="0 0 48 48" class="w-full h-full"><path fill="#EA4335" d="M24 9.5c3.54 0 6.71 1.22 9.21 3.6l6.85-6.85C35.9 2.38 30.47 0 24 0 14.62 0 6.51 5.38 2.56 13.22l7.98 6.19C12.43 13.72 17.74 9.5 24 9.5z"></path><path fill="#4285F4" d="M46.98 24.55c0-1.57-.15-3.09-.38-4.55H24v9.02h12.94c-.58 2.96-2.26 5.48-4.78 7.18l7.73 6c4.51-4.18 7.09-10.36 7.09-17.65z"></path><path fill="#FBBC05" d="M10.53 28.59c-.48-1.45-.76-2.99-.76-4.59s.27-3.14.76-4.59l-7.98-6.19C.92 16.46 0 20.12 0 24c0 3.88.92 7.54 2.56 10.78l7.97-6.19z"></path><path fill="#34A853" d="M24 48c6.48 0 11.93-2.13 15.89-5.81l-7.73-6c-2.15 1.45-4.92 2.3-8.16 2.3-6.26 0-11.57-4.22-13.47-9.91l-7.98 6.19C6.51 42.62 14.62 48 24 48z"></path><path fill="none" d="M0 0h48v48H0z"></path></svg>
                    </div>
                    <div class="text-left">
                        <div class="flex items-center gap-1 text-yellow-400 text-xs mb-0.5">
                            ★★★★★
                        </div>
                        <p class="text-slate-900 font-bold text-sm group-hover:text-primary transition-colors">See all 5-Star Google Reviews</p>
                    </div>
                    <svg class="w-4 h-4 text-slate-300 group-hover:text-primary transition-colors ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7-7 7"></path></svg>
                </a>
            </div>
            """

        html += f"""
        <section class="py-20 bg-white">
            <div class="container mx-auto px-4">
                 <h2 class="text-3xl font-bold text-slate-900 mb-12 text-center">What Your Neighbors Say</h2>
                <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
                    {test_cards}
                    {google_review_widget}
                </div>
            </div>
        </section>
        """

    # 6. FAQ
    if 'faq' in content_data:
        questions = content_data['faq'].get('questions', [])
        faq_items = ""
        for q in questions:
            faq_items += f"""
            <div class="border-b border-slate-200 py-6">
                <h3 class="text-lg font-bold text-slate-900 mb-2">{q['question']}</h3>
                <p class="text-slate-600 leading-relaxed">{q['answer']}</p>
            </div>
            """
            
        html += f"""
        <section class="py-20 bg-slate-50">
            <div class="container mx-auto px-4 max-w-3xl">
                <h2 class="text-3xl font-bold text-slate-900 mb-12 text-center">{content_data['faq'].get('h2', 'Frequently Asked Questions')}</h2>
                <div class="bg-white rounded-2xl p-8 shadow-sm">
                    {faq_items}
                </div>
            </div>
        </section>
        """

    # 7. Final CTA
    if 'finalCTA' in content_data:
        html += f"""
        <section class="py-24 bg-primary text-white text-center">
            <div class="container mx-auto px-4">
                <h2 class="text-3xl md:text-5xl font-bold mb-6">{content_data['finalCTA'].get('h2', 'Ready to get started?')}</h2>
                <p class="text-xl text-white/90 mb-10 max-w-2xl mx-auto">{content_data['finalCTA'].get('content', '')}</p>
                <a href="/free-estimate/" class="inline-flex items-center justify-center px-8 py-4 bg-white text-primary text-lg font-bold rounded-lg hover:bg-secondary hover:text-white transition-all shadow-xl hover:shadow-2xl hover:-translate-y-1">
                    Get Free Estimate
                </a>
            </div>
        </section>
        """

    return html

def generate_about_content(content_data):
    """
    Generates HTML content for the About page based on the provided JSON data.
    """
    html = ""
    about_data = content_data.get('aboutPage', {})

    # 1. Hero Section (Custom for About)
    if 'hero' in about_data:
        hero = about_data['hero']
        html += f"""
        <section class="relative bg-slate-900 text-white py-32 md:py-48 overflow-hidden">
            <div class="absolute inset-0 z-0">
                <img src="{hero.get('heroImage', {}).get('src', '')}" alt="{hero.get('heroImage', {}).get('alt', '')}" class="w-full h-full object-cover opacity-30">
                <div class="absolute inset-0 bg-gradient-to-t from-slate-900 via-slate-900/50 to-transparent"></div>
            </div>
            <div class="container mx-auto px-4 relative z-10 text-center max-w-4xl">
                {'<span class="inline-flex items-center px-4 py-2 rounded-full bg-yellow-500/20 border border-yellow-500/50 text-yellow-400 font-bold mb-8 uppercase tracking-wider text-sm"><svg class="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 20 20"><path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/></svg>' + hero['badge'] + '</span>' if 'badge' in hero else ''}
                <h1 class="text-4xl md:text-6xl font-bold mb-6 leading-tight">{hero.get('h1', '')}</h1>
                <p class="text-xl md:text-2xl text-slate-200 font-light leading-relaxed max-w-2xl mx-auto">{hero.get('subheadline', '')}</p>
            </div>
        </section>
        """

    # 2. Owner Story Section
    if 'story' in about_data:
        story = about_data['story']
        paragraphs = story.get('content', [])
        p_html = "".join([f'<p class="text-lg text-slate-600 mb-6 leading-relaxed">{p}</p>' for p in paragraphs])
        
        html += f"""
        <section class="py-24 bg-white">
            <div class="container mx-auto px-4">
                <div class="flex flex-col md:flex-row gap-16 items-center">
                     <div class="md:w-1/2 relative">
                        <div class="absolute -top-4 -left-4 w-32 h-32 bg-primary/10 rounded-tl-3xl -z-10"></div>
                        <div class="absolute -bottom-4 -right-4 w-32 h-32 bg-slate-100 rounded-br-3xl -z-10"></div>
                        <img src="{story.get('image', {}).get('src', '')}" alt="{story.get('image', {}).get('alt', '')}" class="rounded-xl shadow-2xl relative z-10 w-full h-auto">
                        
                         <div class="absolute bottom-8 left-8 bg-white/95 backdrop-blur-sm p-6 rounded-lg shadow-lg max-w-xs border-l-4 border-primary">
                            <p class="font-bold text-slate-900 text-lg">Kevin</p>
                            <p class="text-slate-500 text-sm uppercase tracking-wide">{story.get('h3', 'Owner')}</p>
                        </div>
                    </div>
                    <div class="md:w-1/2">
                        <h2 class="text-4xl font-bold text-slate-900 mb-8 relative inline-block">
                            {story.get('h2', 'Our Story')}
                            <span class="absolute bottom-0 left-0 w-1/3 h-2 bg-primary/20 -mb-2"></span>
                        </h2>
                        {p_html}
                        <div class="mt-8">
                            <a href="tel:{PHONE.replace('-', '')}" class="inline-flex items-center justify-center px-8 py-4 bg-primary text-white text-lg font-bold rounded-lg hover:bg-secondary transition-all shadow-lg hover:shadow-xl hover:-translate-y-1">
                                Call Kevin
                                <svg class="w-5 h-5 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"></path></svg>
                            </a>
                        </div>
                    </div>
                </div>
            </div>
        </section>
        """

    # 3. Values Section
    if 'values' in about_data:
        values = about_data['values']
        cards_html = ""
        for item in values.get('items', []):
            icon_html = "" # Add logic to pick icon based on name if needed, or generic
            if item.get('icon') == 'shield-check':
                icon_html = '<svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>'
            elif item.get('icon') == 'clock':
                icon_html = '<svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>'
            elif item.get('icon') == 'star':
                icon_html = '<svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"></path></svg>'
            elif item.get('icon') == 'hand-heart':
                icon_html = '<svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"></path></svg>'
            else: 
                icon_html = '<svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>' # fallback

            cards_html += f"""
            <div class="bg-white p-8 rounded-2xl shadow-sm border border-slate-100 hover:shadow-lg transition-all hover:-translate-y-1">
                <div class="w-16 h-16 bg-primary rounded-xl flex items-center justify-center mb-6 shadow-lg shadow-primary/30">
                    {icon_html}
                </div>
                <h3 class="text-xl font-bold text-slate-900 mb-3">{item['title']}</h3>
                <p class="text-slate-600 leading-relaxed">{item['description']}</p>
            </div>
            """
        
        html += f"""
        <section class="py-24 bg-slate-50">
            <div class="container mx-auto px-4">
                <div class="text-center max-w-3xl mx-auto mb-16">
                    <h2 class="text-3xl font-bold text-slate-900 mb-4">{values.get('h2', 'Our Values')}</h2>
                    <p class="text-lg text-slate-600">{values.get('intro', '')}</p>
                </div>
                <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
                    {cards_html}
                </div>
            </div>
        </section>
        """

    # 4. Credentials Section
    if 'credentials' in about_data:
        creds = about_data['credentials']
        items_html = "".join([f'<div class="flex items-center bg-white px-6 py-4 rounded-full shadow-sm border border-slate-100"><svg class="w-6 h-6 text-green-500 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg><span class="font-semibold text-slate-700">{item}</span></div>' for item in creds.get('items', [])])
        
        html += f"""
        <section class="py-20 bg-white">
            <div class="container mx-auto px-4 text-center">
                 <h2 class="text-2xl font-bold text-slate-900 mb-10">{creds.get('h2', 'Credentials')}</h2>
                 <div class="flex flex-wrap gap-4 justify-center">
                    {items_html}
                 </div>
            </div>
        </section>
        """
        
    # 4.5 External Links Section
    html += f"""
    <section class="py-16 bg-slate-50 border-t border-b border-slate-100">
        <div class="container mx-auto px-4 text-center">
            <h2 class="text-3xl font-bold text-slate-900 mb-12">Verify & Connect</h2>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-5xl mx-auto">
                <!-- Google Maps -->
                <a href="https://maps.app.goo.gl/rxz38GoVW1M49ujMA" target="_blank" rel="noopener" class="bg-white p-8 rounded-2xl shadow-sm hover:shadow-xl transition-all border border-slate-100 group h-full flex flex-col items-center">
                    <div class="w-14 h-14 bg-blue-50 rounded-xl flex items-center justify-center text-primary mb-6 group-hover:bg-primary group-hover:text-white transition-colors">
                        <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"></path><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"></path></svg>
                    </div>
                    <h3 class="text-xl font-bold text-slate-900 mb-2">Find Us on Maps</h3>
                    <p class="text-slate-500 mb-6 text-sm flex-grow">View our service area and leave a review.</p>
                    <span class="text-primary font-bold inline-flex items-center text-sm">Open in Google Maps <svg class="w-4 h-4 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"></path></svg></span>
                </a>

                <!-- Sunbiz -->
                <a href="https://search.sunbiz.org/Inquiry/CorporationSearch/SearchResultDetail?inquirytype=EntityName&directionType=Initial&searchNameOrder=FIREWATERPOOLS%20L230003438120&aggregateId=flal-l23000343812-b586057c-ce35-4dfe-b1ba-c65c0e08b377&searchTerm=Firewater%20Media%20Group%2C%20Inc&listNameOrder=FIREWATERMEDIAGROUP%20F100000012770" target="_blank" rel="noopener" class="bg-white p-8 rounded-2xl shadow-sm hover:shadow-xl transition-all border border-slate-100 group h-full flex flex-col items-center">
                    <div class="w-14 h-14 bg-orange-50 rounded-xl flex items-center justify-center text-orange-600 mb-6 group-hover:bg-orange-600 group-hover:text-white transition-colors">
                        <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"></path></svg>
                    </div>
                    <h3 class="text-xl font-bold text-slate-900 mb-2">Registered Business</h3>
                    <p class="text-slate-500 mb-6 text-sm flex-grow">Sunbiz.org Department of State Registration.</p>
                    <span class="text-orange-600 font-bold inline-flex items-center text-sm">Verify on Sunbiz <svg class="w-4 h-4 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"></path></svg></span>
                </a>

                <!-- Facebook -->
                <a href="https://www.facebook.com/p/Firewater-Pools-61570917715549/" target="_blank" rel="noopener" class="bg-white p-8 rounded-2xl shadow-sm hover:shadow-xl transition-all border border-slate-100 group h-full flex flex-col items-center">
                    <div class="w-14 h-14 bg-indigo-50 rounded-xl flex items-center justify-center text-indigo-600 mb-6 group-hover:bg-indigo-600 group-hover:text-white transition-colors">
                        <svg class="w-8 h-8" fill="currentColor" viewBox="0 0 24 24"><path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/></svg>
                    </div>
                    <h3 class="text-xl font-bold text-slate-900 mb-2">Follow on Facebook</h3>
                    <p class="text-slate-500 mb-6 text-sm flex-grow">Stay updated with our latest pool projects.</p>
                    <span class="text-indigo-600 font-bold inline-flex items-center text-sm">View Profile <svg class="w-4 h-4 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"></path></svg></span>
                </a>
            </div>
        </div>
    </section>
    """
        
    # 5. Testimonials (Cards)
    if 'testimonials' in about_data:
        testis = about_data['testimonials']
        cards_html = ""
        for item in testis.get('items', []):
            cards_html += f"""
            <div class="bg-slate-50 p-8 rounded-2xl relative border border-slate-100">
                <div class="text-yellow-400 flex mb-4">
                    <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20"><path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/></svg>
                    <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20"><path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/></svg>
                    <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20"><path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/></svg>
                    <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20"><path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/></svg>
                    <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20"><path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/></svg>
                </div>
                <p class="text-slate-700 italic mb-6 leading-relaxed">"{item['quote']}"</p>
                <div class="flex items-center">
                     <div class="w-10 h-10 rounded-full bg-slate-200 flex items-center justify-center text-slate-500 font-bold mr-3">{item['author'][0]}</div>
                     <div>
                        <p class="font-bold text-slate-900 text-sm">{item['author']}</p>
                        <p class="text-slate-500 text-xs">{item['location']}</p>
                     </div>
                </div>
            </div>
            """
        
        html += f"""
        <section class="py-24 bg-white">
            <div class="container mx-auto px-4">
                 <h2 class="text-3xl font-bold text-slate-900 mb-12 text-center">{testis.get('h2', 'What Our Neighbors Say')}</h2>
                 <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
                    {cards_html}
                 </div>
            </div>
        </section>
        """

    # 6. Final CTA
    if 'finalCTA' in about_data:
        cta = about_data['finalCTA']
        html += f"""
        <section class="py-24 bg-primary text-white text-center">
            <div class="container mx-auto px-4 max-w-3xl">
                <h2 class="text-3xl md:text-5xl font-bold mb-8">{cta.get('h2', '')}</h2>
                <p class="text-xl text-white/90 mb-12 leading-relaxed">{cta.get('content', '')}</p>
                
                <a href="/free-estimate/" class="inline-flex items-center justify-center px-8 py-4 bg-white text-primary text-lg font-bold rounded-lg hover:bg-secondary hover:text-white transition-all shadow-xl hover:shadow-2xl hover:-translate-y-1">
                    {cta.get('buttonText', 'Contact Us')}
                </a>
            </div>
        </section>
        """

    return html

def generate_location_content(content_data, page_type='location'):
    html = ""
    
    # Hero is handled by the template, but we can access custom hero fields if needed
    
    # 1. Local Intro
    if 'localIntro' in content_data:
        intro_text = content_data['localIntro']
        if isinstance(intro_text, dict):
            intro_text = intro_text.get('content', '')
            
        paragraphs = intro_text.split('\n\n')
        p_html = "".join([f'<p class="text-lg text-slate-600 mb-6 leading-relaxed">{p}</p>' for p in paragraphs])
        
        html += f"""
        <section class="py-20 bg-white">
            <div class="container mx-auto px-4 max-w-4xl">
                {p_html}
            </div>
        </section>
        """

    # 1.5 Local Owner Section
    if 'localOwner' in content_data:
        owner = content_data['localOwner']
        html += f"""
        <section class="py-20 bg-slate-50 border-y border-slate-100">
            <div class="container mx-auto px-4 max-w-6xl">
                <div class="flex flex-col md:flex-row gap-16 items-center">
                    <div class="md:w-3/5 text-center">
                        <img src="{owner.get('image', '/images/kevin-new.jpg')}" alt="{owner.get('name', 'Kevin')}" class="rounded-2xl shadow-2xl w-full object-cover">
                    </div>
                    <div class="md:w-2/5 text-left">
                        <h2 class="text-4xl font-bold text-slate-900 mb-6 leading-tight">{owner.get('h2', 'Meet the Owner')}</h2>
                        <div class="w-20 h-1 bg-primary rounded-full mb-8"></div>
                        <p class="text-xl text-slate-600 mb-8 leading-relaxed italic">{owner.get('quote', '')}</p>
                        <p class="text-slate-700 leading-relaxed text-lg">{owner.get('bio', '')}</p>
                    </div>
                </div>
            </div>
        </section>
        """

    # 2. Services in Area
    if 'servicesInArea' in content_data:
        section_data = content_data['servicesInArea']
        services = section_data.get('services', [])
        
        services_html = ""
        for s in services:
            link_html = ""
            if s.get('url') and not content_data.get('hideLearnMore', False):
                link_html = f"""
                <a href="{s['url']}" class="text-primary font-medium hover:text-secondary text-sm inline-flex items-center">
                    Learn more <svg class="w-3 h-3 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path></svg>
                </a>
                """
            
            services_html += f"""
            <div class="bg-slate-50 p-6 rounded-xl border border-slate-100 hover:shadow-md transition-shadow">
                <h3 class="text-xl font-bold text-slate-900 mb-2">{s['name']}</h3>
                <p class="text-slate-600 mb-4 text-sm">{s['description']}</p>
                {link_html}
            </div>
            """
        
        ctas_html = ""
        if 'ctas' in section_data:
            ctas_html = '<div class="flex flex-wrap justify-center gap-4 mt-12">'
            for cta in section_data['ctas']:
                bg_color = "bg-primary" if cta.get('primary', True) else "bg-slate-700"
                ctas_html += f"""
                <a href="{cta['url']}" class="inline-flex items-center justify-center px-8 py-4 border border-transparent text-lg font-bold rounded-lg text-white {bg_color} hover:bg-secondary transition-all shadow-xl hover:shadow-2xl hover:-translate-y-1">
                    {cta['text']}
                </a>
                """
            ctas_html += '</div>'
            
        html += f"""
        <section class="py-20 bg-white border-t border-slate-100">
            <div class="container mx-auto px-4">
                <div class="text-center max-w-3xl mx-auto mb-12">
                    <h2 class="text-3xl font-bold text-slate-900 mb-4">{section_data.get('h2', 'Services in Your Area')}</h2>
                    <p class="text-lg text-slate-600">{section_data.get('intro', '')}</p>
                </div>
                <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {services_html}
                </div>
                {ctas_html}
            </div>
        </section>
        """

    # 3. Local Knowledge / Why Choose Us
    if 'localKnowledge' in content_data:
        lk = content_data['localKnowledge']
        bullets = lk.get('bullets', [])
        bullets_html = "".join([f'<li class="flex items-center text-slate-700"><svg class="w-5 h-5 text-green-500 mr-3 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>{b}</li>' for b in bullets])
        
        html += f"""
        <section class="py-20 bg-slate-50">
            <div class="container mx-auto px-4">
                <div class="flex flex-col md:flex-row gap-12 items-center">
                    <div class="md:w-1/2 order-2 md:order-1">
                         <div class="relative">
                            <div class="absolute -top-4 -left-4 w-24 h-24 bg-primary/10 rounded-full z-0"></div>
                            <img src="https://images.unsplash.com/photo-1540541338287-41700207dee6?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80" alt="Local Pool Service" class="rounded-2xl shadow-xl relative z-10 w-full">
                        </div>
                    </div>
                    <div class="md:w-1/2 order-1 md:order-2">
                        <h2 class="text-3xl font-bold text-slate-900 mb-6">{lk.get('h2', 'Why Choose Us')}</h2>
                        <p class="text-lg text-slate-600 mb-8 leading-relaxed">{lk.get('content', '')}</p>
                        <ul class="space-y-4">
                            {bullets_html}
                        </ul>
                    </div>
                </div>
            </div>
        </section>
        """

    # 4. Neighborhoods
    if 'neighborhoodsServed' in content_data:
        ns = content_data['neighborhoodsServed']
        hoods = ns.get('neighborhoods', [])
        hoods_details = ns.get('neighborhoodsDetails', [])
        
        neighborhoods_html = ""
        if hoods_details:
            # Use grid for details
            grid_items = ""
            for detail in hoods_details:
                grid_items += f"""
                <div class="bg-white p-6 rounded-xl shadow-sm border border-slate-100">
                    <h3 class="text-xl font-bold text-slate-900 mb-3">{detail['name']}</h3>
                    <p class="text-slate-600 text-sm leading-relaxed">{detail['detail']}</p>
                </div>
                """
            neighborhoods_html = f"""
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                {grid_items}
            </div>
            """
        else:
            # Traditional list
            mid = (len(hoods) + 1) // 2
            col1 = hoods[:mid]
            col2 = hoods[mid:]
            
            def make_list(items):
                return "".join([f'<li class="flex items-center text-slate-600 mb-2"><span class="w-1.5 h-1.5 bg-primary rounded-full mr-2"></span>{item}</li>' for item in items])
                
            neighborhoods_html = f"""
            <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
                <ul class="space-y-1">
                    {make_list(col1)}
                </ul>
                <ul class="space-y-1">
                    {make_list(col2)}
                </ul>
            </div>
            """
            
        map_html = ""
        if ns.get('mapEmbed'):
            map_html = f"""
            <div class="mt-10 rounded-xl overflow-hidden shadow-lg h-96 border border-slate-200">
                {ns['mapEmbed'].replace('width="600"', 'width="100%"').replace('height="450"', 'height="100%"')}
            </div>
            """
            
        zip_html = ""
        if ns.get('zipCodes'):
            zip_tags = " ".join([f'<span class="text-sm font-semibold text-primary bg-blue-100 px-3 py-1 rounded-full text-slate-600">{z}</span>' for z in ns['zipCodes']])
            zip_html = f'<div class="flex flex-wrap justify-center gap-2 mb-4">{zip_tags}</div>'

        html += f"""
        <section class="py-20 bg-white">
            <div class="container mx-auto px-4 max-w-4xl">
                <div class="bg-blue-50 rounded-2xl p-8 md:p-12">
                    <div class="text-center mb-10">
                        <h2 class="text-3xl font-bold text-slate-900 mb-4">{ns.get('h2', 'Neighborhoods We Serve')}</h2>
                        <p class="text-lg text-slate-600 mb-4">{ns.get('content', '')}</p>
                        {zip_html}
                    </div>
                    {neighborhoods_html}
                    {map_html}
                    <p class="text-center text-slate-500 mt-8 text-sm italic">{ns.get('closingNote', '')}</p>
                </div>
            </div>
        </section>
        """

    # 4.5 Local Tips (Water Conditions, etc.)
    if 'localTips' in content_data:
        tips = content_data['localTips']
        tips_html = ""
        for tip in tips:
            tips_html += f"""
            <div class="bg-amber-50 border-l-4 border-amber-400 p-6 rounded-r-xl shadow-sm">
                <div class="flex">
                    <div class="flex-shrink-0">
                        <svg class="h-6 w-6 text-amber-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                    </div>
                    <div class="ml-4">
                        <h3 class="text-lg font-bold text-amber-900 mb-2">{tip['title']}</h3>
                        <p class="text-amber-800 leading-relaxed">{tip['content']}</p>
                    </div>
                </div>
            </div>
            """
        
        html += f"""
        <section class="py-16 bg-white border-t border-slate-100">
            <div class="container mx-auto px-4 max-w-4xl">
                <h2 class="text-3xl font-bold text-slate-900 mb-10 text-center">Local Expert Advice</h2>
                <div class="space-y-6">
                    {tips_html}
                </div>
            </div>
        </section>
        """

    # 5. Primary Service Area (for Hub page)
    if 'primaryServiceArea' in content_data:
        psa = content_data['primaryServiceArea']
        hoods = psa.get('neighborhoods', [])
        hoods_html = ", ".join(hoods)
        
        html += f"""
        <section class="py-20 bg-white">
             <div class="container mx-auto px-4">
                <div class="flex flex-col md:flex-row gap-12 items-center">
                    <div class="md:w-1/2">
                        <h2 class="text-3xl font-bold text-slate-900 mb-6">{psa.get('h2', '')}</h2>
                        <p class="text-lg text-slate-600 mb-6 leading-relaxed">{psa.get('content', '')}</p>
                        <a href="{psa.get('link', {}).get('url', '/')}" class="text-primary font-bold hover:text-secondary inline-flex items-center">
                            {psa.get('link', {}).get('text', 'Learn More')}
                            <svg class="w-4 h-4 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 8l4 4m0 0l-4 4m4-4H3"></path></svg>
                        </a>
                    </div>
                    <div class="md:w-1/2">
                        <div class="bg-slate-50 p-8 rounded-2xl border border-slate-100">
                            <h3 class="font-bold text-slate-900 mb-4">Neighborhoods</h3>
                            <div class="flex flex-wrap gap-2">
                                {"".join([f'<span class="px-3 py-1 bg-white border border-slate-200 rounded-full text-sm text-slate-600">{h}</span>' for h in hoods])}
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>
        """

    # 6. Service Areas List (for Hub page)
    if 'serviceAreas' in content_data:
        sa = content_data['serviceAreas']
        areas_html = ""
        for area in sa.get('areas', []):
            areas_html += f"""
            <a href="{area['url']}" class="group block relative overflow-hidden rounded-2xl aspect-[4/3]">
                <img src="{area.get('image', '').replace('[location-slug]', 'demo')}" alt="{area['name']}" class="absolute inset-0 w-full h-full object-cover transition-transform duration-500 group-hover:scale-110">
                <div class="absolute inset-0 bg-gradient-to-t from-black/80 via-black/40 to-transparent"></div>
                <div class="absolute bottom-0 left-0 p-6">
                    <h3 class="text-2xl font-bold text-white mb-1 group-hover:text-primary transition-colors">{area['name']}</h3>
                    <p class="text-white/90 text-sm">{area['description']}</p>
                </div>
            </a>
            """
            
        html += f"""
        <section class="py-20 bg-slate-50">
            <div class="container mx-auto px-4">
                <div class="text-center max-w-3xl mx-auto mb-12">
                    <h2 class="text-3xl font-bold text-slate-900 mb-4">{sa.get('h2', 'Communities We Serve')}</h2>
                    <p class="text-lg text-slate-600">{sa.get('intro', '')}</p>
                </div>
                <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {areas_html}
                </div>
            </div>
        </section>
        """

    # 7. Services Offered (for Hub page)
    if 'servicesOffered' in content_data:
        so = content_data['servicesOffered']
        # similar to regular services grid but maybe simpler
        s_html = ""
        for s in so.get('services', []):
             s_html += f"""
            <div class="bg-white p-6 rounded-xl shadow-sm border border-slate-100">
                <h3 class="font-bold text-slate-900 mb-2">{s['name']}</h3>
                <p class="text-slate-600 text-sm mb-3">{s['description']}</p>
                <a href="{s['url']}" class="text-primary text-sm font-medium hover:underline">Learn more</a>
            </div>
            """
            
        html += f"""
        <section class="py-20 bg-white">
            <div class="container mx-auto px-4">
                 <h2 class="text-3xl font-bold text-slate-900 mb-12 text-center">{so.get('h2', 'Services Available')}</h2>
                 <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {s_html}
                 </div>
            </div>
        </section>
        """


    # 8. Testimonials
    if 'testimonials' in content_data:
        testimonials = content_data.get('testimonials', [])
        if isinstance(testimonials, dict): # Handle object structure in hub page if any, though usually list
            testimonials = [] 

        test_cards = ""
        for t in testimonials:
            test_cards += f"""
            <div class="bg-slate-50 p-8 rounded-xl relative">
                <div class="text-yellow-400 text-2xl mb-4">★★★★★</div>
                <p class="text-slate-600 mb-6 italic">"{t['quote']}"</p>
                <div>
                    <p class="font-bold text-slate-900">{t['author']}</p>
                    <p class="text-sm text-slate-500">{t['location']}</p>
                </div>
            </div>
            """

        google_review_widget = ""
        if content_data.get('googleReviewsLink'):
            link = content_data['googleReviewsLink']
            google_review_widget = f"""
            <div class="col-span-full flex justify-center mt-12">
                <a href="{link}" target="_blank" rel="noopener" class="inline-flex items-center gap-4 bg-white border border-slate-200 p-6 rounded-2xl shadow-sm hover:shadow-md transition-all group">
                    <div class="w-8 h-8 flex-shrink-0">
                        <svg viewBox="0 0 48 48" class="w-full h-full"><path fill="#EA4335" d="M24 9.5c3.54 0 6.71 1.22 9.21 3.6l6.85-6.85C35.9 2.38 30.47 0 24 0 14.62 0 6.51 5.38 2.56 13.22l7.98 6.19C12.43 13.72 17.74 9.5 24 9.5z"></path><path fill="#4285F4" d="M46.98 24.55c0-1.57-.15-3.09-.38-4.55H24v9.02h12.94c-.58 2.96-2.26 5.48-4.78 7.18l7.73 6c4.51-4.18 7.09-10.36 7.09-17.65z"></path><path fill="#FBBC05" d="M10.53 28.59c-.48-1.45-.76-2.99-.76-4.59s.27-3.14.76-4.59l-7.98-6.19C.92 16.46 0 20.12 0 24c0 3.88.92 7.54 2.56 10.78l7.97-6.19z"></path><path fill="#34A853" d="M24 48c6.48 0 11.93-2.13 15.89-5.81l-7.73-6c-2.15 1.45-4.92 2.3-8.16 2.3-6.26 0-11.57-4.22-13.47-9.91l-7.98 6.19C6.51 42.62 14.62 48 24 48z"></path><path fill="none" d="M0 0h48v48H0z"></path></svg>
                    </div>
                    <div class="text-left">
                        <div class="flex items-center gap-1 text-yellow-400 text-xs mb-0.5">
                            ★★★★★
                        </div>
                        <p class="text-slate-900 font-bold text-sm group-hover:text-primary transition-colors">See all 5-Star Google Reviews</p>
                    </div>
                    <svg class="w-4 h-4 text-slate-300 group-hover:text-primary transition-colors ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7-7 7"></path></svg>
                </a>
            </div>
            """
            
        if test_cards:
            html += f"""
            <section class="py-20 bg-white">
                <div class="container mx-auto px-4">
                     <h2 class="text-3xl font-bold text-slate-900 mb-12 text-center">What {content_data['seo']['title'].split('|')[0].replace('Pool Service', '').strip()} Homeowners Say</h2>
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-8 max-w-4xl mx-auto">
                        {test_cards}
                        {google_review_widget}
                    </div>
                </div>
            </section>
            """

    # 9. FAQ
    if 'faq' in content_data:
        questions = content_data['faq'].get('questions', [])
        faq_items = ""
        for q in questions:
            faq_items += f"""
            <div class="border-b border-slate-200 py-6">
                <h3 class="text-lg font-bold text-slate-900 mb-2">{q['question']}</h3>
                <p class="text-slate-600 leading-relaxed">{q['answer']}</p>
            </div>
            """
            
        html += f"""
        <section class="py-20 bg-slate-50">
            <div class="container mx-auto px-4 max-w-3xl">
                <h2 class="text-3xl font-bold text-slate-900 mb-12 text-center">{content_data['faq'].get('h2', 'Frequently Asked Questions')}</h2>
                <div class="bg-white rounded-2xl p-8 shadow-sm">
                    {faq_items}
                </div>
            </div>
        </section>
        """

    # 10. Final CTA
    if 'finalCTA' in content_data:
        cta = content_data['finalCTA']
        html += f"""
        <section class="py-24 bg-primary text-white text-center">
            <div class="container mx-auto px-4">
                <h2 class="text-3xl md:text-5xl font-bold mb-6">{cta.get('h2', 'Ready to get started?')}</h2>
                <p class="text-xl text-white/90 mb-10 max-w-2xl mx-auto">{cta.get('content', '')}</p>
                <div class="flex flex-col sm:flex-row gap-4 justify-center">
                    <a href="/free-estimate/" class="inline-flex items-center justify-center px-8 py-4 bg-white text-primary text-lg font-bold rounded-lg hover:bg-slate-100 transition-all shadow-xl hover:shadow-2xl hover:-translate-y-1">
                        {cta.get('primaryCTA', {}).get('text', 'Get Your Free Estimate')}
                    </a>
                     <a href="tel:{PHONE.replace('(','').replace(')','').replace(' ','').replace('-','')}" class="inline-flex items-center justify-center px-8 py-4 border-2 border-white text-white text-lg font-bold rounded-lg hover:bg-white/10 transition-all">
                        {cta.get('secondaryCTA', {}).get('text', 'Call Us')}
                    </a>
                </div>
            </div>
        </section>
        """
        


    return html

def generate_content_for_page(page_type, data, extra_data={}):
    if page_type == 'home':
        services_grid = extra_data.get('services_grid', '')
        
        return f"""
        <!-- Trusted Info Section -->
        <section class="py-20 bg-white">
            <div class="container mx-auto px-4">
                <div class="grid grid-cols-1 lg:grid-cols-2 gap-16 items-center">
                    <div>
                        <h2 class="text-4xl font-bold text-slate-900 mb-6 leading-tight">Professional Pool Care You Can Trust</h2>
                        <div class="w-20 h-1 bg-primary rounded-full mb-8"></div>
                        <p class="text-lg text-slate-600 mb-8 leading-relaxed">
                            Keeping your pool crystal clear requires more than just skimming the surface. It requires consistent care, precise chemical balancing, and expert equipment knowledge. At Firewater Pools, we take the hassle out of pool ownership.
                        </p>
                        <ul class="space-y-6 mb-8">
                            <li class="flex items-start">
                                <div class="w-10 h-10 bg-blue-50 rounded-lg flex items-center justify-center text-primary mr-4 flex-shrink-0">
                                    <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"></path></svg>
                                </div>
                                <div>
                                    <p class="font-bold text-slate-900">Licensed & Insured Professionals</p>
                                    <p class="text-slate-500 text-sm">Peace of mind for your property.</p>
                                </div>
                            </li>
                            <li class="flex items-start">
                                <div class="w-10 h-10 bg-blue-50 rounded-lg flex items-center justify-center text-primary mr-4 flex-shrink-0">
                                    <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                                </div>
                                <div>
                                    <p class="font-bold text-slate-900">No Contracts Required</p>
                                    <p class="text-slate-500 text-sm">We earn your business every single week.</p>
                                </div>
                            </li>
                            <li class="flex items-start">
                                <div class="w-10 h-10 bg-blue-50 rounded-lg flex items-center justify-center text-primary mr-4 flex-shrink-0">
                                    <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 18h.01M8 21h8a2 2 0 002-2V5a2 2 0 00-2-2H8a2 2 0 00-2 2v14a2 2 0 002 2z"></path></svg>
                                </div>
                                <div>
                                    <p class="font-bold text-slate-900">Weekly Digital Reports</p>
                                    <p class="text-slate-500 text-sm">We email you a photo and chemical log after every visit so you know the job was done right.</p>
                                </div>
                            </li>
                            <li class="flex items-start">
                                <div class="w-10 h-10 bg-blue-50 rounded-lg flex items-center justify-center text-primary mr-4 flex-shrink-0">
                                    <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"></path></svg>
                                </div>
                                <div>
                                    <p class="font-bold text-slate-900">5-Star Rated</p>
                                    <p class="text-slate-500 text-sm">Voted best service in Vero Beach.</p>
                                </div>
                            </li>
                        </ul>
                        <div class="mt-10">
                            <a href="/free-estimate/" class="inline-flex items-center justify-center px-8 py-4 bg-primary text-white text-lg font-bold rounded-lg hover:bg-secondary transition-all shadow-lg hover:shadow-xl hover:-translate-y-1">
                                Get a Pool Service Quote
                                <svg class="w-5 h-5 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7-7 7"></path></svg>
                            </a>
                        </div>
                    </div>
                    <div class="relative">
                        <div class="absolute -top-4 -left-4 w-24 h-24 bg-blue-100 rounded-full z-0 opacity-50"></div>
                        <div class="absolute -bottom-4 -right-4 w-32 h-32 bg-primary/10 rounded-full z-0"></div>
                        <img src="https://images.unsplash.com/photo-1562778612-e1e0cda9915c?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80" alt="Sparkling blue pool" class="rounded-2xl shadow-2xl relative z-10 w-full object-cover h-[500px]">
                        <div class="absolute bottom-8 left-8 bg-white p-6 rounded-lg shadow-xl z-20 max-w-xs hidden md:block border-l-4 border-primary">
                            <div class="flex text-yellow-400 mb-2">
                                <svg class="w-5 h-5 fill-current" viewBox="0 0 20 20"><path d="M10 15l-5.878 3.09 1.123-6.545L.489 6.91l6.572-.955L10 0l2.939 5.955 6.572.955-4.756 4.635 1.123 6.545z"/></svg>
                                <svg class="w-5 h-5 fill-current" viewBox="0 0 20 20"><path d="M10 15l-5.878 3.09 1.123-6.545L.489 6.91l6.572-.955L10 0l2.939 5.955 6.572.955-4.756 4.635 1.123 6.545z"/></svg>
                                <svg class="w-5 h-5 fill-current" viewBox="0 0 20 20"><path d="M10 15l-5.878 3.09 1.123-6.545L.489 6.91l6.572-.955L10 0l2.939 5.955 6.572.955-4.756 4.635 1.123 6.545z"/></svg>
                                <svg class="w-5 h-5 fill-current" viewBox="0 0 20 20"><path d="M10 15l-5.878 3.09 1.123-6.545L.489 6.91l6.572-.955L10 0l2.939 5.955 6.572.955-4.756 4.635 1.123 6.545z"/></svg>
                                <svg class="w-5 h-5 fill-current" viewBox="0 0 20 20"><path d="M10 15l-5.878 3.09 1.123-6.545L.489 6.91l6.572-.955L10 0l2.939 5.955 6.572.955-4.756 4.635 1.123 6.545z"/></svg>
                            </div>
                            <p class="font-bold text-slate-900">Voted Best in Vero</p>
                            <p class="text-sm text-slate-500">Professional & Reliable Care</p>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- Services Grid -->
        <section class="py-20 bg-slate-50">
            <div class="container mx-auto px-4">
                <div class="text-center max-w-3xl mx-auto mb-16">
                    <h2 class="text-3xl md:text-4xl font-bold text-slate-900 mb-4">Full-Service Pool Care You Can Rely On</h2>
                    <p class="text-lg text-slate-600">Stop juggling contractors. We handle everything from routine maintenance to complex equipment repairs in-house.</p>
                </div>
                
                <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
                    {services_grid}
                </div>
                <div class="mt-12 text-center">
                    <a href="tel:{PHONE.replace('-', '')}" class="inline-flex items-center justify-center px-8 py-4 bg-primary text-white text-lg font-bold rounded-lg hover:bg-secondary transition-all shadow-lg hover:shadow-xl hover:-translate-y-1">
                        Call For Pool Service
                        <svg class="w-5 h-5 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"></path></svg>
                    </a>
                </div>
            </div>
        </section>

        <!-- About Kevin Section -->
        <section class="py-20 bg-white">
            <div class="container mx-auto px-4">
                <div class="grid grid-cols-1 lg:grid-cols-2 gap-16 items-center">
                    <div class="order-2 lg:order-1 relative">
                        <img src="/images/kevin-new.jpg" alt="Kevin owner of Firewater Pools" class="rounded-2xl shadow-2xl w-full h-auto max-h-[700px] object-scale-down">
                        <div class="absolute -bottom-6 -right-6 bg-secondary text-white p-8 rounded-xl shadow-xl z-20 hidden lg:block">
                            <p class="text-2xl font-bold mb-1">Kevin</p>
                            <p class="opacity-90">Owner & Operator</p>
                        </div>
                    </div>
                    <div class="order-1 lg:order-2">
                        <h2 class="text-3xl md:text-4xl font-bold text-slate-900 mb-6 leading-tight">Thanks for Choosing Firewater Pools</h2>
                        <div class="w-20 h-1 bg-primary rounded-full mb-8"></div>
                        <p class="text-lg text-slate-600 mb-6 leading-relaxed">
                            Hi, I'm Kevin, the owner and operator of Firewater Pools. I started this company right here in Vero Beach with a simple mission: to provide pool service that homeowners can actually rely on.
                        </p>
                        <p class="text-lg text-slate-600 mb-6 leading-relaxed">
                            After years of hearing complaints about pool guys who never showed up, skipped steps, or overcharged for simple fixes, I knew there was a better way. I built Firewater Pools on the values of transparency, communication, and genuine craftsmanship.
                        </p>
                         <p class="text-lg text-slate-600 mb-8 leading-relaxed">
                            When you hire us, you're not just getting a "pool guy"—you're getting a dedicated partner who cares about the safety and beauty of your backyard oasis as much as you do.
                        </p>
                        <div>
                            <a href="tel:{PHONE.replace('-', '')}" class="inline-flex items-center justify-center px-8 py-4 bg-primary text-white text-lg font-bold rounded-lg hover:bg-secondary transition-all shadow-lg hover:shadow-xl hover:-translate-y-1">
                                Call Kevin
                                <svg class="w-5 h-5 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"></path></svg>
                            </a>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- CTA Section -->
        <section class="bg-white border-t border-slate-200 py-20 relative overflow-hidden">
            <div class="bg-primary/5 absolute inset-0 transform -skew-y-2 scale-110 z-0"></div>
            <div class="container mx-auto px-4 text-center relative z-10">
                <h2 class="text-3xl md:text-5xl font-bold text-slate-900 mb-6">Ready for a Crystal Clear Pool?</h2>
                <p class="text-xl text-slate-600 mb-10 max-w-2xl mx-auto">Join hundreds of happy homeowners in Vero Beach. Professional, reliable, and affordable pool care is just a click away.</p>
                <a href="/free-estimate/" class="inline-flex items-center justify-center px-8 py-4 border border-transparent text-lg font-bold rounded-lg text-white bg-secondary hover:bg-accent transition-all shadow-xl hover:shadow-2xl hover:scale-105">
                    Schedule Your Free Estimate
                </a>
            </div>
        </section>

        <!-- Service Areas / Neighborhoods -->
        <section class="py-16 bg-slate-50 border-t border-slate-200">
            <div class="container mx-auto px-4 text-center">
                <h2 class="text-3xl font-bold text-slate-900 mb-6">Proudly Serving Vero Beach</h2>
                <div class="w-16 h-1 bg-primary mx-auto mb-8 rounded-full"></div>
                <p class="text-xl text-slate-700 max-w-3xl mx-auto leading-relaxed">
                    We provide professional pool service throughout the entire Vero Beach area, including 
                    <span class="font-semibold text-slate-900 underline decoration-primary/30">Grand Harbor</span>, 
                    <span class="font-semibold text-slate-900 underline decoration-primary/30">Sea Oaks</span>, 
                    <span class="font-semibold text-slate-900 underline decoration-primary/30">The Moorings</span>, 
                    <span class="font-semibold text-slate-900 underline decoration-primary/30">Bent Pine</span>, and 
                    <span class="font-semibold text-slate-900 underline decoration-primary/30">Central Beach</span>.
                </p>
            </div>
        </section>
        """

    # Base content with some typography for simple pages
    content = f"""
        <div class="prose prose-lg prose-slate max-w-none">
            <p class="lead text-xl text-slate-600 mb-8">
                {data.get('metaDescription', '')}
            </p>
            <h3>Service Overview</h3>
            <p>At {COMPANY_NAME}, we pride ourselves on delivering top-tier pool services to the Vero Beach community. Whether you need weekly maintenance, equipment repairs, or a complete green pool cleanup, our team of certified professionals is here to help.</p>
            
            <ul>
                <li>Licensed and Insured Professionals</li>
                <li>Reliable Weekly Schedules</li>
                <li>Transparent Pricing & No Hidden Fees</li>
                <li>Locally Owned in Vero Beach</li>
            </ul>
            
            <h3>Why Choose Us?</h3>
            <p>We understand that your pool is a major investment. That's why we treat every pool as if it were our own, ensuring the water is balanced, the equipment is functioning efficiently, and the surface is spotless.</p>
        </div>
    """

    # Free Estimate Page (Simple Form)
    if page_type == 'free-estimate':
        content = f"""
        <div class="max-w-4xl mx-auto py-24">
            <div class="text-center mb-12">
                <h2 class="text-3xl font-bold text-slate-900 mb-4">Request Your Free Estimate</h2>
                <p class="text-lg text-slate-600">Tell us a bit about your pool and we'll get back to you with a custom quote.</p>
            </div>
            
            <div class="bg-white p-8 md:p-12 rounded-2xl shadow-xl border border-slate-100">
                <form name="free-estimate" method="POST" data-netlify="true" class="space-y-6">
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                        <div>
                            <label class="block text-sm font-semibold text-slate-700 mb-2">First Name</label>
                            <input type="text" name="first-name" required class="w-full px-4 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-primary outline-none transition-all bg-slate-50 focus:bg-white" placeholder="John">
                        </div>
                        <div>
                            <label class="block text-sm font-semibold text-slate-700 mb-2">Last Name</label>
                            <input type="text" name="last-name" required class="w-full px-4 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-primary outline-none transition-all bg-slate-50 focus:bg-white" placeholder="Doe">
                        </div>
                    </div>
                    
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                        <div>
                            <label class="block text-sm font-semibold text-slate-700 mb-2">Email Address</label>
                             <input type="email" name="email" required class="w-full px-4 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-primary outline-none transition-all bg-slate-50 focus:bg-white" placeholder="your@email.com">
                        </div>
                        <div>
                            <label class="block text-sm font-semibold text-slate-700 mb-2">Phone Number</label>
                            <input type="tel" name="phone" required class="w-full px-4 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-primary outline-none transition-all bg-slate-50 focus:bg-white" placeholder="772-269-0249">
                        </div>
                    </div>
                    
                     <div>
                        <label class="block text-sm font-semibold text-slate-700 mb-2">Service Needed</label>
                        <select name="service" class="w-full px-4 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-primary outline-none transition-all bg-slate-50 focus:bg-white">
                            <option>Pool Cleaning</option>
                            <option>Repair</option>
                            <option>Green Pool Cleanup</option>
                            <option>Equipment Install</option>
                            <option>Other</option>
                        </select>
                    </div>
                    
                    <div>
                        <label class="block text-sm font-semibold text-slate-700 mb-2">Message & Details</label>
                        <textarea name="message" rows="4" class="w-full px-4 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-primary outline-none transition-all bg-slate-50 focus:bg-white" placeholder="Tell us about your pool (size, condition, specific issues)..."></textarea>
                    </div>
                    
                    <button type="submit" class="w-full py-4 px-6 bg-primary hover:bg-secondary text-white font-bold text-lg rounded-lg transition-all shadow-lg hover:shadow-xl hover:-translate-y-1">
                        Get Your Free Estimate
                    </button>
                    <p class="text-center text-sm text-slate-500 mt-4">We respect your privacy. No spam, ever.</p>
                </form>
            </div>
        </div>
        """

    # Custom Improved Contact Page
    if page_type == 'contact':
        content = f"""
        <div class="mb-20">
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-16 max-w-4xl mx-auto">
                <!-- Contact Card -->
                <div class="bg-white p-10 rounded-2xl shadow-lg border border-slate-100 flex flex-col items-center text-center">
                    <div class="w-20 h-20 bg-blue-50 rounded-full flex items-center justify-center text-primary mb-8">
                        <svg class="w-10 h-10" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"></path></svg>
                    </div>
                    <h3 class="text-2xl font-bold text-slate-900 mb-4">Call Us Directly</h3>
                    <p class="text-slate-600 mb-6 text-lg">We're available Mon-Fri, 8am - 5pm.</p>
                    <a href="tel:{PHONE.replace('-', '')}" class="text-2xl font-bold text-primary hover:text-secondary transition-colors">{PHONE}</a>
                </div>

                <!-- Location Card -->
                <div class="bg-white p-10 rounded-2xl shadow-lg border border-slate-100 flex flex-col items-center text-center">
                     <div class="w-20 h-20 bg-blue-50 rounded-full flex items-center justify-center text-primary mb-8">
                        <svg class="w-10 h-10" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"></path><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"></path></svg>
                    </div>
                    <h3 class="text-2xl font-bold text-slate-900 mb-4">Service Area</h3>
                    <p class="text-slate-600 mb-6 text-lg">Proudly serving Vero Beach & Indian River County.</p>
                    <span class="text-2xl font-bold text-slate-800">{ADDRESS}</span>
                </div>
            </div>

            <div class="grid grid-cols-1 lg:grid-cols-2 gap-12">
                <!-- Message Form -->
                <div class="bg-white p-8 rounded-2xl shadow-lg border border-slate-100">
                    <h3 class="text-2xl font-bold mb-6 text-slate-900">Send us a Message</h3>
                    <form name="contact" method="POST" data-netlify="true" class="space-y-4">
                        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                            <div>
                                <label class="block text-sm font-medium text-slate-700 mb-1">First Name</label>
                                <input type="text" name="first-name" required class="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-primary outline-none transition-all" placeholder="John">
                            </div>
                            <div>
                                <label class="block text-sm font-medium text-slate-700 mb-1">Last Name</label>
                                <input type="text" name="last-name" required class="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-primary outline-none transition-all" placeholder="Doe">
                            </div>
                        </div>
                        <div>
                            <label class="block text-sm font-medium text-slate-700 mb-1">Phone Number</label>
                            <input type="tel" name="phone" required class="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-primary outline-none transition-all" placeholder="772-269-0249">
                        </div>
                        
                        <div>
                            <label class="block text-sm font-medium text-slate-700 mb-1">How can we help?</label>
                            <textarea name="message" rows="4" class="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-primary outline-none transition-all" placeholder="Tell us about your pool..."></textarea>
                        </div>
                        <button type="submit" class="w-full py-3 px-6 bg-primary hover:bg-secondary text-white font-bold rounded-lg transition-colors shadow-md">
                            Send Message
                        </button>
                    </form>
                </div>

                <!-- Map & Hours -->
                <div class="space-y-8">
                     <!-- Map Embed -->
                    <div class="bg-slate-200 rounded-2xl overflow-hidden h-80 shadow-inner relative">
                        <iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d113060.05739023021!2d-80.46335186835252!3d27.63855598686629!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x88de5ec866874ee5%3A0x6b4fb6d43516c11b!2sVero%20Beach%2C%20FL!5e0!3m2!1sen!2sus!4v1709568912345!5m2!1sen!2sus" width="100%" height="100%" style="border:0;" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
                    </div>

                    <!-- Hours Box -->
                    <div class="bg-slate-900 text-white p-8 rounded-2xl shadow-xl">
                        <h3 class="text-xl font-bold mb-6 flex items-center">
                            <svg class="w-6 h-6 text-primary mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                            Business Hours
                        </h3>
                        <ul class="space-y-3 text-slate-300">
                            <li class="flex justify-between border-b border-slate-700 pb-2">
                                <span>Monday - Friday</span>
                                <span class="font-bold text-white">8:00 AM - 5:00 PM</span>
                            </li>
                            <li class="flex justify-between border-b border-slate-700 pb-2">
                                <span>Saturday</span>
                                <span class="font-bold text-white">By Appointment</span>
                            </li>
                            <li class="flex justify-between pb-2">
                                <span>Sunday</span>
                                <span class="text-slate-500">Closed</span>
                            </li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
        """
    
    return content

def generate_blog_post_content(content_data):
    html = ""
    # Header Meta
    html += f"""
    <section class="py-12 bg-slate-50 border-b border-slate-200">
        <div class="container mx-auto px-4 max-w-3xl">
            <a href="/pool-care-guide/" class="inline-flex items-center text-primary font-medium hover:underline mb-8">
                <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"></path></svg>
                Back to Guide
            </a>
            <div class="flex items-center space-x-4 text-sm text-slate-500 mb-6">
                <span class="flex items-center"><svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path></svg> {content_data.get('date', '')}</span>
                <span class="flex items-center"><svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 007-7z"></path></svg> {content_data.get('author', 'Firewater Pools')}</span>
            </div>
            <p class="text-xl md:text-2xl text-slate-700 leading-relaxed italic border-l-4 border-primary pl-6 py-2 bg-white rounded-r-lg shadow-sm">
                {content_data.get('intro', '')}
            </p>
        </div>
    </section>
    """

    # Content Body
    body_content = ""
    for item in content_data.get('content', []):
        body_content += f'<div class="mb-8">{item}</div>'

    html += f"""
    <section class="py-16 bg-white">
        <div class="container mx-auto px-4 max-w-3xl prose prose-lg prose-slate prose-headings:text-slate-900 prose-a:text-primary">
            {body_content}
            
            <div class="mt-12 p-8 bg-blue-50 rounded-2xl border border-blue-100">
                <h3 class="text-xl font-bold text-slate-900 mb-4">Summary</h3>
                <p class="text-slate-700">{content_data.get('conclusion', '')}</p>
            </div>
        </div>
    </section>
    """
    
    # CTA
    html += f"""
    <section class="py-20 bg-slate-900 text-white text-center">
        <div class="container mx-auto px-4 max-w-2xl">
            <h2 class="text-3xl font-bold mb-6">Still have questions?</h2>
            <p class="text-lg text-slate-300 mb-8">Pool care can be tricky. We're here to help you get it right.</p>
            <a href="/contact/" class="inline-flex items-center justify-center px-8 py-4 bg-primary text-white font-bold rounded-lg hover:bg-secondary transition-all">
                Contact Us
            </a>
        </div>
    </section>
    """
    
    return html

def generate_blog_hub_content(content_data, blog_posts_list):
    html = ""
    
    # Intro
    if 'intro' in content_data:
        html += f"""
        <section class="py-16 bg-white text-center">
            <div class="container mx-auto px-4 max-w-3xl">
                <p class="text-xl text-slate-600 leading-relaxed">{content_data.get('intro', '')}</p>
            </div>
        </section>
        """

    # Grid
    posts_html = ""
    for post in blog_posts_list:
        # We need to peek into the content json for details if we had them all loaded, 
        # but here we might only have the structure data (name, h1, etc).
        # We can map the ID to the intro/date if passed, but simpler to just use structure data for now
        # or rely on the fact that we might not have efficient access to all content here easily without loading it all.
        # Actually, main() passes explicit content_data for the Hub, but for the grid items we need the content of *other* pages.
        # Let's assume we want a simple card for now.
        
        posts_html += f"""
        <a href="{post['url']}" class="group flex flex-col bg-white rounded-xl shadow-sm border border-slate-100 overflow-hidden hover:shadow-xl transition-all hover:-translate-y-1 h-full">
            <div class="h-48 bg-slate-200 relative overflow-hidden">
                <!-- Placeholder for blog image -->
                <div class="absolute inset-0 bg-gradient-to-br from-primary/80 to-secondary/80 flex items-center justify-center">
                    <svg class="w-16 h-16 text-white/50" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 20H5a2 2 0 01-2-2V6a2 2 0 012-2h10a2 2 0 012 2v1m2 13a2 2 0 01-2-2V7m2 13a2 2 0 002-2V9a2 2 0 00-2-2h-2m-4-3H9M7 16h6M7 8h6v4H7V8z"></path></svg>
                </div>
            </div>
            <div class="p-8 flex flex-col flex-grow">
                <h3 class="text-xl font-bold text-slate-900 mb-3 group-hover:text-primary transition-colors">{post['h1']}</h3>
                <p class="text-slate-600 mb-6 flex-grow text-sm line-clamp-3">{post['metaDescription']}</p>
                <span class="text-indigo-600 font-semibold text-sm flex items-center mt-auto">
                    Read Article 
                    <svg class="w-4 h-4 ml-1 transform group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 8l4 4m0 0l-4 4m4-4H3"></path></svg>
                </span>
            </div>
        </a>
        """

    html += f"""
    <section class="py-20 bg-slate-50">
        <div class="container mx-auto px-4">
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                {posts_html}
            </div>
        </div>
    </section>
    """

    # Hub CTA
    if 'cta' in content_data:
        cta = content_data['cta']
        html += f"""
        <section class="py-24 bg-white text-center">
             <div class="container mx-auto px-4 max-w-3xl">
                <h2 class="text-3xl font-bold text-slate-900 mb-6">{cta.get('h2', '')}</h2>
                <p class="text-xl text-slate-600 mb-10">{cta.get('content', '')}</p>
                <a href="/contact/" class="inline-flex items-center justify-center px-8 py-4 bg-primary text-white text-lg font-bold rounded-lg hover:bg-secondary transition-all shadow-lg hover:shadow-xl">
                    {cta.get('buttonText', 'Contact Us')}
                </a>
            </div>
        </section>
        """

    return html

def create_page(path, data, extra_data, page_type="generic", content_data=None):
    # Ensure directory exists
    clean_path = path.strip('/')
    if clean_path:
        dir_path = os.path.join(OUTPUT_DIR, clean_path)
    else:
        dir_path = OUTPUT_DIR
    
    os.makedirs(dir_path, exist_ok=True)
    
    file_path = os.path.join(dir_path, 'index.html')
    
    # Placeholders replacement
    seo_title = data.get('seoTitle', 'Pool Service Vero Beach').replace('[Company Name]', COMPANY_NAME)
    meta_desc = data.get('metaDescription', '').replace('[Company Name]', COMPANY_NAME)
    h1 = data.get('h1', 'Pool Services').replace('[Company Name]', COMPANY_NAME)
    
    # Use subheadline from content data if available, else default to meta desc
    subheadline = meta_desc
    if content_data and 'hero' in content_data and 'subheadline' in content_data['hero']:
        subheadline = content_data['hero']['subheadline']
    
    schema = generate_schema_markup(data, is_home=(path == '/'))
    
    
    if content_data:
        if page_type in ['location', 'location_hub']:
            content = generate_location_content(content_data, page_type)
        elif page_type == 'about':
            content = generate_about_content(content_data)
        elif page_type == 'blog_post':
            content = generate_blog_post_content(content_data)
        elif page_type == 'blog_hub':
            content = generate_blog_hub_content(content_data, extra_data.get('blog_posts_list', []))
        else:
            content = generate_detailed_service_content(content_data)
    else:
        content = generate_content_for_page(page_type, data, extra_data)
    
    # Determine hero image
    hero_image_url = "https://images.unsplash.com/photo-1576013551627-0cc20b96c2a7?ixlib=rb-1.2.1&auto=format&fit=crop&w=1950&q=80"
    if content_data and 'hero' in content_data and 'heroImage' in content_data['hero']:
        hero_image_url = content_data['hero']['heroImage'].get('src', hero_image_url)
    
    # Badge Text Override
    badge_text = "Serving Vero Beach & Indian River County"
    if content_data and 'badgeText' in content_data:
        badge_text = content_data['badgeText']

    # Sticky Call Button for Mobile
    sticky_call_button = ""
    if content_data and content_data.get('showStickyCallButton', False):
        sticky_call_button = f"""
    <!-- Sticky Call Button -->
    <div class="md:hidden fixed bottom-0 left-0 right-0 z-[100] p-4 bg-gradient-to-t from-black/20 to-transparent">
        <a href="tel:{PHONE.replace('-', '')}" class="flex items-center justify-center gap-3 bg-secondary text-white py-4 rounded-xl font-bold shadow-2xl animate-bounce-subtle">
            <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 24 24"><path d="M3.5 3h17a1 1 0 011 1v16a1 1 0 01-1 1h-17a1 1 0 01-1-1V4a1 1 0 011-1zm1 2v14h15V5h-15zm4 4h7v2h-7V9zm0 4h7v2h-7v-2z"></path></svg>
            Call Now for a Free Estimate
        </a>
    </div>
    <style>
    @keyframes bounce-subtle {{
        0%, 100% {{ transform: translateY(0); }}
        50% {{ transform: translateY(-5px); }}
    }}
    .animate-bounce-subtle {{
        animation: bounce-subtle 3s infinite ease-in-out;
    }}
    </style>
    """

    html = HTML_TEMPLATE.format(
        seo_title=seo_title,
        meta_description=meta_desc,
        h1=h1,
        subheadline=subheadline,
        hero_image_url=hero_image_url,
        company_name=COMPANY_NAME,
        phone=PHONE,
        address=ADDRESS,
        year=datetime.now().year,
        schema_markup=schema,
        custom_content=content,
        locations_dropdown=extra_data.get('locations_dropdown', ''),
        services_dropdown=extra_data.get('services_dropdown', ''),
        services_footer_list=extra_data.get('services_footer_list', ''),
        badge_text=badge_text,
        sticky_call_button=sticky_call_button
    )
    
    with open(file_path, 'w') as f:
        f.write(html)
    print(f"Created: {file_path}")

def generate_sitemap(urls):
    """
    Generates a sitemap.xml file for Google Search Console.
    """
    domain = "https://www.firewaterpools.com"
    today = datetime.now().strftime('%Y-%m-%d')
    
    sitemap_header = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
    sitemap_footer = '\n</urlset>'
    
    url_items = []
    for url in urls:
        # Ensure URL starts with /
        if not url.startswith('/'):
            url = '/' + url
            
        # Set priority and changefreq based on URL path
        priority = "0.8"
        changefreq = "weekly"
        
        if url == "/":
            priority = "1.0"
            changefreq = "daily"
        elif "/pool-care-guide/" in url:
            priority = "0.7"
            changefreq = "monthly"
        elif "/service-areas/" in url:
            priority = "0.9"
            changefreq = "weekly"
            
        item = f"""
  <url>
    <loc>{domain}{url}</loc>
    <lastmod>{today}</lastmod>
    <changefreq>{changefreq}</changefreq>
    <priority>{priority}</priority>
  </url>"""
        url_items.append(item)
        
    sitemap_content = sitemap_header + "".join(url_items) + sitemap_footer
    
    sitemap_path = os.path.join(OUTPUT_DIR, 'sitemap.xml')
    with open(sitemap_path, 'w') as f:
        f.write(sitemap_content)
    print(f"Sitemap generated at {sitemap_path}")
    
    # Generate robots.txt
    robots_content = f"User-agent: *\nAllow: /\n\nSitemap: {domain}/sitemap.xml"
    robots_path = os.path.join(OUTPUT_DIR, 'robots.txt')
    with open(robots_path, 'w') as f:
        f.write(robots_content)
    print(f"robots.txt generated at {robots_path}")

def main():
    # Clean output dir
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
    os.makedirs(OUTPUT_DIR)

    # Copy Assets
    if os.path.exists(ASSETS_DIR):
        shutil.copytree(ASSETS_DIR, OUTPUT_DIR, dirs_exist_ok=True)
        print(f"Copied assets from {ASSETS_DIR} to {OUTPUT_DIR}")

    # Read Structure JSON
    with open(JSON_FILE, 'r') as f:
        site_data = json.load(f)
        
    # Read Content JSON (Optional)
    detailed_content = {}
    if os.path.exists(CONTENT_JSON_FILE):
        with open(CONTENT_JSON_FILE, 'r') as f:
            content_json = json.load(f)
            # Create map of id -> content
            for item in content_json.get('servicePages', []):
                detailed_content[item['id']] = item

    # Read Location Content JSON
    location_content = {}
    if os.path.exists(LOCATION_CONTENT_JSON_FILE):
        with open(LOCATION_CONTENT_JSON_FILE, 'r') as f:
            loc_json = json.load(f)
            location_content['overview'] = loc_json.get('locationsOverviewPage')
            for item in loc_json.get('locationPages', []):
                location_content[item['id']] = item

    # Read About Content JSON
    about_content = {}
    if os.path.exists(ABOUT_CONTENT_JSON_FILE):
        with open(ABOUT_CONTENT_JSON_FILE, 'r') as f:
            about_content = json.load(f)

    # Read Blog Content JSON
    blog_content = {}
    if os.path.exists(BLOG_CONTENT_JSON_FILE):
        with open(BLOG_CONTENT_JSON_FILE, 'r') as f:
            blog_content = json.load(f)

    pages = site_data.get('pages', {})
    
    # Pre-calculate Locations Dropdown HTML
    loc_pages = pages.get('locationPages', {})
    locations_html = ""
    if 'locations' in loc_pages:
        for loc in loc_pages['locations']:
            locations_html += f'<a href="{loc["url"]}" class="block px-4 py-2 text-sm text-slate-600 hover:bg-slate-50 hover:text-primary">{loc["name"]}</a>\n'

    # Pre-calculate Services HTML and Dropdown
    service_pages = pages.get('servicePages', [])
    
    services_dropdown_html = ""
    services_footer_html = ""
    services_grid_html = ""
    
    for s in service_pages:
        # Dropdown
        services_dropdown_html += f'<a href="{s["url"]}" class="block px-4 py-2 text-sm text-slate-600 hover:bg-slate-50 hover:text-primary">{s["name"]}</a>\n'
        # Footer
        services_footer_html += f'<li><a href="{s["url"]}" class="hover:text-primary transition-colors">{s["name"]}</a></li>\n'
        # Grid Card
        services_grid_html += f"""
        <div class="bg-white rounded-xl p-8 shadow-md hover:shadow-xl transition-all hover:-translate-y-1 group border border-slate-100 flex flex-col h-full">
            <div class="w-14 h-14 bg-blue-50 rounded-lg flex items-center justify-center text-primary mb-6 group-hover:bg-primary group-hover:text-white transition-colors flex-shrink-0">
                <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.384-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z"></path></svg>
            </div>
            <h3 class="text-xl font-bold text-slate-900 mb-3">{s['name']}</h3>
            <p class="text-slate-600 leading-relaxed mb-6 flex-grow">{s['metaDescription']}</p>
            <a href="{s['url']}" class="text-primary font-bold hover:text-secondary flex items-center gap-2 group/link">
                Our {s['name']} Service
                <svg class="w-4 h-4 transform group-hover/link:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path></svg>
            </a>
        </div>
        """

    extra_data = {
        'locations_dropdown': locations_html,
        'services_dropdown': services_dropdown_html,
        'services_footer_list': services_footer_html,
        'services_grid': services_grid_html
        
    }

    all_urls = []
    
    # Homepage
    all_urls.append(pages['homepage']['url'])
    create_page(pages['homepage']['url'], pages['homepage'], extra_data, 'home')
    
    # Service Pages
    for page in service_pages:
        # Determine if we have detailed content
        # Map URL to ID? 
        # /pool-cleaning/ -> pool-cleaning
        page_id = page['url'].strip('/').split('/')[-1] # simple heuristic
        if page_id == "": page_id = page['url'].strip('/').split('/')[-2] # handle trail slash
        
        # Override for specific known pages if needed, simple logic for now
        c_data = detailed_content.get(page_id)
        
        all_urls.append(page['url'])
        create_page(page['url'], page, extra_data, 'service', content_data=c_data)
        
    # Location Pages
    if 'overview' in loc_pages:
        c_data = location_content.get('overview')
        all_urls.append(loc_pages['overview']['url'])
        create_page(loc_pages['overview']['url'], loc_pages['overview'], extra_data, 'location_hub', content_data=c_data)
        
    for page in loc_pages.get('locations', []):
        # Match by ID logic: /service-areas/sebastian-fl/ -> sebastian-fl
        page_id = page['url'].strip('/').split('/')[-1]
        c_data = location_content.get(page_id)
        all_urls.append(page['url'])
        create_page(page['url'], page, extra_data, 'location', content_data=c_data)
        
    # Blog Pages
    blog_pages = pages.get('blogPages', {})
    blog_posts_list = blog_pages.get('posts', [])
    
    if 'hub' in blog_pages:
        hub_content = blog_content.get('hub', {})
        extra_data['blog_posts_list'] = blog_posts_list
        all_urls.append(blog_pages['hub']['url'])
        create_page(blog_pages['hub']['url'], blog_pages['hub'], extra_data, 'blog_hub', content_data=hub_content)
        
    for page in blog_posts_list:
        post_id = page['url'].strip('/').split('/')[-1]
        post_content = blog_content.get('posts', {}).get(post_id, {})
        if post_content:
            all_urls.append(page['url'])
            create_page(page['url'], page, extra_data, 'blog_post', content_data=post_content)
        
    # Business Pages
    for page in pages.get('businessPages', []):
        p_type = 'generic'
        c_data = None
        
        if 'contact' in page['url']: 
            p_type = 'contact'
        if 'free-estimate' in page['url']: 
            p_type = 'free-estimate'
        if 'about' in page['url']:
            p_type = 'about'
            c_data = about_content
            
        all_urls.append(page['url'])
        create_page(page['url'], page, extra_data, p_type, content_data=c_data)

    # Generate Sitemap
    generate_sitemap(all_urls)

    print("Site generation complete.")

if __name__ == "__main__":
    main()
