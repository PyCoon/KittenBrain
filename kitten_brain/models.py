import locale
import time
import collections

import arrow
from sqlalchemy import Text, Column, Integer, ForeignKey, String, Float, create_engine, UniqueConstraint
from sqlalchemy.orm import sessionmaker, relationship, validates
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import InvalidRequestError, IntegrityError


locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')

Base = declarative_base()

engine = create_engine('sqlite:///foo.db')
Session = sessionmaker(bind=engine)
session = Session()

# Exceptions Deffinition
class DataBaseException(Exception):
    pass

class TooSmallString(DataBaseException):
    pass
class ObjectEverExist(DataBaseException):
    pass
class NullObject(DataBaseException):
    pass




def capitalyzer(chain):
    return chain.lower().capitalize()

def non_ascii_converter(string):
    """ Replace special french char by ascii equivalent """
    try:
        CHARS = {
        'a' : [ 'â', 'ä', 'à',] ,
        'e' : ['ê', 'ë', 'è',],
        'i': ['î', 'ï', 'ì',],
        'o' : ['ô', 'ö', 'ò',],
        'u' : ['û', 'ü', 'ù',],
        'y' : ['ŷ', 'ÿ', 'ỳ', ], }
        string = string.lower()
        for key, charlist in CHARS.items():
            for char in charlist:
                if char in string:
                    string = string.replace(char, key)
    except AttributeError:
        string = ""
    return string


class SessionManager:
    """ Manage Database connectiona nd commits """

    def __init__(self):
        self.errors = []

    def commit_it(self):

        try:

            with session.no_autoflush:

                session.add(self)
            session.commit()

        except (IntegrityError) as e:
            print(e)
            session.rollback()

            if 'UNIQUE constraint failed' in str(e).split(':')[0]:
                raise ObjectEverExist( "'{}' object ever exist !".format(self.__repr__()))
            elif 'NOT NULL constraint failed' in str(e).split(':')[0]:
                raise NullObject("'{}' object cannot be null !".format(self.__repr__()))
            else :
                raise Exception("'{}' raise an Exception but it can be evalued.\nError message= ( {} )!!!".format(self.__repr__(), e))

        except (InvalidRequestError) as e:
            session.rollback()
            raise Exception('Invalid request for {}'.foramt(self.__repr__()))

            print(e)
        except Exception as e:
            print(e)
            session.rollback()
            raise Exception('An error was occured for {}'.foramt(self.__repr__()))


        else:
            return self

        return False



class Category(Base, SessionManager):

    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    category_name = Column(String, unique=True, nullable=False)
    sub_category = relationship("SubCategory")
    content = relationship("Content")
    __table_args__ = (UniqueConstraint('category_name'),)

    def __init__(self, category_name):

        self.category_name = category_name.lower().capitalize()

    @validates('category_name')
    def validate_category_name(self, key, category_name):
        if len(category_name) < 3 :
            raise TooSmallString("String {} too small for {}" % (category_name, key) )
        return category_name


    def __repr__(self):
        return "%s" % self.category_name

    @validates('category')
    def validate_category(self, key, category):
        return capitalyzer(category)

class SubCategory(Base, SessionManager):

    __tablename__ = 'sub_category'
    id = Column(Integer, primary_key=True)
    sub_category_name =  Column(String, nullable=False)
    category_id = Column(Integer, ForeignKey('category.id', onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    content = relationship("Content")
    __table_args__ = (UniqueConstraint('sub_category_name'),)


    def __init__(self, category_id, sub_category_name ):


        self.sub_category_name = sub_category_name.lower().capitalize()
        self.category_id = category_id


    def __repr__(self):
        return "%s" % self.sub_category_name

    @validates('sub_category_name')
    def validate_sub_category_name(self, key, sub_category_name):
        if len(sub_category_name) < 3 :
            raise TooSmallString("String {} too small for {}" % (sub_category_name, key) )
        return sub_category_name


class Content(Base, SessionManager):
    __tablename__ = 'contentdata'

    id = Column(Integer, primary_key=True)
    date = Column(String, default=time.time)
    description = Column(String, nullable=True)
    parsed_description = Column(String, nullable=False)
    content = Column(Text, unique=True, nullable=False)
    category_id = Column(Integer, ForeignKey('category.id', onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    sub_category_id = Column(Integer, ForeignKey('sub_category.id', onupdate="CASCADE", ondelete="CASCADE"), nullable=False)

    __table_args__ = (UniqueConstraint("content"),)


    def __init__(self, category_id, sub_category_id, description, content):


        self.description = description
        self.parsed_description = non_ascii_converter(description)
        self.content = content
        self.category_id = category_id
        self.sub_category_id = sub_category_id



    @property
    def date_parsed(self):
        arw = arrow.get(float(self.date))
        return arw.humanize(locale='fr_fr')

    def __repr__(self):
        return "%s" % self.description

    @validates('content')
    def validate_sub_category_name(self, key, content):
        if len(content) < 3 :
            raise exception.TooSmallString("String {} too small for {}" % (content, key) )
        return content


Base.metadata.create_all(engine)


class BaseIface:

    def get_all_category():
        return session.query(Category).all()


    def get_sub_category(category):
        q = session.query(SubCategory).filter(SubCategory.category_id == category)
        return q


    def get_all_content():
        return session.query(Content).all()


    def get_content(category, sub_category=None, description=''):
        """ Search content, must have a category, possible empty description or sub_categiory"""
        if category and not sub_category:
            q = session.query(Content).filter(Content.category_id == category)
        elif category and sub_category:
            q = session.query(Content).filter(Content.category_id == category,
                                              Content.sub_category_id == sub_category)
        else:
            raise(BaseException, 'Il faut une category, celle là = {}'.format(category))
        if description == '' or description == ''  :
            return q

        parsed_description = non_ascii_converter(description)

        valid_description = [obj for obj in q if parsed_description == obj.parsed_description]

        if len(valid_description) > 0:
            return valid_description

        splited_description = parsed_description.split()

        ordr_dict = collections.defaultdict(list)
        for ind, obj in enumerate(q):
            cp = 0

            for word in splited_description:
                if word in obj.parsed_description:
                    cp += 1
                if cp > 0:
                    ordr_dict[cp].append(q[ind])
        result = []

        for key in collections.OrderedDict(sorted(ordr_dict.items())):
            result += result + ordr_dict[key]
        return list(set(result))


    def get_content_by_date(category, sub_category, date, desc=True):
        if desc:
            q = session.query(Content).filter(Content.category_id == category,
                                                  Content.sub_category_id == sub_category).order_by(
                Content.date.amount.desc())

        else:
            q = session.query(Content).filter(Content.category_id == category,
                                                  Content.sub_category_id == sub_category).order_by(
                Content.date.amount.asc())
        return q


    def add_category(category_name):
        try:
            q = Category(category_name)
            q.commit_it()
        except ObjectEverExist:
            q = session.query(Category).filter(Category.category_name == category_name.lower().capitalize()).one()
        return q


    def add_sub_category(category, sub_category_name):
        try:
            q = SubCategory(category, sub_category_name)
            q.commit_it()
        except ObjectEverExist:
            q = session.query(SubCategory).filter(SubCategory.category_id == category, SubCategory.sub_category_name==sub_category_name.lower().capitalize()).one()

        return q

    def add_content(category, sub_category, description, content):
        q = Content( category, sub_category, description, content)
        q.commit_it()
        return q

    def delete_content(content_id):
        session.query(Content).filter(Content.id == content_id).delete(synchronize_session=False)
        return True

