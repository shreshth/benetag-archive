from google.appengine.ext import db, webapp
from google.appengine.ext.webapp import template
import bene_util
import os
import urllib



"""
Generic class to view a product line, config, unit
"""
class View(webapp.RequestHandler):
    def get(self):
        ID = bene_util.sanitize(self.request.get('id'))
        if not ID:
            '''
            TODO: if no id is sent ?
            '''
            self.redirect('/')
            return
        generic = db.get(ID)
        ''' an error in getting the item will be redirected to exception handler'''
        
        # if its a product line, show its default config
        if generic.isLine:
            if generic.numConfigs() > 1:
                self.redirect('/viewproduct?%s' % urllib.urlencode({'id': generic.key()}))
                return
            else:
                _configs = generic.getConfigs()
                for _config in _configs:
                    if _config:
                        self.redirect('/viewconfig?%s' % urllib.urlencode({'id': _config.key()}))
                        return
                return
                        
        if generic.isConfig:
            self.redirect('/viewconfig?%s' % urllib.urlencode({'id': generic.key()}))
            return
        if generic.isUnit:
            self.redirect('/viewunit?%s' % urllib.urlencode({'id': generic.key()}))
            return
                                                            
        db.get('abc') # force exception handler
                                                                                                   
    '''
    Exception handler
    '''
    def handle_exception(self, exception, debug_mode):
        if debug_mode:
            super(View, self).handle_exception(exception, debug_mode)
        else:
            template_values = bene_util.initTemplate(self.request.uri)
            path = os.path.join(os.path.dirname(__file__), 'not_found.html')
            self.response.out.write(template.render(path, template_values))
            return                         
            
            