from google.appengine.api import users
from google.appengine.ext import db, webapp
from google.appengine.ext.webapp import template
import bene_query
import bene_util
import os
import urllib
#import Image



"""
View a Worker Page
"""
class ViewWorker(webapp.RequestHandler):
    def get(self):
        ID = bene_util.sanitize(self.request.get('id'))
        if not ID:
            '''
            TODO: if no id is sent, defaults to a page with all workers? 
            '''
            self.redirect('/')
        worker = db.get(ID)
        ''' an error in getting the worker will be redirected to exception handler'''
        
        # Make a dictionary for template
        name = worker.name
        location = worker.getLocation()
        profile = worker.profile
        picture = worker.getPicture()
        producer = worker.getProducer()
        products = worker.getProductLines()
        if location:
            if location.location:
                latitude = location.location.lat
                longitude = location.location.lon
            else:
                latitude = None
                longitude = None
        else:
            latitude = None
            longitude = None
        template_values = bene_util.initTemplate(self.request.uri)
        template_values['id'] = worker.key()
        template_values['worker'] = worker
        template_values['name'] = name
        template_values['picture'] = picture
        template_values['profile'] = profile
        template_values['location'] = location
        template_values['producer'] = producer 
        template_values['products'] = products 
        template_values['latitude'] = latitude
        template_values['longitude'] = longitude
        template_values['url'] = self.request.url 
        template_values['path'] = "worker"
    
        template_values['can_edit'] = False
        user = users.get_current_user()
        if user:
            if worker.owner == user and bene_query.getCurrentUser().isProducer:
                template_values['can_edit'] = True
                template_values['edit_link'] = '/editworker?%s' % urllib.urlencode({'id': ID})
    
        path = os.path.join(os.path.dirname(__file__), 'viewworker.html')
        self.response.out.write(template.render(path, template_values))
        return
    
    '''
    Exception handler
    '''
    def handle_exception(self, exception, debug_mode):
        if debug_mode:
            super(ViewWorker, self).handle_exception(exception, debug_mode)
        else:
            template_values = bene_util.initTemplate(self.request.uri)
            path = os.path.join(os.path.dirname(__file__), 'not_found.html')
            self.response.out.write(template.render(path, template_values))
            return
        