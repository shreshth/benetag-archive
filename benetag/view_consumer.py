from google.appengine.api import users
from google.appengine.ext import db, webapp
from google.appengine.ext.webapp import template
import bene_query
import bene_util
import os


"""
View a Consumer Page
"""
class ViewConsumer(webapp.RequestHandler):
    def get(self):
        ID = bene_util.sanitize(self.request.get('id'))
        if not ID:
            '''
            TODO: if no id is sent, defaults to a page with all producers? 
            '''
            self.redirect('/')
            return
        consumer = db.get(ID)
        ''' an error in getting the consumer will be redirected to exception handler'''
        
        # Make a dictionary for template
        name = consumer.name
        profile = consumer.profile
        email_public = consumer.email_public
        
        template_values = bene_util.initTemplate(self.request.uri)
        template_values['id'] = ID
        template_values['consumer'] = consumer
        _products = consumer.getProducts()
        if _products:
            template_values['products'] = _products[0:4] 
        template_values['name'] = name
        template_values['profile'] = profile
        template_values['email_public'] = email_public
        template_values['path'] = self.request.path
        
        template_values['can_edit'] = False
        user = users.get_current_user()
        if user:
            if consumer.owner == user:
                template_values['can_edit'] = True           
                template_values['edit_link'] = '/editconsumer'
        
        path = os.path.join(os.path.dirname(__file__), 'viewconsumer.html')
        self.response.out.write(template.render(path, template_values))
        return
    