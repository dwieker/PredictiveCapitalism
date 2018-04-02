# -*- coding: utf-8 -*-

import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base, DeferredReflection
import time
import os
import gplay_store.settings as SETTINGS
dirname = os.path.dirname(__file__)
Base = declarative_base(cls=DeferredReflection)

class App(Base):
    __tablename__ = "dim_apps"

class GplayPipeline(object):

    def __init__(self):
        sqlalchemy.String(1000, convert_unicode=True)
        credentials = (
            SETTINGS.DB_USERNAME,
            SETTINGS.DB_PASSWORD,
            SETTINGS.DB_ENDPOINT,
            SETTINGS.DB_NAME,
        )
        db_uri = "mysql+pymysql://%s:%s@%s/%s?use_unicode=yes&charset=utf8mb4" % credentials
        engine = sqlalchemy.create_engine(db_uri)
        Base.prepare(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()

        # Create table if not exists
        create_query = """
        CREATE TABLE IF NOT EXISTS dim_apps (
            ID INT,
            appid TEXT,
            name TEXT,
            genre VARCHAR(20),
            price DOUBLE,
            rating DOUBLE,
            ratings INT,
            description TEXT,
            size DOUBLE,
            installs INT,
            version VARCHAR(20),
            page_update_time VARCHAR(20),
            ds VARCHAR(10)
        );
        ALTER TABLE dim_apps ADD PRIMARY KEY (ID, ds);
        """

    def process_item(self, item, spider):
        item['ds'] = SETTINGS.DATEID
        try:
            self.session.bulk_insert_mappings(App, [item])
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            print(e)
            SETTINGS.logger.error(str(e))
        return item
