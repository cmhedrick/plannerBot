import sys
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from models import Chat


class SQLHelper:

    def __init__(self, db_file):
        #import pdb; pdb.set_trace()
        self.db_file = db_file
        self.db_exists = os.path.isfile(db_file)
        engine = create_engine(
            'sqlite:///' + db_file,
            echo=False
        )
        if not self.db_exists:
            Base = declarative_base()
            Base.metadata.create_all(engine, tables=[Chat.__table__])
        # create Session factory
        Session = sessionmaker(bind=engine)
        Session = sessionmaker()
        Session.configure(bind=engine)
        # bind session to SQLHelper
        self.session = Session()

    def add_chat(self, chat_id):
        chat = Chat(chat_id=chat_id)
        self.session.add(chat)
        self.session.commit()

    def is_duplicate_chat(self, chat_id):
        if self.session.query(Chat).filter(
            Chat.chat_id == chat_id
        ).all():
            return True
        else:
            return False


if __name__ == '__main__':
    # hack route to config #FightMe
    sys.path.insert(0, "../config")
    import config

    # create SQLHelper
    sqh = SQLHelper(db_file=config.DB)

    # test entry
    sqh.add_chat(chat_id="TESTNUMBER380938298320")

    # test retrival
    print(sqh.session.query(Chat).all())

    # test duplicate (True)
    print(sqh.is_duplicate_chat(chat_id="TESTNUMBER380938298320"))
    # false
    print(sqh.is_duplicate_chat(chat_id="VeryFalse1093839893928"))
