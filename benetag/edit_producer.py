from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
import bene_query
import bene_util
import os
import urllib



"""
Creates a form to sign up as a Producer
"""
class EditProducerPage(webapp.RequestHandler):
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
        template_values['id'] = _producer.key()
        template_values['name_old'] = _producer.name
        template_values['description_old'] = _producer.description
        template_values['email_public_old'] = _producer.email_public
        template_values['cropentity'] = _producer
        path = os.path.join(os.path.dirname(__file__), 'editproducer.html')
        self.response.out.write(template.render(path, template_values))
        return
    
    '''
    Exception handler
    '''
    def handle_exception(self, exception, debug_mode):
        if debug_mode:
            super(EditProducerPage, self).handle_exception(exception, debug_mode)
        else:
            template_values = bene_util.initTemplate(self.request.uri)
            path = os.path.join(os.path.dirname(__file__), 'not_found.html')
            self.response.out.write(template.render(path, template_values))
            return
        

"""
Puts a Producer in the database
"""
class StoreEditedProducerPage(webapp.RequestHandler):
    def post(self):
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
        
        _name = bene_util.sanitize(self.request.get('name'))
        _description = bene_util.sanitize(self.request.get('description'))
        _picture = self.request.get('picturedata')
        _email_public = self.request.get('email')
            
                              
        _producer.name = _name
        _producer.description = _description
        _producer.email_public = _email_public
        _producer.addPicture(_picture)
        _producer.put()
                        
        self.redirect('/myprofile')
        return
    
    '''
    Exception handler
    '''
    def handle_exception(self, exception, debug_mode):
        if debug_mode:
            super(StoreEditedProducerPage, self).handle_exception(exception, debug_mode)
        else:
            template_values = bene_util.initTemplate(self.request.uri)
            path = os.path.join(os.path.dirname(__file__), 'not_found.html')
            self.response.out.write(template.render(path, template_values))
            return