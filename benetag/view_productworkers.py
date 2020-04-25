from google.appengine.ext import db, webapp
from google.appengine.ext.webapp import template
import bene_util
import os




"""
View workers who worked on a product
"""
class ViewProductWorkers(webapp.RequestHandler):
    def get(self):
        ID = bene_util.sanitize(self.request.get('id'))
        if not ID:
            ''' 
            TODO: If no ID sent, default to page with all products?
            '''
            self.redirect('/')
            return
        _product = db.get(ID)
        ''' an error in getting the product will be redirected to exception handler'''
        
        if _product.isUnit:
            _product = _product.getProductConfig()
        
        
        # Make a dictionary for template
        _productconfig = _product
        name = _product.name
        producer = _productconfig.getProducer()
        workers = _productconfig.getWorkers()
        template_values = bene_util.initTemplate(self.request.uri)
        template_values['id'] = ID
        template_values['productconfig'] = _productconfig
        template_values['name'] = name
        template_values['producer'] = producer
        template_values['workers'] = workers
        template_values['url'] = self.request.url
        template_values['qr_url'] = self.request.url.replace('view','qr')
        path = os.path.join(os.path.dirname(__file__), 'viewproductworkers.html')
        self.response.out.write(template.render(path, template_values))
        return
    
    '''
    Exception handler
    '''
    def handle_exception(self, exception, debug_mode):
        if debug_mode:
            super(ViewProductWorkers, self).handle_exception(exception, debug_mode)
        else:
            template_values = bene_util.initTemplate(self.request.uri)
            path = os.path.join(os.path.dirname(__file__), 'not_found.html')
            self.response.out.write(template.render(path, template_values))
            return