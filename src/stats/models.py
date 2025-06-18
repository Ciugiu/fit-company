from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class WorkoutStat(Base):
    __tablename__ = 'workout_stats'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    exercise_name = Column(String, nullable=False)
    duration = Column(Float, nullable=False)  # Duration in minutes
    calories_burned = Column(Float, nullable=False)
    timestamp = Column(DateTime, nullable=False)

    def __repr__(self):
        return f"<WorkoutStat(id={self.id}, user_id={self.user_id}, exercise_name='{self.exercise_name}', duration={self.duration}, calories_burned={self.calories_burned}, timestamp={self.timestamp})>"