from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase

class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)

class Data(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    timestamp: Mapped[datetime] = mapped_column(nullable=False)
    temperature: Mapped[float] = mapped_column(nullable=False)
    humidity: Mapped[float] = mapped_column(nullable=False)
    
    
    
    # id = db.Column(db.Integer, primary_key=True)
    # timestamp = db.Column(db.DateTime, nullable=False)
    # temperature = db.Column(db.Float, nullable=False)
    # humidity = db.Column(db.Float, nullable=False)

    # def __init__(self, timestamp, temperature, humidity):
    #     self.timestamp = timestamp
    #     self.temperature = temperature
    #     self.humidity = humidity

