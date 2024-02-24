#!/usr/bin/python3
"""This module defines the DBStorage class"""

import models
from models.base_model import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

import os
HBNB_MYSQL_USER = os.getenv('HBNB_MYSQL_USER')
HBNB_MYSQL_PWD = os.getenv('HBNB_MYSQL_PWD')
HBNB_MYSQL_HOST = os.getenv('HBNB_MYSQL_HOST')
HBNB_MYSQL_DB = os.getenv('HBNB_MYSQL_DB')

env = os.getenv("HBNB_ENV")

class DBStorage:
    """A class for interacting with the MySQL database"""
    __engine = None
    __session = None

    def __init__(self):
        """Creates the engine and session"""
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.format(
            HBNB_MYSQL_USER,
            HBNB_MYSQL_PWD,
            HBNB_MYSQL_HOST,
            HBNB_MYSQL_DB), pool_pre_ping=True)
        if (env == 'test'):
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Query the current session and list all instances of cls
        """
        result = {}
        if cls:
            for instance in self.__session.query(cls).all():
                key = "{}.{}".format(cls.__name__, instance.id)
                instance.to_dict()
                result.update({key: instance})
        else:
            for table in models.dummy_tables:
                cls = models.dummy_tables[table]
                for instance in self.__session.query(cls).all():
                    key = "{}.{}".format(cls.__name__, instance.id)
                    instance.to_dict()
                    result.update({key: instance})
        return result

    def rollback(self):
        """rollback changes
        """
        self.__session.rollback()

    def new(self, obj):
        """add object to current session
        """
        self.__session.add(obj)

    def save(self):
        """commit current done work
        """
        self.__session.commit()

    def delete(self, obj=None):
        """Delete obj from the current database session if not None
        """
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """reload the session
        """
        Base.metadata.create_all(self.__engine)
        Session = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Scope = scoped_session(Session)
        self.__session = Scope()

    def close(self):
        """display our HBNB data
        """
        self.__session.__class__.close(self.__session)
        self.reload()
