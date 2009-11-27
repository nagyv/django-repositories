import os
from django.core.management.base import LabelCommand, CommandError
from django.template import Template, Context
from django.template.loader import get_template

from repositories import settings

class Command(LabelCommand):
    def __init__(self):
        super(Command, self).__init__()
        VCS = {}
        for key, value in settings.VCS_CONFIG.items():
            VCS[value['name'].lower()] = value
        self.VCS = VCS
        print VCS
    
    def handle_label(self, label, **options):
        try:
            vcs_config = self.VCS[label]
        except KeyError:
            raise CommandError("'%s' is not configured in REPO_VCS_CONFIG" % label)
        
        tmpl = get_template('repositories/apache2_%s.conf' % label)
        ctxt_dict = vcs_config.copy()
        ctxt_dict['wsgi_auth_script_path'] = os.path.dirname(settings.WSGI_AUTH_SCRIPT)
        ctxt_dict['wsgi_auth_script'] = settings.WSGI_AUTH_SCRIPT
        ctxt_dict['wsgi_script'] = settings.WSGI_SCRIPT
        ctxt = Context(ctxt_dict)
        print tmpl.render(ctxt)