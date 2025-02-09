from app.database.database import Base

from sqlalchemy import Column, Integer, Numeric, Boolean, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship


class Invoice(Base):
    __tablename__ = 'invoices'

    id = Column(Integer, primary_key=True, autoincrement=True)
    value = Column(Numeric, nullable=False)
    paid_value = Column(Numeric, nullable=True, default=0.0)
    paid = Column(Boolean, nullable=True, default=False)
    payment_date = Column(DateTime, nullable=True)
    payment_method = Column(String(128), nullable=True)

    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    user = relationship('User')

    @property
    def remaining_value(self):
        return float(self.value) - float(self.paid_value or 0.0)

    @property
    def full_payment(self):
        return self.remaining_value <= 0
