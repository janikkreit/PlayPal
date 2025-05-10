from sqlalchemy import Column, Integer, String, Table, ForeignKey, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
import os

Base = declarative_base()

# Association table for many-to-many relationship between Users and Events (participants)
event_participants = Table(
    "event_participants",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("event_id", Integer, ForeignKey("events.id"))
)

class Event(Base):
    """
    Event class to represent events in the system.
    
    Attributes:
        name (str): Name of the event.
        location (str): Location of the event.
        date (str): Date of the event.
        time (str): Time of the event.
        description (str): Description of the event.
    """
    __tablename__ = "events"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    location = Column(String)
    date = Column(String)
    time = Column(String)
    description = Column(String)

    # ForeignKey to link to event owner
    owner_id = Column(Integer, ForeignKey("users.id"))

    # The user who created/owns the event
    owner = relationship("User", back_populates="owned_events")

    # Participants in the event (many-to-many)
    participants = relationship(
        "User",
        secondary=event_participants,
        back_populates="participating_events"
    )


class User(Base):
    """
    User class to represent users in the system.
    
    Attributes:
        username (str): Username of the user.
    """
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)

    # Events the user owns
    owned_events = relationship("Event", back_populates="owner")

    # Events the user participates in
    participating_events = relationship(
        "Event",
        secondary=event_participants,
        back_populates="participants"
    )


# Database class to handle event-related operations
class Database:
    def __init__(self, db_url: str):
        # check if the database file exists
        # if not, create a new database
        if not os.path.exists(f"{db_url}.db"):
            with open(f"{db_url}.db", "w") as db_file:
                pass

        engine = create_engine(f"sqlite:///{db_url}.db")
        Base.metadata.create_all(engine)
        self.session = sessionmaker(bind=engine)

    def add_event(self, event: Event):
        with self.session() as session:
            session.add(event)
            session.commit()
    
    def get_events(self):
        with self.session() as session:
            return session.query(Event).all()
        
    def get_event_by_id(self, event_id: int):
        with self.session() as session:
            return session.query(Event).filter(Event.id == event_id).first()
        
    def delete_event(self, event_id: int):
        with self.session() as session:
            event = session.query(Event).filter(Event.id == event_id).first()
            if event:
                session.delete(event)
                session.commit()

    def add_user(self, user: User):
        with self.session() as session:
            session.add(user)
            session.commit()

    def get_user_by_id(self, user_id: int):
        with self.session() as session:
            return session.query(User).filter(User.id == user_id).first()

    def get_user_by_username(self, username: str):
        with self.session() as session:
            return session.query(User).filter(User.username == username).first()

    def get_all_users(self):
        with self.session() as session:
            return session.query(User).all()
        
    def add_participant(self, event_id: int, user_id: int):
        with self.session() as session:
            event = session.query(Event).filter(Event.id == event_id).first()
            user = session.query(User).filter(User.id == user_id).first()
            if event and user:
                event.participants.append(user)
                session.commit()

    def remove_participant(self, event_id: int, user_id: int):
        with self.session() as session:
            event = session.query(Event).filter(Event.id == event_id).first()
            user = session.query(User).filter(User.id == user_id).first()
            if event and user:
                event.participants.remove(user)
                session.commit()

    def get_participants(self, event_id: int):
        with self.session() as session:
            event = session.query(Event).filter(Event.id == event_id).first()
            if event:
                return event.participants
            return []