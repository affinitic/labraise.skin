# -*- coding: utf-8 -*-

from zope.component import getUtility
from zope.component import getMultiAdapter
from zope.app.component.interfaces import ISite
from plone.portlets.interfaces import IPortletManager
from plone.portlets.interfaces import IPortletAssignmentMapping
from plone.app.portlets.portlets import navigation
from Products.CMFCore.utils import getToolByName
from Products.Five.component import enableSite
from Products.LinguaPlone.I18NBaseObject import AlreadyTranslated

import logging
logger = logging.getLogger('labraise.skin')

LANGUAGES = ['fr', 'nl', 'en']


def setupVarious(context):
    portal = context.getSite()
    if not ISite.providedBy(portal):
        enableSite(portal)
    setupLanguages(portal)
    clearPortlets(portal)
    setupNavigationPortlet(portal)
    # createContent(portal)


def setupLanguages(portal):
    lang = getToolByName(portal, 'portal_languages')
    lang.supported_langs = LANGUAGES
    lang.setDefaultLanguage('fr')
    lang.display_flags = 1


def createContent(portal):
    # Contact
    folder = createFolder(portal, "contact", "Contact")
    createPage(folder, "contact", "Contact")
    folder.setDefaultPage('contact')
    translations = createTranslationsForObject(folder)
    # Menu
    folder = createFolder(portal, "menu", "Menu")
    createPage(folder, "menu", "Menu")
    folder.setDefaultPage('menu')
    translations = createTranslationsForObject(folder)
    # Galerie
    folder = createFolder(portal, "galerie", "Galerie")
    translations = createTranslationsForObject(folder)
    # Réservation
    folder = createFolder(portal, "reservation", "Réservation")
    createPage(folder, "reservation", "Réservation")
    folder.setDefaultPage('reservation')
    translations = createTranslationsForObject(folder)


def publishObject(obj):
    portal_workflow = getToolByName(obj, 'portal_workflow')
    if portal_workflow.getInfoFor(obj, 'review_state') in ['visible', 'private']:
        portal_workflow.doActionFor(obj, 'publish')
    return


def createPage(parentFolder, documentId, documentTitle):
    if documentId not in parentFolder.objectIds():
        parentFolder.invokeFactory('Document', documentId, title=documentTitle)
    document = getattr(parentFolder, documentId)
    publishObject(document)
    return document


def createFolder(parentFolder, folderId, folderTitle):
    if folderId not in parentFolder.objectIds():
        parentFolder.invokeFactory('Folder', folderId, title=folderTitle)
    createdFolder = getattr(parentFolder, folderId)
    createdFolder.reindexObject()
    publishObject(createdFolder)
    createdFolder.reindexObject()
    return createdFolder


def createTranslationsForObject(obj):
    translatedObjects = []

    for lang in LANGUAGES:
        try:
            obj.addTranslation(lang)
        except AlreadyTranslated:
            pass
        translated = obj.getTranslation(lang)
        publishObject(translated)
        translated.reindexObject()
        translatedObjects.append(translated)

    return translatedObjects


def getManager(folder, column):
    if column == 'left':
        manager = getUtility(IPortletManager, name=u'plone.leftcolumn',
                             context=folder)
    else:
        manager = getUtility(IPortletManager, name=u'plone.rightcolumn',
                             context=folder)
    return manager


def clearColumnPortlets(folder, column):
    manager = getManager(folder, column)
    assignments = getMultiAdapter((folder, manager, ),
                                  IPortletAssignmentMapping)
    for portlet in assignments:
        del assignments[portlet]


def clearPortlets(folder):
    clearColumnPortlets(folder, 'left')
    clearColumnPortlets(folder, 'right')


def setupNavigationPortlet(folder):
    manager = getManager(folder, 'left')
    assignments = getMultiAdapter((folder, manager, ),
                                  IPortletAssignmentMapping)

    assignment = navigation.Assignment(name=u"Navigation",
                                       root=None,
                                       currentFolderOnly=False,
                                       includeTop=False,
                                       topLevel=0,
                                       bottomLevel=1)
    assignments['navtree'] = assignment
