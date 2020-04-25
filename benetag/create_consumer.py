from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
import bene_query
import bene_util
import entities
import os
import urllib

"""
Creates a form to sign up as a Consumer
"""
class CreateConsumerPage(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if not user: # need to sign in
            self.redirect('/?signin=True')
            return
        if bene_query.getCurrentUser().isProducer: # producers can't do this
            self.redirect('/')
            return
        
        if bene_query.getCurrentConsumer() != None: # has consumer page 
            self.redirect('/')
            return
            
        template_values = bene_util.initTemplate(self.request.uri)
        template_values['email_public_old'] = bene_util.getEmail(user)
        path = os.path.join(os.path.dirname(__file__), 'createconsumer.html')
        self.response.out.write(template.render(path, template_values))
        return
    
    '''
    Exception handler
    '''
    def handle_exception(self, exception, debug_mode):
        if debug_mode:
            super(CreateConsumerPage, self).handle_exception(exception, debug_mode)
        else:
            template_values = bene_util.initTemplate(self.request.uri)
            path = os.path.join(os.path.dirname(__file__), 'not_found.html')
            self.response.out.write(template.render(path, template_values))
            return
            

"""
Puts a Producer in the database
"""
class StoreConsumerPage(webapp.RequestHandler):
    def post(self):
        user = users.get_current_user()
        if not user: # need to sign in
            self.redirect('/?signin=True')
            return
        if bene_query.getCurrentUser().isProducer: # producers can't do this
            self.redirect('/')
            return
        
        if bene_query.getCurrentConsumer() != None: # already exists
            self.redirect('/')
            return
            
        # no consumer, so add to store
        _name = bene_util.sanitize(self.request.get('name'))
        _picture = bene_util.sanitize(self.request.get('picturedata'))
        _profile = self.request.get('profile')
        _email_public = self.request.get('email')
                
        c = entities.Consumer(name=_name, 
                              has_unread=0,
                              email=bene_util.getEmail(user), 
                              email_public=_email_public,
                              owner=user,
                              profile=_profile,                      
                              verified=False)
        c.addPicture(_picture)
        c.put()
                        
        self.redirect('/consumerhome?%s' % urllib.urlencode({'firsttime': True}))
        return

    '''
    Exception handler
    '''
    def handle_exception(self, exception, debug_mode):
        if debug_mode:
            super(StoreConsumerPage, self).handle_exception(exception, debug_mode)
        else:
            template_values = bene_util.initTemplate(self.request.uri)
            path = os.path.join(os.path.dirname(__file__), 'not_found.html')
            self.response.out.write(template.render(path, template_values))
            return
