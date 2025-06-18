from flask import Blueprint, g, request, jsonify
from ..services import payment_service
from ..services.auth_service import jwt_required, api_key_required
from ..database import db_session
from ..models_db import UserModel
import requests

payment_bp = Blueprint('payment', __name__)

@payment_bp.route("/", methods=["POST"])
@jwt_required
def create_payment_route():
    """
    Creates a new payment for the authenticated user and updates their role to premium.
    """
    db = None
    try:
        data = request.get_json()
        if not data or 'card' not in data:
            return jsonify({"error": "Card information is required"}), 400

        amount = 1
        if not isinstance(amount, (int, float)) or amount <= 0:
            return jsonify({"error": "A valid positive amount is required"}), 400
        
        payment_response = payment_service.create_payment(user_email=g.user_email, amount=float(amount))
        
        # If payment is successful, update user to premium
        if payment_response.get("status") == "completed":
            db = db_session()
            user = db.query(UserModel).filter(UserModel.email == g.user_email).first()
            if user:
                user.role = "premium"
                user.premium = True
                db.commit()

        return jsonify(payment_response), 201

    except requests.HTTPError as e:
        return jsonify(e.response.json()), e.response.status_code
    except Exception as e:
        return jsonify({"error": "Error creating payment", "details": str(e)}), 500
    finally:
        if db:
            db.close()

@payment_bp.route("/history", methods=["GET"])
@jwt_required
def get_payment_history_route():
    """
    Retrieves the payment history for the authenticated user.
    """
    try:
        history = payment_service.get_payment_history(user_email=g.user_email)
        return jsonify(history), 200
    except requests.HTTPError as e:
        return jsonify(e.response.json()), e.response.status_code
    except Exception as e:
        return jsonify({"error": "Error retrieving payment history", "details": str(e)}), 500

@payment_bp.route("/refund/<int:payment_id>", methods=["POST"])
@api_key_required
def refund_payment_route(payment_id: int):
    """
    Refunds a specific payment. Requires API key for authorization.
    """
    try:
        refund_response = payment_service.refund_payment(payment_id=payment_id)
        return jsonify(refund_response), 200
    except requests.HTTPError as e:
        return jsonify(e.response.json()), e.response.status_code
    except Exception as e:
        return jsonify({"error": "Error processing refund", "details": str(e)}), 500