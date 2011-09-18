# -*- coding: utf-8 -*-
"""Main Controller"""

from tg import expose, flash, require, url, request, redirect
from tg.i18n import ugettext as _, lazy_ugettext as l_
from tgext.admin.tgadminconfig import TGAdminConfig
from tgext.admin.controller import AdminController
from repoze.what import predicates

from tg2app.lib.base import BaseController
from tg2app.model import DBSession, metadata
from tg2app import model
from tg2app.controllers.secure import SecureController

from tg2app.controllers.error import ErrorController

from tg2app.widgets import ForeclosureGrid, ForeclosurePie
import tw2.jit

__all__ = ['RootController']


class RootController(BaseController):
    """
    The root controller for the tg2app application.

    All the other controllers and WSGI applications should be mounted on this
    controller. For example::

        panel = ControlPanelController()
        another_app = AnotherWSGIApplication()

    Keep in mind that WSGI applications shouldn't be mounted directly: They
    must be wrapped around with :class:`tg.controllers.WSGIAppController`.

    """
    secc = SecureController()

    admin = AdminController(model, DBSession, config_type=TGAdminConfig)

    error = ErrorController()

    @expose('tg2app.templates.index')
    def index(self):
        """Handle the front-page."""
        redirect('/grid')

    @expose('json')
    def jqgrid(self, *args, **kwargs):
        return ForeclosureGrid.request(request).body

    @expose('tg2app.templates.widget')
    def grid(self):
        return dict(widget=ForeclosureGrid)

    @expose('tg2app.templates.widget')
    def grantor(self, top=5):
        return self._granted('grantor', top)

    @expose('tg2app.templates.widget')
    def grantee(self, top=5):
        return self._granted('grantee', top)

    @expose('tg2app.templates.widget')
    def day(self):
        return self._time('day')

    @expose('tg2app.templates.widget')
    def month(self):
        return self._time('month')

    @expose('tg2app.templates.widget')
    def year(self):
        return self._time('year')

    @expose('tg2app.templates.widget')
    def dayofweek(self):
        return self._time('dayofweek')

    def _granted(self, attr, top):
        if not attr in ['grantor', 'grantee']:
            redirect('/')

        try:
            top = int(top)
        except TypeError:
            redirect('/' + attr)

        closures = model.Foreclosure.query.all()

        bucket = {}
        for c in closures:
            bucket[getattr(c, attr)] = bucket.get(getattr(c, attr), 0) + 1

        items = bucket.items()
        items.sort(lambda a, b: cmp(b[1], a[1]))
        items = [(item[0] + "(%i)" % item[1], item[1]) for item in items]

        bucket = dict(items[:top])
        other_count = sum([item[1] for item in items[top:]])
        bucket['OTHER (%i)' % other_count] = other_count

        data = {
            'labels' : ['Foreclosures'],
            'values' : [
                {
                    'label': key,
                    'values': [value],
                } for key, value in bucket.iteritems()
            ]
        }

        pie = ForeclosurePie(data=data)

        return dict(widget=pie)

    def _time(self, attr):
        lookup = {
            'day': '%d',
            'month': '%b',
            'year': '%Y',
            'dayofweek': '%a',
        }

        if attr not in lookup.keys():
            redirect('/')

        closures = model.Foreclosure.query.all()

        fmt = lookup[attr]
        bucket = {}
        for c in closures:
            bucket[c.filing_date.strftime(fmt)] = \
                    bucket.get(c.filing_date.strftime(fmt), 0) + 1

        items = bucket.items()
        items = [(item[0] + "(%i)" % item[1], item[1]) for item in items]

        bucket = dict(items)

        data = {
            'labels' : ['Foreclosures'],
            'values' : [
                {
                    'label': key,
                    'values': [value],
                } for key, value in bucket.iteritems()
            ]
        }

        pie = ForeclosurePie(data=data)

        return dict(widget=pie)
