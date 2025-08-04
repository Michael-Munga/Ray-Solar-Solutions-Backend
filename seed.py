from app import app
from models import db, Product, Category, User

# ===========================
# 1. Add Admin User
# ===========================
with app.app_context():
    admin_email = "admin@gmail.com"
    existing_admin = User.query.filter_by(email=admin_email).first()
    if not existing_admin:
        

        admin = User(
            first_name="Admin",
            last_name="User",
            email=admin_email,
            role="admin",
            is_approved=True
        )
        admin.set_password("Admin123")
        db.session.add(admin)
        db.session.commit()
        print(" Admin user created.")
    else:
        print("ℹ Admin user already exists.")

# ===========================
# 2. Seed Categories & Products
# ===========================
    category_products = {
        "Solar Panels": [
            {
                "name": "UltraSlim 300W Solar Panel",
                "short_description": "Compact panel ideal for rooftops.",
                "description": "This 300W monocrystalline panel fits snugly on small roofs and RVs. Built for harsh climates.",
                "image_url": "https://i.pinimg.com/736x/78/d7/7d/78d77d4b555ea7836cbc9bccf7679ce2.jpg",
                "wattage": "300W", "warranty": "20-year warranty", "price": 279.99, "original": 319.99, "popular": True
            },
            {
                "name": "BlackFrame 400W Solar Panel",
                "short_description": "Durable with anodized aluminum frame.",
                "description": "Highly efficient 400W solar panel, ideal for off-grid systems or rural setups.",
                "image_url": "https://i.pinimg.com/1200x/9a/6e/95/9a6e958b3f5868c9a2abd5e7b7c5a97f.jpg",
                "wattage": "400W", "warranty": "25-year warranty", "price": 349.99, "original": 399.99, "popular": True
            },
            {
                "name": "TwinCell 500W Bifacial Panel",
                "short_description": "Dual-cell design for max output.",
                "description": "Innovative bifacial solar panel captures sunlight on both sides. 500W output ideal for commercial installations.",
                "image_url": "https://i.pinimg.com/736x/4e/8e/44/4e8e445cce1daae0ca5d798a70b97078.jpg",
                "wattage": "500W", "warranty": "30-year performance warranty", "price": 419.99, "original": 469.99, "popular": True
            },
            {
                "name": "GlassShield 250W Solar Panel",
                "short_description": "Low-glare glass for urban rooftops.",
                "description": "Aesthetic 250W panel with anti-reflective coating. Built for dense neighborhoods and eco-homes.",
                "image_url": "https://i.pinimg.com/736x/83/bd/c3/83bdc301eff678a5d936353ca3f7ae27.jpg",
                "wattage": "250W", "warranty": "15-year warranty", "price": 199.99, "original": 249.99, "popular": False
            },
            {
                "name": "PeakMax 600W Commercial Panel",
                "short_description": "High-output for solar farms.",
                "description": "Premium 600W industrial-grade solar panel designed for maximum efficiency in utility-scale arrays.",
                "image_url": "https://i.pinimg.com/736x/c6/b1/54/c6b15439833fa204b1183e46f096e5b2.jpg",
                "wattage": "600W", "warranty": "25-year warranty", "price": 499.99, "original": 579.99, "popular": True
            },
        ],
        "Garden Lights": [
            {
                "name": "AmberGlow Path Light",
                "short_description": "Soft amber lighting for walkways.",
                "description": "Rechargeable solar light with dusk-to-dawn sensor. Perfect for warm outdoor ambiance.",
                "image_url": "https://i.pinimg.com/1200x/df/73/06/df730675ccacf7012eaf58bfa6401a6d.jpg",
                "wattage": "4W", "duration": "10 hours", "warranty": "1-year warranty", "price": 19.99, "original": 29.99, "popular": True
            },
            {
                "name": "Vintage Spike Solar Light",
                "short_description": "Decorative lighting for flower beds.",
                "description": "Black matte finish with clear casing. Charges quickly, stays lit all night.",
                "image_url": "https://i.pinimg.com/1200x/63/c4/38/63c438e4a4481a27d00310a9468c6e17.jpg",
                "wattage": "3W", "duration": "8 hours", "warranty": "1-year warranty", "price": 15.99, "original": 22.99, "popular": False
            },
            {
                "name": "LED Stone Path Light",
                "short_description": "Stone-like casing, blends with nature.",
                "description": "Weather-resistant light disguised as decorative stone. Great for ground placement.",
                "image_url": "https://i.pinimg.com/736x/14/51/02/1451020c56f89174161934c2294225e5.jpg",
                "wattage": "2W", "duration": "6 hours", "warranty": "6-month warranty", "price": 12.49, "original": 16.99, "popular": False
            },
            {
                "name": "GardenGlow Lantern Light",
                "short_description": "Lantern-style with flicker effect.",
                "description": "Solar-powered with LED flame flicker. Decorative and functional.",
                "image_url": "https://i.pinimg.com/736x/f9/32/d7/f932d707b2eb23ebde224fb580bb1031.jpg",
                "wattage": "4W", "duration": "10-12 hours", "warranty": "1-year warranty", "price": 21.99, "original": 27.99, "popular": True
            },
            {
                "name": "DualMode Spot Light",
                "short_description": "Motion-sensing spotlight.",
                "description": "Switches from low to high beam on movement. Waterproof and energy-saving.",
                "image_url": "https://i.pinimg.com/736x/df/7e/96/df7e96f97c88638dee4355cf55a3d096.jpg",
                "wattage": "6W", "duration": "up to 12 hrs", "warranty": "2-year warranty", "price": 29.99, "original": 35.99, "popular": True
            },
            {
                "name": "Flora Ring Light",
                "short_description": "Circular solar ring for flowerpots.",
                "description": "Wrap-around LED glow for floral beds. Solar panel charges fast even in low light.",
                "image_url": "https://i.pinimg.com/736x/ad/0b/7a/ad0b7a2ef48f6e04b22230fcd43169b8.jpg",
                "wattage": "3W", "duration": "9 hours", "warranty": "1-year warranty", "price": 17.49, "original": 21.49, "popular": False
            },
            {
                "name": "Solar Rope Light Strip",
                "short_description": "Flexible LED rope for railings.",
                "description": "16ft solar LED rope. Bend around garden edges or patio furniture for ambient light.",
                "image_url": "https://i.pinimg.com/736x/56/f8/d0/56f8d01cae5321c75618045a38e0d4c1.jpg",
                "wattage": "5W", "duration": "14 hours", "warranty": "1-year warranty", "price": 23.99, "original": 28.99, "popular": True
            },
        ],
        "Home Systems": [
            {
                "name": "LumenPro A19 Smart Bulb",
                "short_description": "Voice-controlled LED bulb.",
                "description": "Wi-Fi enabled LED bulb with full RGB spectrum. Compatible with Alexa and Google Home.",
                "image_url": "https://i.pinimg.com/1200x/d0/4e/0e/d04e0e1492667754114fc7e696bd1293.jpg",
                "wattage": "10W", "duration": "25,000 hrs", "warranty": "2-year warranty", "price": 12.99, "original": 16.99, "popular": True
            },
            {
                "name": "EcoLight Cool White LED",
                "short_description": "Energy-efficient home lighting.",
                "description": "Low-heat LED bulb producing bright white light. Rated A++ for efficiency.",
                "image_url": "https://i.pinimg.com/1200x/54/45/1b/54451b7308223afe56a840e1a481c302.jpg",
                "wattage": "9W", "duration": "20,000 hrs", "warranty": "1-year warranty", "price": 9.99, "original": 12.49, "popular": False
            },
            {
                "name": "SunTone Color Changing Bulb",
                "short_description": "App-controlled multicolor LED.",
                "description": "Switch colors, brightness, and schedules via mobile app. Great for bedrooms or studios.",
                "image_url": "https://i.pinimg.com/1200x/f7/a2/8d/f7a28dbfa325314b2ec84c31c406dbea.jpg",
                "wattage": "12W", "duration": "30,000 hrs", "warranty": "3-year warranty", "price": 14.99, "original": 18.99, "popular": True
            },
            {
                "name": "Smart Filament Bulb E26",
                "short_description": "Vintage look, modern tech.",
                "description": "Classic filament shape with LED efficiency and smart control features.",
                "image_url": "https://i.pinimg.com/736x/f6/af/84/f6af84dc16913004ea084286ebf222ad.jpg",
                "wattage": "7W", "duration": "15,000 hrs", "warranty": "2-year warranty", "price": 10.49, "original": 13.99, "popular": False
            },
            {
                "name": "PowerGlow B22 LED",
                "short_description": "High-lumen LED for large spaces.",
                "description": "Designed for basements, garages, or high ceilings. Broad light coverage.",
                "image_url": "https://i.pinimg.com/736x/99/ee/90/99ee9042fe669adf586b943728d09734.jpg",
                "wattage": "15W", "duration": "35,000 hrs", "warranty": "3-year warranty", "price": 18.99, "original": 22.99, "popular": True
            },
        ],
        "Street Lights": [
            {
                "name": "MotionMax Solar Street Light",
                "short_description": "Auto-dim with motion trigger.",
                "description": "Street light with PIR motion detection. Efficient lithium battery and fast charging.",
                "image_url": "https://i.pinimg.com/1200x/d1/73/98/d173982ed1d0cb61040bd8335905a622.jpg",
                "wattage": "60W", "duration": "12 hours", "warranty": "3-year warranty", "price": 89.99, "original": 99.99, "popular": True
            },
            {
                "name": "BrightWay 80W Solar Lamp",
                "short_description": "All-in-one weatherproof light.",
                "description": "Anti-rust aluminum casing, long-range LED beam for streets and parking lots.",
                "image_url": "https://i.pinimg.com/736x/b1/73/de/b173ded2cb1d003d4404b5c5c39f7a3a.jpg",
                "wattage": "80W", "duration": "10-14 hrs", "warranty": "5-year warranty", "price": 119.99, "original": 139.99, "popular": True
            },
            {
                "name": "EcoBeam Compact 40W Light",
                "short_description": "Smaller unit for short poles.",
                "description": "Ideal for parks, bike lanes, or pathways. Compact solar unit with efficient LED.",
                "image_url": "https://i.pinimg.com/736x/a4/28/47/a42847ea088186543d2a556e24887eed.jpg",
                "wattage": "40W", "duration": "8 hours", "warranty": "2-year warranty", "price": 69.99, "original": 79.99, "popular": False
            },
            {
                "name": "StormGuard 100W Light",
                "short_description": "Built to survive storms.",
                "description": "Reinforced panels and battery enclosure. Excellent for coastal cities and heavy rains.",
                "image_url": "https://i.pinimg.com/736x/20/cc/7a/20cc7a90d0ddc0a57e6a6de27da87a6f.jpg",
                "wattage": "100W", "duration": "14 hrs", "warranty": "5-year warranty", "price": 129.99, "original": 149.99, "popular": True
            },
            {
                "name": "UrbanLite LED Street Light",
                "short_description": "Ideal for city sidewalks.",
                "description": "Slim profile with modern design. Excellent brightness and low light pollution.",
                "image_url": "https://i.pinimg.com/736x/41/44/5a/41445ae5fcdc1728fcd20d90122eb55a.jpg",
                "wattage": "50W", "duration": "10 hrs", "warranty": "3-year warranty", "price": 99.99, "original": 114.99, "popular": False
            },
            {
                "name": "HighBeam Dual Panel Light",
                "short_description": "Dual-panel design for faster charging.",
                "description": "Great for areas with partial sun. Dual solar panel system and long-life lithium battery.",
                "image_url": "https://i.pinimg.com/736x/50/38/06/503806e1a59260e676830ba4e3ffd98d.jpg",
                "wattage": "75W", "duration": "13 hrs", "warranty": "4-year warranty", "price": 109.99, "original": 124.99, "popular": True
            },
        ]
    }

    for category_name, products in category_products.items():
        category = Category.query.filter_by(name=category_name).first()
        if not category:
            category = Category(name=category_name)
            db.session.add(category)
            db.session.commit()

        for p in products:
            if Product.query.filter_by(name=p["name"]).first():
                continue

            product = Product(
                name=p["name"],
                short_description=p["short_description"],
                description=p["description"],
                image_url=p["image_url"],
                wattage=p.get("wattage"),
                duration=p.get("duration", ""),
                warranty_period=p["warranty"],
                stock=20,
                price=p["price"],
                original_price=p["original"],
                is_popular=p["popular"],
                category_id=category.id
            )
            db.session.add(product)

    db.session.commit()
    print(" Seeded categories, products, and admin user.")
