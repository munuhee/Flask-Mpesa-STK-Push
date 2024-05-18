# Flask M-Pesa Integration

<img src="https://res.cloudinary.com/murste/image/upload/v1713944812/icons/daraja_geyyh9.png" width="150" />

This application allows you to integrate M-Pesa functionalities into your Flask application. It enables features like initiating STK push requests.

## Prerequisites

Before you begin, ensure you have the following:

- A Safaricom Developer Portal account. [Safaricom Developer Portal](https://developer.safaricom.co.ke/)
- Consumer Key and Consumer Secret obtained from the Safaricom Developer Portal.
- Test credentials assigned to you by Safaricom.

## Setup

1. **Environment Configuration:**
   - Create a `.env` file in the root directory of your Flask project.
   - Add the following credentials to your `.env` file:

     ```bash
     # Secret Key
     SECRET_KEY= # Your Safaricom Secret Key

     # Daraja API credentials
     CONSUMER_KEY= # Your Safaricom Consumer Key
     CONSUMER_SECRET= # Your Safaricom Consumer Secret
     SHORTCODE= # Your Safaricom Short Code
     PASSKEY= # Your Passkey

     # Database URI
     SQLALCHEMY_DATABASE_URI= # Your  Database URI
     ```

2. **Virtual Environment Setup:**
   - It's a best practice to work within a virtual environment to manage package dependencies. Here's how to set it up based on your operating system:

     - **For Windows:**
       ```bash
       python -m venv venv
       venv\Scripts\activate
       ```
     - **For macOS/Linux:**
       ```bash
       python3 -m venv venv
       source venv/bin/activate
       ```

3. **Environment Activation:**
   - Once the virtual environment is activated, depending on your operating system, run the appropriate command to source the `.env` file:

     - **For Linux/MacOS:**
       ```bash
       source .env
       ```
     - **For Windows:**
       ```bash
       call setenv.bat
       ```

## Database Migration

To manage database migrations, follow these steps:

1. Initialize the migration environment:
   ```bash
   flask db init
   ```

2. Create an initial migration:
   ```bash
   flask db migrate -m "Initial migration"
   ```

3. Apply the migration to the database:
   ```bash
   flask db upgrade
   ```

## Usage

### Endpoints

1. **Initiate M-Pesa STK Push**
   - **Endpoint:** `/initiate_mpesa_stk_push`
   - **Methods:** POST, GET
   - **Description:** Initiate STK push for M-Pesa payment.

2. **View Records**
   - **Endpoint:** `/view_records`
   - **Method:** GET
   - **Description:** View M-Pesa transaction records.
