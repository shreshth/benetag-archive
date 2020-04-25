from google.appengine.api import users
from google.appengine.ext import db, webapp
from google.appengine.ext.webapp import template
import bene_query
import bene_util
import entities
import os
import urllib

"""
Creates a form to send message to consumers of a productline/config
"""
class MyOutbox(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user() 
        if not user: # need to sign in
            self.redirect('/?signin=True')
            return
        
        if bene_query.getCurrentUser().isConsumer: # consumers can't access this
            self.redirect('/')
            return
            
        _producer = bene_query.getCurrentProducer()
        if _producer  == None: # no producer signed up, so ask to sign up
            self.redirect('/')
            return
        
        template_values = bene_util.initTemplate(self.request.uri)
        template_values['producer'] = _producer
        template_values['path'] = "message"
        __msgs = _producer.getSentMsg()
        _msgs = []
        for _msg in __msgs:
            _msgs.append(_msg)
        if _msgs: 
            _msgs.reverse()
        template_values['messages'] = _msgs
        
        path = os.path.join(os.path.dirname(__file__), 'viewoutbox.html')
        self.response.out.write(template.render(path, template_values))
        return
    
    '''
    Exception handler
    '''
    def handle_exception(self, exception, debug_mode):
        if debug_mode:
            super(MyOutbox, self).handle_exception(exception, debug_mode)
        else:
            template_values = bene_util.initTemplate(self.request.uri)
            path = os.path.join(os.path.dirname(__file__), 'not_found.html')
            self.response.out.write(template.render(path, template_values))
            return

                    