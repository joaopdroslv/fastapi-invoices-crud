from database.database import Base

from sqlalchemy import Column, Integer, Numeric, Boolean, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship


class Invoice(Base):
    __tablename__ = 'invoices'

    id = Column(Integer, primary_key=True, autoincrement=True)
    value = Column(Numeric)
    paid = Column(Boolean, default=False)
    paid_value = Column(Numeric)
    payment_date = Column(DateTime, nullable=True)
    payment_method = Column(String(128), nullable=True)

    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    user = relationship('User')
