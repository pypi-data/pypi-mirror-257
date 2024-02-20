# -*- coding: utf-8 -*-

from . import logger


from .base import reload_gs_profile
from collective.plausible import _
from plone.registry import Record, field
from plone.registry.interfaces import IRegistry
from zope.component import getUtility


def upgrade(setup_tool=None):
    """ """
    logger.info("Running upgrade (Python): Add action linking to @@plausible-view")
    registry = getUtility(IRegistry)
    if "collective.plausible.link_user_action" not in registry.records:
        registry_field = field.Bool(
            title=_("Add a link in the user menu"),
            description=_("Add a link to the statistics browser view in the user menu"),
            default=True,
            required=False,
            readonly=False,
        )
        registry_record = Record(registry_field)
        registry.records["collective.plausible.link_user_action"] = registry_record
    reload_gs_profile(setup_tool)
