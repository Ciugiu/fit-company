from sqlalchemy import Column, String, Float, Integer, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import datetime

Base = declarative_base()

class UserModel(Base):
    __tablename__ = "users"

    email = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    role = Column(String, nullable=False)
    password_hash = Column(String, nullable=False)

    # Relationships
    payments = relationship("PaymentModel", back_populates="user")

    def __repr__(self):
        return f"<User(email='{self.email}', name='{self.name}', role='{self.role}')>"

class PaymentModel(Base):
    __tablename__ = 'payments'

    id = Column(Integer, primary_key=True)
    user_email = Column(String, ForeignKey('users.email'), nullable=False)
    amount = Column(Float, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)

    # Relationships
    user = relationship("UserModel", back_populates="payments")

    def __repr__(self):
        return f"<Payment(id={self.id}, user_email='{self.user_email}', amount={self.amount}, created_at='{self.created_at}')>"