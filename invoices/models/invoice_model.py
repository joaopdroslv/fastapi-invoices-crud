from shared.database import Base

from sqlalchemy import Column, Integer, Numeric, Boolean, String, Date


class Invoice(Base):
    __tablename__ = 'invoices'

    id = Column(Integer, primary_key=True, autoincrement=True)
    value = Column(Numeric)
    paid = Column(Boolean, default=False)
    payment_date = Column(Date, nullable=True)
    payment_method = Column(String(128), nullable=True)
