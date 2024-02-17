# -*- coding: utf-8 -*-

from plone import api
from plone.app.upgrade.utils import loadMigrationProfile
from Products.CMFCore.utils import getToolByName


def reload_gs_profile(context):
    loadMigrationProfile(
        context,
        "profile-library.policy:default",
    )


# silly : default_language = fr
# root and folders are fr-be !
def change_language(context):
    pl = api.portal.get_tool("portal_languages")
    default_language = pl.getDefaultLanguage()
    root = api.portal.get()
    brains = api.content.find(root)
    for brain in brains:
        obj = brain.getObject()
        if obj.language != default_language:
            obj.language = default_language
    root.language = default_language


def configure_faceted(context):
    pass


def upgrade_1004_to_1005(context):
    setup_tool = getToolByName(context, "portal_setup")
    setup_tool.runAllImportStepsFromProfile("profile-collective.plausible:default")
