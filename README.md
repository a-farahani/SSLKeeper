# SSLKeeper

**SSLKeeper** is a Django application designed to manage and renew SSL certificates for domains. It supports automated renewal using Let's Encrypt with Cloudflare DNS-01 challenges. The app stores private keys, certificates, and expiration dates, and sends notifications about upcoming expirations.

Features
-----

- Store SSL certificate details, including private keys and certificates.
- Automatically calculate and store certificate expiration dates.
- Manage Cloudflare DNS records for Let's Encrypt DNS-01 challenges.
- Automated certificate renewal when expiration is within 7 days.
- Alerts sent via Telegram when certificates are 15 days from expiration.
- Integration with Celery for task scheduling and background processing.
- Notifications sent to a Telegram bot about certificate expirations.

Requirements
-----

- Docker
- Docker Compose

Installation
-----

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/a-farahani/sslkeeper.git
   cd sslkeeper
   ```

2. **Create and Configure the .env File:**

   ```bash
   cp .env.example .env
   ```
   Edit the .env file to include your configuration

3. **Build and Start the Docker Containers:**

   ```bash
   docker compose build
   docker compose up -d
   ```

4. **Run Migrations:**

   ```bash
   docker compose exec sslkeeper python manage.py migrate
   ```

5. **Create Superuser:**

   ```bash
   docker compose exec sslkeeper python manage.py createsuperuser
   ```

Usage
-----

1.  **Add Domains:**
    
    *   Navigate to the Django admin panel at http://localhost:8000/admin/.
        
    *   Add domain details including private key, certificate, Cloudflare API key, and email.
        
2.  **Automated Renewal:**
    
    *   The application checks daily for certificates expiring within 7 days and renews them using Certbot with Cloudflare DNS-01 challenge.
        
3.  **Notifications:**
    
    *   Configure the Telegram bot to receive alerts about expiring certificates. Make sure your bot is set up and the TELEGRAM\_BOT\_TOKEN and TELEGRAM\_CHAT\_ID in the .env file are correctly configured.
        

Configuration
-------------

*   **Cloudflare API Key:** Add the Cloudflare API key in the Domain model within the Django admin panel. This key will be used for DNS challenges during certificate renewal.
    
*   **Email:** Specify the email address for Let's Encrypt notifications in the Domain model.
    

Contributing
------------

Feel free to fork the repository and submit pull requests. Ensure your code adheres to the project's style guidelines and includes tests.

License
-------

This project is licensed under the Apache 2.0 License. See the LICENSE file for details.

Contact
-------

For any inquiries, please contact alireza.f.7596@gmail.com.