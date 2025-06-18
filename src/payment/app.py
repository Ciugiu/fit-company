from flask import Flask, request, jsonify
import logging
import sys
from .database import init_db, SessionLocal
from .services import payment_service
from .models_dto import PaymentSchema
from pydantic import ValidationError

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Create Flask app
app = Flask(__name__)
app.logger.setLevel(logging.DEBUG)

# Force stdout to be unbuffered
sys.stdout.reconfigure(line_buffering=True)

@app.route("/health")
def health():
    return {"status": "UP"}

@app.route("/payment", methods=["POST"])
def create_payment():
    """
    Process a new payment.
    """
    db = SessionLocal()
    try:
        payment_data = PaymentSchema.model_validate(request.get_json())
        payment = payment_service.process_payment(payment_data=payment_data, db=db)
        return jsonify({
            "id": payment.id,
            "user_email": payment.user_email,
            "amount": payment.amount,
            "status": payment.status,
            "created_at": payment.created_at.isoformat()
        }), 201
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400
    except Exception as e:
        app.logger.error(f"Error processing payment: {e}")
        return jsonify({"error": "Internal server error"}), 500
    finally:
        db.close()

@app.route("/payment/history/<string:user_email>", methods=["GET"])
def get_user_payment_history(user_email: str):
    """
    Retrieve payment history for a user.
    """
    db = SessionLocal()
    try:
        payments = payment_service.get_payment_history(user_email=user_email, db=db)
        payment_history = [
            {
                "id": p.id,
                "user_email": p.user_email,
                "amount": p.amount,
                "status": p.status,
                "created_at": p.created_at.isoformat()
            } for p in payments
        ]
        return jsonify(payment_history)
    except Exception as e:
        app.logger.error(f"Error retrieving payment history: {e}")
        return jsonify({"error": "Internal server error"}), 500
    finally:
        db.close()

@app.route("/payment/refund/<int:payment_id>", methods=["POST"])
def refund_user_payment(payment_id: int):
    """
    Refund a specific payment.
    """
    db = SessionLocal()
    try:
        payment = payment_service.refund_payment(payment_id=payment_id, db=db)
        return jsonify({
            "id": payment.id,
            "user_email": payment.user_email,
            "amount": payment.amount,
            "status": payment.status,
            "created_at": payment.created_at.isoformat()
        })
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        app.logger.error(f"Error processing refund: {e}")
        return jsonify({"error": "Internal server error"}), 500
    finally:
        db.close()

def run_app():
    """Entry point for the application script"""
    # Initialize the database before starting the app
    init_db()

    app.run(host="0.0.0.0", port=5000, debug=True)

if __name__ == "__main__":
    run_app()