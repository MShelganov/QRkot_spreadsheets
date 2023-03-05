from sqlalchemy import Column, String, Text

from app.core.db import Base, DonationAbs


class CharityProject(DonationAbs, Base):
    name = Column(String(100))
    description = Column(Text)
