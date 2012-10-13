from zope.interface import implements
from zope.i18n import translate
from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory

from plone.contentrules.engine.interfaces import IRuleStorage
from plone.memoize.instance import memoize
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from plone.app.layout.viewlets.common import ViewletBase
from plone.app.contentrules import PloneMessageFactory as _
from plone.app.contentrules.browser.interfaces import IContentRulesControlPanel
from plone.app.contentrules.rule import get_assignments

def get_trigger_class(trigger):
    return "trigger-%s" % trigger.__identifier__.split('.')[-1].lower()


class ContentRulesControlPanel(BrowserView):
    """Manage rules in a the global rules container
    """
    implements(IContentRulesControlPanel)
    template = ViewPageTemplateFile('templates/controlpanel.pt')

    def __call__(self):
        form = self.request.form
        ruleIds = form.get('ruleId', [])
        storage = getUtility(IRuleStorage)
        if form.get('form.button.SaveSettings', None) is not None:
            storage.active = form.get('global_enable', True)
        elif form.get('form.button.EnableRule', None) is not None:
            for r in ruleIds:
                if r in storage:
                    storage[r].enabled = True
        elif form.get('form.button.DisableRule', None) is not None:
            for r in ruleIds:
                if r in storage:
                    storage[r].enabled = False
        elif form.get('form.button.DeleteRule', None) is not None:
            for r in ruleIds:
                if r in storage:
                    del storage[r]
        return self.template()

    def globally_enabled(self):
        storage = getUtility(IRuleStorage)
        return storage.active

    def registeredRules(self):
        selector = self.request.get('ruleType', 'all')
        rules = self._getRules()

        events = dict([(e.value, e.token) for e in self._events()])
        info = []
        for r in rules:
            trigger_class = get_trigger_class(r.event)
            enabled_class = r.enabled and 'state-enabled' or 'state-disabled'
            assigned = len(get_assignments(r)) > 0
            info.append({'id': r.__name__,
                        'title': r.title,
                        'description': r.description,
                        'enabled': r.enabled,
                        'assigned': assigned,
                        'trigger': events[r.event],
                        'row_class': "%s %s" % (trigger_class, enabled_class)
                        })

        return info

    def ruleTypesToShow(self):
        selector = []
        for event in self._events():
            eventname = translate(event.token, context=self.request, domain='plone')
            selector.append(dict(id = get_trigger_class(event.value),
                                 title = _(u"Trigger: ${name}", mapping = {'name': eventname})), )

        selector += ({'id': 'state-enabled', 'title': _(u"label_rule_enabled", default=u"Enabled")},
                     {'id': 'state-disabled', 'title': _(u"label_rule_disabled", default=u"Disabled"), },
                     # {'id': 'state-rule-assigned', 'title': _(u"Rule is in use")},
                     # {'id': 'state-rule-not-assigned', 'title': _(u"Rule is not assigned anywhere"), },
                     )

        return selector

    def _getRules(self):
        storage = getUtility(IRuleStorage)
        return storage.values()

    @memoize
    def _events(self):
        eventsFactory = getUtility(IVocabularyFactory, name="plone.contentrules.events")
        return eventsFactory(self.context)

