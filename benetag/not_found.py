import os
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

import bene_util


"""
not found handler
"""
class NotFound(webapp.RequestHandler):
    def get(self):
        template_values = bene_util.initTemplate(self.request.uri)
        path = os.path.join(os.path.dirname(__file__), 'not_found.html')
        self.response.out.write(template.render(path, template_values))
        return
    
    '''
    Exception handler
    '''
    def handle_exception(self, exception, debug_mode):
        if debug_mode:
            super(NotFound, self).handle_exception(exception, debug_mode)
        else:
            template_values = bene_util.initTemplate(self.request.uri)
            path = os.path.join(os.path.dirname(__file__), 'not_found.html')
            self.response.out.write(template.render(path, template_values))
            return