from typing import List
from sqlalchemy.orm import Session
from ..models_db import PaymentModel, UserModel
from ..models_dto import PaymentSchema
import logging

logger = logging.getLogger(__name__)

def process_payment(payment_data: PaymentSchema, db: Session) -> PaymentModel:
    """
    Process a payment and save it to the database.
    """
    logger.debug("Processing payment for user: %s", payment_data.user_email)
    
    payment = PaymentModel(
        user_email=payment_data.user_email,
        amount=payment_data.amount,
        status="processed"
    )
    
    db.add(payment)
    db.commit()
    db.refresh(payment)
    
    logger.info("Payment processed successfully: %s", payment)
    return payment

def get_payment_history(user_email: str, db: Session) -> List[PaymentModel]:
    """
    Retrieve payment history for a specific user.
    """
    logger.debug("Retrieving payment history for user: %s", user_email)
    
    payments = db.query(PaymentModel).filter(PaymentModel.user_email == user_email).all()
    
    logger.info("Retrieved payment history for user: %s", user_email)
    return payments

def refund_payment(payment_id: int, db: Session) -> PaymentModel:
    """
    Process a refund for a specific payment.
    """
    logger.debug("Processing refund for payment ID: %d", payment_id)
    
    payment = db.query(PaymentModel).filter(PaymentModel.id == payment_id).first()
    if not payment:
        logger.error("Payment not found: %d", payment_id)
        raise ValueError("Payment not found")
    
    payment.status = "refunded"
    db.commit()
    db.refresh(payment)
    
    logger.info("Payment refunded successfully: %s", payment)
    return payment