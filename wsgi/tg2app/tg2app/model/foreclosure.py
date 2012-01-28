# -*- coding: utf-8 -*-
"""Sample model module."""

from sqlalchemy import *
from sqlalchemy.orm import mapper, relation
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Integer, Unicode, Float, Boolean, DateTime

from tg2app.model import DeclarativeBase, metadata, DBSession

from datetime import datetime


class Foreclosure(DeclarativeBase):
    """
    {'Book': u'NOTICE OF PENDENCY',
     'Book Page': u'1160 52',
     'Control No': u'201109120267',
     'Filing Date': u'9/12/2011',
     'Formatted Address': '277 Raspberry Patch Dr, Rochester, NY 14612, USA',
     'Grantee': u'SUKHENKO CHRISTINE M',
     'Grantor': u'WELLS FARGO BANK NA',
     'Index Detail': u'',
     'Instrument Type': u'NOTICE OF PENDENCY MORTGAGE FORECLOSURE',
     'Land Description': u'',
     'Latitude': 43.248163,
     'Longitude': -77.727037,
     'XReffed Owner': u'Bob Loblaw',
     'Map Ready': True,
     'Property Address': u'277 RASPBERRY PATCH GREECE',
     'Reference 1': u'I2011010924',
     'Reference 2': u'MCZ010184',
     'View Image': u'(4)'}
    """
    __tablename__ = 'foreclosure_table'

    control_no = Column(Unicode(255), nullable=False, primary_key=True)

    book = Column(Unicode(255), nullable=False)
    book_page = Column(Unicode(255), nullable=False)
    filing_date = Column(DateTime, nullable=False)
    formatted_address = Column(Unicode(255), nullable=False)
    grantee = Column(Unicode(255), nullable=False)
    grantor = Column(Unicode(255), nullable=False)
    index_detail = Column(Unicode(255), nullable=False)
    instrument_type = Column(Unicode(255), nullable=False)
    land_description = Column(Unicode(255), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    map_ready = Column(Boolean, nullable=False)
    property_address = Column(Unicode(255), nullable=False)
    reference_1 = Column(Unicode(255), nullable=False)
    reference_2 = Column(Unicode(255), nullable=False)
    view_image = Column(Unicode(255), nullable=False)
    xreffed_owner = Column(Unicode(255), nullable=False)
    xref_updated = Column(DateTime, nullable=False, default=datetime.now)


    def csv_headers(self):
        return [
            key for key, value in Foreclosure.__dict__.iteritems()
            if type(getattr(Foreclosure, key)) == InstrumentedAttribute
        ]


    def to_csv(self):
        return "|".join([
            str(getattr(self, attr)) for attr in self.csv_headers()
        ])

    def to_dict(self):
        return dict([(attr, getattr(self, attr))
                     for attr in self.csv_headers()])

    def to_geojson(self):
        d = self.to_dict()
        d['filing_date'] = d['filing_date'].strftime('%m/%d/%Y')
        return d
