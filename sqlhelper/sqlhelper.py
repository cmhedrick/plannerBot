import sys
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# prod uncomment below
from sqlhelper.models import Chat, Schedule, Task
# run file as main uncomment below
#from models import Chat, Schedule, Task


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
        chat = self.get_chat(chat_id)
        if self.session.query(Schedule).filter(
            Schedule.chat_id == chat.id
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
    def add_task(self, chat_id, task_title):
        """add task to db, returns task obj"""
        schedule = self.get_schedule(chat_id)
        task = Task(
            schedule_id=schedule.id,
            title=task_title,
            task_num=len(schedule.tasks) + 1
        )
        self.session.add(task)
        self.session.commit()
        import pdb
        pdb.set_trace()
        return task

    def update_task_desc(self, chat_id, task_num, task_desc):
        """add task to db, returns task obj"""
        task = self.get_task_by_num(chat_id=chat_id, task_num=task_num)
        task.description = task_desc
        self.session.add(task)
        self.session.commit()
        return task

    def get_task_by_num(self, chat_id, task_num):
        sched = self.get_schedule(chat_id)
        task = self.session.query(Task).filter(
            Task.schedule_id == sched.id
        ).first()
        return task


if __name__ == '__main__':
    # hack route to config #FightMe
    sys.path.insert(0, "../config")
    import config

    # create SQLHelper
    sqh = SQLHelper(db_file=config.DB)

    # test entry
    chat = sqh.add_chat(chat_id="TESTNUMBER380938298320")
    schedule = sqh.add_schedule(
        chat_id=chat.chat_id,
        schedule_title="TestSchedule"
    )
    task1 = sqh.add_task(chat_id=chat.chat_id, task_title="Test Task1")
    task2 = sqh.add_task(chat_id=chat.chat_id, task_title="Test Task2")

    # test chat retrival
    print(sqh.session.query(Chat).all())
    # test schedule retrival
    print(sqh.session.query(Schedule).all())
    # get all tasks
    print(sqh.session.query(Task).all())
    # get specific schedule
    print(sqh.get_schedule("TESTNUMBER380938298320"))
    # print tasks belonging to schedule
    for task in schedule.tasks:
        print(task)
    # test duplicate (True)
    print(sqh.is_duplicate_chat(chat_id="TESTNUMBER380938298320"))
    # false
    print(sqh.is_duplicate_chat(chat_id="VeryFalse1093839893928"))
    # test duplicate (True)
    print(sqh.chat_has_schedule(chat_id=chat.id))
    # false
    print(sqh.chat_has_schedule(chat_id=2))
