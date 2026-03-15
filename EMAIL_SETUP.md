# Email Configuration Setup

To enable the OTP email system, I have created a `.env` file in the project root with your credentials.

## Credentials

The following credentials are used in the `.env` file:
- **Email:** `electronicsstoreelectroshop@gmail.com`
- **App Password:** `bwnu gxge gcph qhyg`

## How it works

1.  **`.env` File:** A file named `.env` exists in `d:\smart_ecg\` containing:
    ```text
    EMAIL_HOST_USER=electronicsstoreelectroshop@gmail.com
    EMAIL_HOST_PASSWORD=bwnu gxge gcph qhyg
    ```
2.  **Django Settings:** `settings.py` now uses `python-dotenv` to automatically load these variables when the server starts.

## Running the Server
You no longer need to set environment variables manually in the terminal. Just start your Django server:
```bash
python manage.py runserver
```

> [!IMPORTANT]
> Ensure the `.env` file is NOT committed to a public repository to keep your credentials secure.
