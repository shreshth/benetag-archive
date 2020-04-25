from google.appengine.api import users
from google.appengine.ext import db, webapp
from google.appengine.ext.webapp import template
import bene_query
import bene_util
import os
import urllib




"""
View a Location Page
"""
class ViewLocation(webapp.RequestHandler):
    def get(self):
        ID = bene_util.sanitize(self.request.get('id'))
        if not ID:
            '''
            TODO: If no ID sent, default to page with all locations?
            '''
            self.redirect('/')
            return
        location = db.get(ID)
        ''' an error in getting the location will be redirected to exception handler'''
        
        # Make a dictionary for template
        name = location.name
        producer = location.getProducer()
        productlist = location.getProductLines()
        workers = location.getWorkers()
        address = location.address
        if location.location:
            latitude = location.location.lat
            longitude = location.location.lon
        else:
            latitude = None
            longitude = None
        template_values = bene_util.initTemplate(self.request.uri)
        template_values['id'] = ID
        template_values['name'] = name
        template_values['location'] = location
        template_values['producer'] = producer
        template_values['products'] = productlist
        template_values['workers'] = workers
        template_values['latitude'] = latitude
        template_values['longitude'] = longitude
        template_values['url'] = self.request.url
        template_values['address'] = address
        template_values['qr_url'] = self.request.url.replace('view','qr')
        template_values['path'] = "location"
        
        template_values['can_edit'] = False
        user = users.get_current_user()
        if user:
            if location.owner == user and bene_query.getCurrentUser().isProducer:
                template_values['can_edit'] = True
                template_values['edit_link'] = '/editlocation?%s' % urllib.urlencode({'id' : ID})
        
        path = os.path.join(os.path.dirname(__file__), 'apolis_viewlocation.html')
        self.response.out.write(template.render(path, template_values))
        return
    
    '''
    Exception handler
    '''
    def handle_exception(self, exception, debug_mode):
        if debug_mode:
            super(ViewLocation, self).handle_exception(exception, debug_mode)
        else:
            template_values = bene_util.initTemplate(self.request.uri)
            path = os.path.join(os.path.dirname(__file__), 'not_found.html')
            self.response.out.write(template.render(path, template_values))
            return
