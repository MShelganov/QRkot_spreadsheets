from sqlalchemy import Column, ForeignKey, Integer, Text

from app.core.db import Base, DonationAbs


class Donation(DonationAbs, Base):
    comment = Column(Text)
    user_id = Column(Integer, ForeignKey('user.id'))
