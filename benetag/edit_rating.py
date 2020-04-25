from google.appengine.api import users
from google.appengine.ext import db, webapp
from google.appengine.ext.webapp import template
import bene_query
import bene_util
import os


class ChangeRating(webapp.RequestHandler):
    def post(self):
        user = users.get_current_user() 
        if not user: # need to sign in
            self.redirect('/?signin=True')
            return
        
        if bene_query.getCurrentUser().isProducer: # producers can't access this
            self.redirect('/')
            return
        
        _consumer = bene_query.getCurrentConsumer()
        if _consumer  == None: # no consumer signed up, so ask to sign up
            self.redirect('/')
            return
    
        productConfigKey = bene_util.sanitize(self.request.get('productConfigKey'))
        _productconfig = db.get(productConfigKey)
        _productconfig.updateRating(float(bene_util.sanitize(self.request.get('adv1'))), _consumer)
        _productconfig.put()
        
        '''
        Exception handler
        '''
    def handle_exception(self, exception, debug_mode):
        if debug_mode:
            super(ChangeRating, self).handle_exception(exception, debug_mode)
        else:
            template_values = bene_util.initTemplate(self.request.uri)
            path = os.path.join(os.path.dirname(__file__), 'not_found.html')
            self.response.out.write(template.render(path, template_values))
            return