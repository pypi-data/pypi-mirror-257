# -*- coding: utf-8 -*-

from collective.plausible.utils import get_plausible_vars
from Products.Five.browser import BrowserView
from zope.interface import implementer
from zope.interface import Interface


# from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class IPlausibleView(Interface):
    """Marker Interface for IPlausibleView"""


@implementer(IPlausibleView)
class PlausibleView(BrowserView):
    # If you want to define a template here, please remove the template from
    # the configure.zcml registration of this view.
    # template = ViewPageTemplateFile('plausible_view.pt')

    def __call__(self):
        # Implement your own actions:
        return self.index()

    @property
    def is_plausible_set(self):
        return True if get_plausible_vars() else False

    @property
    def get_embedhostjs_src(self):
        vars = get_plausible_vars()
        return f"https://{vars['plausible_url']}/js/embed.host.js"

    @property
    def get_iframe_src(self):
        vars = get_plausible_vars()
        return f"https://{vars['plausible_url']}/share/{vars['plausible_site']}?auth={vars['plausible_token']}&embed=true&theme=light&background=transparent"
