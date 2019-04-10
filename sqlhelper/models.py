from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()


class Chat(Base):
    __tablename__ = 'Chats'

    id = Column(Integer, primary_key=True)
    chat_id = Column(String)

    def __repr__(self):
        return "Chat ID: {}".format(self.chat_id)


if __name__ == "__main__":
    import sys
    from sqlalchemy import create_engine

    # hack route to config #FightMe
    sys.path.insert(0, "../config")
    import config

    # create engine to spin up db
    engine = create_engine(
        'sqlite:///' + config.DB,
        echo=True
    )

    Base.metadata.create_all(engine)
