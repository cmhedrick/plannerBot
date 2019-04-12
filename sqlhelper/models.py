from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Chat(Base):
    __tablename__ = 'chats'

    id = Column(Integer, primary_key=True)
    chat_id = Column(String)
    # parent of schedules
    schedules = relationship("Schedule", back_populates="chat")

    def __repr__(self):
        return "Chat ID: {}".format(self.chat_id)


class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True)
    datetime = Column(DateTime)
    description = Column(Text)
    location = Column(Text)
    # child of schedules
    schedule_id = Column(Integer, ForeignKey('schedules.id'))
    schedule = relationship("Schedule", back_populates="tasks")

    def __repr__(self):
        return "Task: {}".format(self.id)


class Schedule(Base):
    __tablename__ = 'schedules'

    id = Column(Integer, primary_key=True)
    # parent of tasks
    tasks = relationship("Task", back_populates="schedule")
    # child of chats
    chat_id = Column(Integer, ForeignKey('chats.id'))
    chat = relationship("Chat", back_populates="schedules")

    def __repr__(self):
        return "Schedule: {}".format(self.id)


if __name__ == "__main__":
    import sys
    import os
    from sqlalchemy import create_engine

    # hack route to config #FightMe
    sys.path.insert(0, "../config")
    import config
    try:
        # create engine to spin up db
        engine = create_engine(
            'sqlite:///' + config.DB,
            echo=True
        )

        Base.metadata.create_all(engine)
    except Exception as e:
        print(e)
        os.remove("test.db")
        print("Removed garbage DB")
