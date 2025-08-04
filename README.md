# Ray Solar Solutions Backend

## Frontend Repository
🔗 **Frontend Application**: [Ray Solar Solutions Frontend](https://github.com/Michael-Munga/Ray-Solar-Solutions-Frontend)

## Environment Variables

To run this project, you need to set the following environment variables in your .env file:

```env
# Flask Configuration
SECRET_KEY=your_secret_key_here
DATABASE_URL=sqlite:///app.db

# M-Pesa Configuration
MPESA_CONSUMER_KEY=your_consumer_key_here
MPESA_CONSUMER_SECRET=your_consumer_secret_here
MPESA_BASE_URL=https://sandbox.safaricom.co.ke
MPESA_SHORTCODE=your_shortcode_here
MPESA_PASSKEY=your_passkey_here
BASE_URL=http://localhost:5555

# JWT Configuration
JWT_SECRET_KEY=your_jwt_secret_key_here
```

## Required Environment Variables

- `SECRET_KEY`: A secret key for Flask sessions
- `DATABASE_URL`: Database connection string
- `MPESA_CONSUMER_KEY`: Your M-Pesa consumer key from Safaricom Daraja
- `MPESA_CONSUMER_SECRET`: Your M-Pesa consumer secret from Safaricom Daraja
- `MPESA_BASE_URL`: The base URL for M-Pesa APIs (sandbox or production)
- `MPESA_SHORTCODE`: Your M-Pesa business shortcode
- `MPESA_PASSKEY`: Your M-Pesa passkey
- `BASE_URL`: The base URL of your application (used for callbacks)
- `JWT_SECRET_KEY`: A secret key for JWT token generation

## Installation

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up your environment variables in a .env file

3. Run migrations:
   ```bash
   flask db upgrade
   ```

4. Run the application:
   ```bash
   python app.py
   ```

## Setup

1. Clone the Repository:
   ```bash
   git clone https://https://github.com/Michael-Munga/Ray-Solar-Solutions-Backend
   cd ray-solar-backend
   ```

## Testing M-Pesa Integration Locally (Sandbox)

Using Ngrok to expose your local server:
```bash
ngrok http 5555
```

This will give you a public URL like https://abc123.ngrok.io.

Update your .env:
```env
BASE_URL=https://abc123.ngrok.io
```

Then test with:
```json
POST /mpesa/pay
{
  "phone": "2547XXXXXXXX",
  "amount": 10
}
```

Simulate a callback via curl or Daraja sandbox tools.

## Author

Ray Solar Solutions — Built by Group 3 members.

🌞 Powering off-grid communities with reliable solar energy, one transaction at a time.