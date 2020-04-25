from google.appengine.api import users
from google.appengine.ext import db, webapp
from google.appengine.ext.webapp import template
import bene_query
import bene_util
import os



"""
View a Producer Page
"""
class ViewProducer(webapp.RequestHandler):
    def get(self):
        ID = bene_util.sanitize(self.request.get('id'))
        if not ID:
            '''
            TODO: if no id is sent, defaults to a page with all producers? 
            '''
            self.redirect('/')
            return
        _producer = db.get(ID)
        ''' an error in getting the producer will be redirected to exception handler'''
        
        # Make a dictionary for template
        name = _producer.name
        description = _producer.description
        product_lines = _producer.getProductLines()[0:4]
        workers = _producer.getWorkers()[0:4]
        locations = _producer.getLocations()[0:4]
        email_public = _producer.email_public
        
        template_values = bene_util.initTemplate(self.request.uri)
        template_values['id'] = _producer.key()
        template_values['name'] = name
        template_values['email_public'] = email_public
        template_values['description'] = description
        template_values['locations'] = locations
        template_values['product_lines'] = product_lines
        template_values['producer'] = _producer
        template_values['workers'] = workers
        template_values['url'] = self.request.url
        template_values['path'] = self.request.path  

        
        template_values['can_edit'] = False
        user = users.get_current_user()
        if user:
            if _producer.owner == user and bene_query.getCurrentUser().isProducer:
                template_values['can_edit'] = True
                template_values['edit_link'] = '/editproducer'           
    
        path = os.path.join(os.path.dirname(__file__), 'viewproducer.html')
        self.response.out.write(template.render(path, template_values))
        return
    
    '''
    Exception handler
    '''
    def handle_exception(self, exception, debug_mode):
        if debug_mode:
            super(ViewProducer, self).handle_exception(exception, debug_mode)
        else:
            template_values = bene_util.initTemplate(self.request.uri)
            path = os.path.join(os.path.dirname(__file__), 'not_found.html')
            self.response.out.write(template.render(path, template_values))
            return