# -*- coding: utf-8 -*-

import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base, DeferredReflection
import time
import os
import gplay_store.config as CONFIG
dirname = os.path.dirname(__file__)
Base = declarative_base(cls=DeferredReflection)

class App(Base):
    __tablename__ = "dim_apps"

class GplayPipeline(object):

    def __init__(self):
        engine = sqlalchemy.create_engine("mysql+pymysql://%s:%s@%s/%s"%("root", "password", "localhost","PC"))
        Base.prepare(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def process_item(self, item, spider):
        item['ds'] = CONFIG.DATEID
        try:
            self.session.bulk_insert_mappings(App, [item])
            self.session.commit()
        except:
            self.session.rollback()
        return item
