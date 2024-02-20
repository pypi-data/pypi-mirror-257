# -*- coding: utf-8 -*-
from collective.plausible.testing import COLLECTIVE_PLAUSIBLE_FUNCTIONAL_TESTING
from collective.plausible.testing import COLLECTIVE_PLAUSIBLE_INTEGRATION_TESTING
from collective.plausible.views.plausible_view import IPlausibleView
from collective.plausible.views.plausible_view import PlausibleView
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from unittest import mock
from zope.component import getMultiAdapter
from zope.component import queryMultiAdapter
from zope.interface.interfaces import ComponentLookupError

import os
import unittest


class ViewsIntegrationTest(unittest.TestCase):

    layer = COLLECTIVE_PLAUSIBLE_INTEGRATION_TESTING

    def setUp(self):
        self.request = self.layer["request"]
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        api.content.create(self.portal, "Folder", "other-folder")
        api.content.create(self.portal, "Document", "front-page")

    def test_plausible_view_is_registered(self):
        view = getMultiAdapter(
            (self.portal, self.portal.REQUEST), name="plausible-view"
        )
        self.assertTrue(IPlausibleView.providedBy(view))

    def test_plausible_view_not_matching_interface(self):
        view_found = True
        try:
            view = getMultiAdapter(
                (self.portal["front-page"], self.portal.REQUEST), name="plausible-view"
            )
        except ComponentLookupError:
            view_found = False
        else:
            view_found = IPlausibleView.providedBy(view)
        self.assertFalse(view_found)

    def set_registry_records(self):
        api.portal.set_registry_record("collective.plausible.site", "site-registry.be")
        api.portal.set_registry_record("collective.plausible.token", "token-registry")
        api.portal.set_registry_record("collective.plausible.url", "url-registry.be")

    @mock.patch.dict(
        os.environ,
        {
            "COLLECTIVE_PLAUSIBLE_SITE": "",
            "COLLECTIVE_PLAUSIBLE_TOKEN": "",
            "COLLECTIVE_PLAUSIBLE_URL": "",
        },
    )
    def test_noenv(self):
        view = PlausibleView(self.portal, self.request)
        self.assertFalse(view.is_plausible_set)
        self.set_registry_records()
        self.assertTrue(view.is_plausible_set)
        self.assertEqual(
            view.get_iframe_src,
            "https://url-registry.be/share/site-registry.be?auth=token-registry&embed=true&theme=light&background=transparent",
        )
        self.assertEqual(
            view.get_embedhostjs_src,
            "https://url-registry.be/js/embed.host.js",
        )

    @mock.patch.dict(
        os.environ,
        {
            "COLLECTIVE_PLAUSIBLE_SITE": "site-varenv.be",
            "COLLECTIVE_PLAUSIBLE_TOKEN": "token-varenv",
            "COLLECTIVE_PLAUSIBLE_URL": "url-varenv.be",
        },
    )
    def test_env(self):
        view = PlausibleView(self.portal, self.request)
        self.assertTrue(view.is_plausible_set)
        self.assertEqual(
            view.get_iframe_src,
            "https://url-varenv.be/share/site-varenv.be?auth=token-varenv&embed=true&theme=light&background=transparent",
        )
        self.assertEqual(
            view.get_embedhostjs_src,
            "https://url-varenv.be/js/embed.host.js",
        )
        self.set_registry_records()
        self.assertEqual(
            view.get_iframe_src,
            "https://url-varenv.be/share/site-varenv.be?auth=token-varenv&embed=true&theme=light&background=transparent",
        )
        self.assertEqual(
            view.get_embedhostjs_src,
            "https://url-varenv.be/js/embed.host.js",
        )

    def test_plausible_view(self):
        view = queryMultiAdapter((self.portal, self.request), name="plausible-view")
        self.assertNotIn("iframe", view())
        self.assertIn("Plausible analytics is not set", view())
        self.set_registry_records()
        self.assertIn("iframe", view())
        self.assertNotIn("Plausible analytics is not set", view())


class ViewsFunctionalTest(unittest.TestCase):

    layer = COLLECTIVE_PLAUSIBLE_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
