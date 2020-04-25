from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
import bene_query
import bene_util
import entities
import os
import urllib

"""
Creates a form to sign up as a Producer
"""
class CreateProducerPage(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user() 
        if not user: # need to sign in
            self.redirect('/?signin=True')
            return
        
        if bene_query.getCurrentUser().isConsumer: # consumers can't access this
            self.redirect('/')
            return
            
        _producer = bene_query.getCurrentProducer()
        if _producer != None: # already has a producer page
            self.redirect('/')
            return
         
        template_values = bene_util.initTemplate(self.request.uri)
        template_values['email_public_old'] = bene_util.getEmail(user)
        path = os.path.join(os.path.dirname(__file__), 'createproducer.html')
        self.response.out.write(template.render(path, template_values))
        return
    
    '''
    Exception handler
    '''
    def handle_exception(self, exception, debug_mode):
        if debug_mode:
            super(CreateProducerPage, self).handle_exception(exception, debug_mode)
        else:
            template_values = bene_util.initTemplate(self.request.uri)
            path = os.path.join(os.path.dirname(__file__), 'not_found.html')
            self.response.out.write(template.render(path, template_values))
            return
                

        
"""
Puts a Producer in the database
"""
class StoreProducerPage(webapp.RequestHandler):
    def post(self):
        user = users.get_current_user() 
        if not user: # need to sign in
            self.redirect('/?signin=True')
            return
        
        if bene_query.getCurrentUser().isConsumer: # consumers can't access this
            self.redirect('/')
            return
            
        _producer = bene_query.getCurrentProducer()
        if _producer != None: # already has a producer page
            self.redirect('/')
            return
        
        _name = bene_util.sanitize(self.request.get('name'))
        _picture = self.request.get('picturedata')
        _description = bene_util.sanitize(self.request.get('description'))
        _email_public = self.request.get('email')
                    
        p = entities.Producer(name = _name, 
                              email=bene_util.getEmail(user), 
                              email_public=_email_public,
                              owner=user,
                              description=_description,
                              verified=False)
        p.addPicture(_picture)
        p.put()
                        
        self.redirect('/producerhome?%s' % urllib.urlencode({'verifyone': True}))
        return
    
    '''
    Exception handler
    '''
    def handle_exception(self, exception, debug_mode):
        if debug_mode:
            super(StoreProducerPage, self).handle_exception(exception, debug_mode)
        else:
            template_values = bene_util.initTemplate(self.request.uri)
            path = os.path.join(os.path.dirname(__file__), 'not_found.html')
            self.response.out.write(template.render(path, template_values))
            return
