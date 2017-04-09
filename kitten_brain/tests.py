import sys, os
import sys
import time
import locale
from sqlalchemy import Text, Column, Integer, ForeignKey, String, Float, create_engine, UniqueConstraint

from sqlalchemy.orm import sessionmaker, relationship, validates
from sqlalchemy.sql.expression import insert
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import InvalidRequestError, IntegrityError
from sqlalchemy.orm.exc import NoResultFound
import time
import collections

import arrow

import collections
import xml.etree.cElementTree as ET

from kitten_brain.models import *

import pytest


sys.path.append(os.path.dirname(os.path.realpath(__file__)))


# Real tests

def test_capitalyzer():
    """Capitalyze and lowerise"""
    assert capitalyzer('toTo') == 'Toto'

def test_non_ascii_converter():
    """Replace sépcial utf-8 char by ascii char"""
    assert non_ascii_converter('âäàêëèîïìôöòûüùŷÿỳ AAA') == 'aaaeeeiiiooouuuyyy aaa'

@pytest.fixture()
def set_up_base():
    if os.path.isfile('test.db'):
        os.remove('test.db')
    engine = create_engine('sqlite:///test.db')
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


def set_up_category_obj():
    q = Category("random catéégory")
    q = q.commit_it()
    assert q.category_name == "random catéégory".lower().capitalyze()


def test_category_exeption ():
    """Test category class"""
    try:
        q = Category("random catéégory")
    except ObjectEverExist as e:
        assert e.isintance(ObjectEverExist) == True


@pytest.fixture()
def set_up_baseiface():
    i = BaseIface()
    return i

def test_add_category ():
    """ """
    q = set_up_baseiface().add_category("Love")
    assert q.category_name == "Love".lower().capitalize()

def test_add_sub_category ():
    """ """
    q = set_up_baseiface().add_category("Père Noël")
    q1 = set_up_baseiface().add_sub_category("Père Noë")

    assert q == q1











