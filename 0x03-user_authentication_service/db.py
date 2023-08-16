#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from user import User
from user import Base


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email, hashed_password):
        """returns a User object"""
        user_add = User(email=email, hashed_password=hashed_password)
        self._session.add(user_add)
        self._session.commit()
        return user_add

    def find_user_by(self, **kwargs) -> User:
        """ this function queries the db """
        session = self._session
        try:
            user = session.query(User).filter_by(**kwargs).one()
            return user
        except InvalidRequestError:
            raise
        except NoResultFound:
            raise

    def update_user(self, user_id, **kwargs) -> None:
        to_update = self.find_user_by(id = user_id)
        if to_update:
            for attr, value in kwargs.items():
                if hasattr(to_update, attr):
                    setattr(to_update, attr, value)        
        else:
            raise ValueError
        self._session.commit()
