import sys
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from sqlhelper.models import Chat, Schedule, Task


class SQLHelper:

    def __init__(self, db_file):
        self.db_file = db_file
        self.db_exists = os.path.isfile(db_file)
        engine = create_engine(
            'sqlite:///' + db_file,
            echo=False
        )
        if not self.db_exists:
            Base = declarative_base()
            Base.metadata.create_all(
                engine,
                tables=[
                    Chat.__table__,
                    Schedule.__table__,
                    Task.__table__
                ]
            )
        # create Session factory
        Session = sessionmaker(bind=engine)
        Session = sessionmaker()
        Session.configure(bind=engine)
        # bind session to SQLHelper
        self.session = Session()

    # chat helper section
    def add_chat(self, chat_id):
        """add chat to db, returns Chat obj"""
        chat = Chat(chat_id=chat_id)
        self.session.add(chat)
        self.session.commit()
        return chat

    def is_duplicate_chat(self, chat_id):
        if self.session.query(Chat).filter(
            Chat.chat_id == chat_id
        ).all():
            return True
        else:
            return False

    def get_chat(self, chat_id):
        chat = self.session.query(Chat).filter(
            Chat.chat_id == chat_id
        ).first()
        return chat

    # schedule helpers
    def add_schedule(self, chat_id, schedule_title):
        """add schedule to db, returns Schedule obj"""
        chat = self.get_chat(chat_id)
        schedule = Schedule(chat_id=chat.id, title=schedule_title)
        self.session.add(schedule)
        self.session.commit()
        return schedule

    def chat_has_schedule(self, chat_id):
        if self.session.query(Schedule).filter(
            Schedule.chat_id == chat_id
        ).all():
            return True
        else:
            return False

    def get_schedule(self, chat_id):
        chat = self.get_chat(chat_id)
        sched = self.session.query(Schedule).filter(
            Schedule.chat_id == chat.id
        ).first()
        return sched

    # task helpers


if __name__ == '__main__':
    # hack route to config #FightMe
    sys.path.insert(0, "../config")
    import config

    # create SQLHelper
    sqh = SQLHelper(db_file=config.DB)

    # test entry
    chat = sqh.add_chat(chat_id="TESTNUMBER380938298320")
    schedule = sqh.add_schedule(chat_id=chat.id, schedule_title="TestSchedule")

    # test chat retrival
    print(sqh.session.query(Chat).all())
    # test schedule retrival
    print(sqh.session.query(Schedule).all())
    # get specific schedule
    print(sqh.get_schedule("TESTNUMBER380938298320"))

    # test duplicate (True)
    print(sqh.is_duplicate_chat(chat_id="TESTNUMBER380938298320"))
    # false
    print(sqh.is_duplicate_chat(chat_id="VeryFalse1093839893928"))
    # test duplicate (True)
    print(sqh.chat_has_schedule(chat_id=chat.id))
    # false
    print(sqh.chat_has_schedule(chat_id=2))
