import os
import requests
from typing import Dict, Any, List

# Assumes PAYMENT_URL is set in your environment, e.g., http://localhost:5001
PAYMENT_URL = os.getenv("PAYMENT_URL")

def create_payment(user_email: str, amount: float) -> Dict[str, Any]:
    """
    Calls the payment service to create a new payment.
    """
    if not PAYMENT_URL:
        raise ValueError("PAYMENT_URL environment variable not set")
    
    response = requests.post(
        f"{PAYMENT_URL}/payment",
        json={"user_email": user_email, "amount": amount}
    )
    response.raise_for_status()
    return response.json()

def get_payment_history(user_email: str) -> List[Dict[str, Any]]:
    """
    Calls the payment service to get a user's payment history.
    """
    if not PAYMENT_URL:
        raise ValueError("PAYMENT_URL environment variable not set")

    response = requests.get(f"{PAYMENT_URL}/payment/history/{user_email}")
    response.raise_for_status()
    return response.json()

def refund_payment(payment_id: int) -> Dict[str, Any]:
    """
    Calls the payment service to refund a payment.
    """
    if not PAYMENT_URL:
        raise ValueError("PAYMENT_URL environment variable not set")
    
    response = requests.post(f"{PAYMENT_URL}/payment/refund/{payment_id}")
    response.raise_for_status()
    return response.json()