from google.appengine.ext import db, webapp
from google.appengine.ext.webapp import template
import bene_util
import os
import urllib




"""
View product path
"""
class ViewPath(webapp.RequestHandler):
    def get(self):
        ID = bene_util.sanitize(self.request.get('id'))
        if not ID:
            ''' 
            TODO: If no ID sent, default to ?
            '''
            self.redirect('/')
            return
        _generic = db.get(ID)
        ''' an error in getting the product will be redirected to exception handler'''
        
        if _generic.isUnit:
            _generic = _generic.getProductConfig()
        
        ''' NOTE THAT THIS WORKS FOR BOTH PRODUCT UNITS AND CONFIGS '''
        
        # Make a dictionary for template
        _productconfig = _generic
        name = _productconfig.getName()
        producer = _productconfig.getProducer()
        template_values = bene_util.initTemplate(self.request.uri)
        template_values['id'] = ID
        template_values['name'] = name
        template_values['producer'] = producer
        template_values['locations'] = _generic.getLocations()
        template_values['numloc'] = len(_generic.getLocations())
        template_values['path'] = "product"
        path = os.path.join(os.path.dirname(__file__), 'viewpath.html')
        self.response.out.write(template.render(path, template_values))
        return
    
    '''
    Exception handler
    '''
    def handle_exception(self, exception, debug_mode):
        if debug_mode:
            super(ViewPath, self).handle_exception(exception, debug_mode)
        else:
            template_values = bene_util.initTemplate(self.request.uri)
            path = os.path.join(os.path.dirname(__file__), 'not_found.html')
            self.response.out.write(template.render(path, template_values))
            return