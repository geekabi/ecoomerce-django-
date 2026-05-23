# Pet Shop E-commerce Platform (Django)
        

            
            
            A comprehensive, scalable, and modern E-commerce platform dedicated to pets and pet supplies, powered by **Django**. This platform includes both a customer-facing storefront and a **bespoke Custom Admin Panel** for full business management.
        

            
            
            ## 🌟 Overview
        

            
            
            This project is an all-in-one solution for a pet shop, featuring product browsing, advanced filtering, a secure checkout process with Zarinpal payment gateway integration, and a specialized administrative dashboard for store managers.
        

            
            
            ## 🚀 Key Features
        

            
            
            ### 🛒 Customer Storefront
        

            
            
            - **Product Catalog:** Advanced categorization using `django-mptt`.
        

            
            
            - **Advanced Search & Filtering:** Find pet supplies easily.
        

            
            
            - **Secure Shopping:** Full cart system and checkout with **Zarinpal** payment gateway.
        

            
            
            - **User Profiles:** Manage addresses, order history, and personal information.
        

            
            
            - **Responsive Design:** Fully optimized for mobile, tablet, and desktop devices.
        

            
            
            ### ⚙️ Custom Admin Dashboard
        

            
            
            - **Dashboard:** Real-time overview of sales and store status.
        

            
            
            - **Order Management:** Deep-dive into order details, shipping info, payment status, and order lifecycle management.
        

            
            
            - **Product Management:** CRUD operations with intelligent unique slug generation.
        

            
            
            - **Category Management:** Hierarchical tree management for products.
        

            
            
            - **HTMX Integration:** Dynamic, SPA-like experiences in the admin area without full page reloads.
        

            
            
            ## 🛠 Tech Stack
        

            
            
            - **Backend:** Django, Python 3
        

            
            
            - **Database:** PostgreSQL/SQLite
        

            
            
            - **Frontend:** HTML5, CSS3, JavaScript (HTMX for interactivity)
        

            
            
            - **Payments:** Zarinpal API
        

            
            
            - **Utilities:** `django-mptt`, `django-crispy-forms`
        

            
            
            ## 📦 Installation & Setup
        

            
            
            1. Clone the repository:
        

            
            
               ```bash
        

            
            
               git clone <your-repository-url>
        

            
            
               cd pet-shop-django
        

            
            
               ```
        

            
            
            2. Setup virtual environment:
        

            
            
               ```bash
        

            
            
               python -m venv venv
        

            
            
               source venv/bin/activate  # Windows: venv\Scripts\activate
        

            
            
               ```
        

            
            
            3. Install dependencies:
        

            
            
               ```bash
        

            
            
               pip install -r requirements.txt
        

            
            
               ```
        

            
            
            4. Database migration:
        

            
            
               ```bash
        

            
            
               python manage.py makemigrations
        

            
            
               python manage.py migrate
        

            
            
               ```
        

            
            
            5. Launch the server:
        

            
            
               ```bash
        

            
            
               python manage.py runserver
        

            
            
               ```
        

            
            
            ## 🏗 Project Structure
        

            
            
            - `accounts/`: User authentication, profile management, and custom user models.
        

            
            
            - `shop/`: Core e-commerce logic, products, variants, orders, and addresses.
        

            
            
            - `adminpanel/`: Our powerful custom admin interface.
        

            
            
            - `templates/`: Professional templates for both storefront and admin panel.
        

            
            
            ## 🤝 Contribution
        

            
            
            Contributions are welcome! If you have any suggestions, improvements, or feature requests, feel free to open an issue or submit a pull request.
        

            
            
            ---
        

            
            
            *Developed with ❤️ by sepehr hosseini*
