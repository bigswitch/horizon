import json
import datetime
import sqlalchemy as sa
from neutron.db import models_v2
from neutron.db import model_base
from sqlalchemy.dialects import postgresql
from sqlalchemy.dialects.mysql.base import VARCHAR
from sqlalchemy.orm import relationship, backref, sessionmaker
from sqlalchemy.types import Enum, TIMESTAMP, TypeDecorator
from sqlalchemy import Table, Column, ForeignKey, func, Integer, create_engine

def debug(msg):
            f = open('haha', 'a')
            f.write(msg)
            f.close()

class JSONEncodedDict(TypeDecorator):
    """Represents an immutable structure as a json-encoded string.
    Usage::
        JSONEncodedDict(255)
    """
    impl = VARCHAR
    def process_bind_param(self, value, dialect):
        if value is not None:
            value = json.dumps(value)
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            value = json.loads(value)
        return value

class ReachabilityTest(model_base.BASEV2):
    '''
    A table to store user configured reachability tests.
    '''
    __tablename__ = 'reachabilitytest'
    id = Column(Integer, primary_key=True)
    tenant_id = sa.Column(sa.String(64), primary_key=False, nullable=False)
    test_id = sa.Column(sa.String(64), primary_key=False, nullable=False)
    src_tenant_id = sa.Column(sa.String(64), primary_key=False, nullable=False)
    src_segment_id = sa.Column(sa.String(64), primary_key=False, nullable=False)
    src_ip = sa.Column(sa.String(16), nullable=False, primary_key=False)
    dst_tenant_id = sa.Column(sa.String(64), nullable=False, primary_key=False)
    dst_segment_id = sa.Column(sa.String(64), nullable=False, primary_key=False)
    dst_ip = sa.Column(sa.String(16), nullable=False)
    expected_result = sa.Column(Enum("reached destination", "dropped by route", "dropped by policy", \
                                     "dropped due to private segment", "packet in", "forwared", "dropped", "multiple sources", \
                                     "unsupported", "invalid input", name="expected_result"), nullable=False)

class ReachabilityTestResult(model_base.BASEV2):
    '''
    A table to store the results of user configured reachability tests.
    '''
    __tablename__ = 'reachabilitytestresult'
    id = Column(Integer, primary_key=True)
    test_primary_key = sa.Column(Integer, ForeignKey('reachabilitytest.id'), nullable=False)
    tenant_id = sa.Column(sa.String(64), primary_key=False, nullable=False)
    test_id = sa.Column(sa.String(64), primary_key=False, nullable=False)
    test_time = sa.Column(TIMESTAMP(timezone=True), primary_key=False, nullable=False, default=func.now())
    test_result = sa.Column(Enum("PASS", "FAIL", "PENDING"), nullable=False)
    detail = sa.Column(JSONEncodedDict(255), nullable=True)

    reachabilitytest = relationship("ReachabilityTest", backref=backref('reachabilitytestresult',\
                                                                        order_by=id, uselist=True,\
                                                                        cascade='delete,all'))

class ReachabilityQuickTest(model_base.BASEV2):
    '''
    A table to store user configured quick tests.
    '''
    __tablename__ = 'reachabilityquicktest'
    id = Column(Integer, primary_key=True)
    tenant_id = sa.Column(sa.String(64), primary_key=False, nullable=False)
    src_tenant_id = sa.Column(sa.String(64), primary_key=False, nullable=False)
    src_segment_id = sa.Column(sa.String(64), primary_key=False, nullable=False)
    src_ip = sa.Column(sa.String(16), nullable=False, primary_key=False)
    dst_tenant_id = sa.Column(sa.String(64), nullable=False, primary_key=False)
    dst_segment_id = sa.Column(sa.String(64), nullable=False, primary_key=False)
    dst_ip = sa.Column(sa.String(16), nullable=False)
    expected_result = sa.Column(Enum("reached destination", "dropped by route", "dropped by policy", \
                                     "dropped due to private segment", "packet in", "forwared", "dropped", "multiple sources", \
                                     "unsupported", "invalid input", name="expected_result"), nullable=False)

class ReachabilityQuickTestResult(model_base.BASEV2):
    '''
    A table to store the results of user configured quick tests.
    '''
    __tablename__ = 'reachabilityquicktestresult'
    id = Column(Integer, primary_key=True)
    test_primary_key = sa.Column(Integer, ForeignKey('reachabilityquicktest.id'), nullable=False)
    tenant_id = sa.Column(sa.String(64), primary_key=False, nullable=False)
    test_time = sa.Column(TIMESTAMP(timezone=True), primary_key=False, nullable=False, default=func.now())
    test_result = sa.Column(Enum("PASS", "FAIL", "PENDING"), nullable=False)
    detail = sa.Column(JSONEncodedDict(255), nullable=True)

    reachabilitytest = relationship("ReachabilityQuickTest", backref=backref('reachabilityquicktestresult',\
                                                                             order_by=id, uselist=True,\
                                                                             cascade='delete,all'))

db_ip = '127.0.0.1'
db_user = 'root'
db_pwd = 'password'
tenant_id = 'admin'
engine_string = "mysql+mysqldb://%s:%s@%s/neutron?charset=utf8" % (db_user, db_pwd, db_ip)
engine = create_engine(engine_string)
Session = sessionmaker(bind=engine)
Base = model_base.BASEV2()
Base.metadata.create_all(bind=engine)

