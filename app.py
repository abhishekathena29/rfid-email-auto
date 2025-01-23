from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import yagmail

# Initialize FastAPI
app = FastAPI()

# Email account credentials
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
APP_PASSWORD = os.getenv("APP_PASSWORD")

# Initialize Yagmail
yag = yagmail.SMTP(SENDER_EMAIL, APP_PASSWORD)

# Define request model
class EmailRequest(BaseModel):
    recipient: str
    subject: str
    body: str

@app.post("/send-email")
async def send_email(email_request: EmailRequest):
    """API endpoint to send an email using Yagmail."""
    try:
        # Send email
        yag.send(
            to=email_request.recipient,
            subject=email_request.subject,
            contents=email_request.body
        )
        return {"message": "Email sent successfully!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
