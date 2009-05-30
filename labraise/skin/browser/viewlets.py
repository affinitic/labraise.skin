# -*- coding: utf-8 -*-
"""
labraise.skin

Licensed under the GPL license, see LICENCE.txt for more details.
Copyright by Affinitic sprl

$Id: viewlets.py 4587 2009-02-22 22:32:37Z alain
"""
from zope.component import getMultiAdapter
from plone.app.layout.viewlets.common import GlobalSectionsViewlet
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.LinguaPlone.browser.selector import TranslatableLanguageSelector


class LaBraiseSectionsViewlet(GlobalSectionsViewlet):
    render = ViewPageTemplateFile('templates/header_labraise.pt')

    def logo_tag(self):
        portal_state = getMultiAdapter((self.context, self.request),
                                        name=u'plone_portal_state')
        portal = portal_state.portal()
        logoName = portal.restrictedTraverse('base_properties').logoName
        return portal.restrictedTraverse(logoName).tag()


class LaBraiseFooterViewlet(GlobalSectionsViewlet):
    render = ViewPageTemplateFile('templates/footer_labraise.pt')


class LaBraiseLanguageSelector(TranslatableLanguageSelector):
    """Language selector for translatable content.
    """
    render = ViewPageTemplateFile('templates/selector.pt')
