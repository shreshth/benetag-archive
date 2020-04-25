from google.appengine.api import users
from google.appengine.ext import db, webapp
from google.appengine.ext.webapp import template
from random import randint
import bene_query
import bene_util
import json
import os
import sys
import urllib


"""
    View mobile page for the product
"""

class ViewProduct(webapp.RequestHandler):
    def get(self):
        # Get the id from the get parameter
        ID = bene_util.sanitize(self.request.get('id'))
        if not ID:
            '''
            TODO: If no ID sent, default to page with all products?
            '''
            self.redirect('/')
            return
        # Fetch the data for this product
        product = db.get(ID)
        ''' an error in getting the product will be redirected to exception handler'''
                
        # Make a dictionary for template
        template_values = bene_util.initTemplate(self.request.uri)
        # generic
        template_values['id'] = ID
        template_values['name'] = product.name
        template_values['product'] = product
        template_values['producer'] = product.getProducer()
        template_values['rating'] = product.getRating()
        # urls
        template_values['url'] = self.request.url
        template_values['path'] = "product"
        template_values['qr_url'] = self.request.url.replace('viewproduct','qr')
        template_values['image_url'] = self.request.url.replace('viewproduct', 'productimage')
        template_values['comment_url'] = '%s/viewproduct?%s' % (self.request.host_url, urllib.urlencode({'id': ID}))
        # interactions - producer
        template_values['can_edit'] = False
        user = users.get_current_user()
        if user:
            if product.owner == user and bene_query.getCurrentUser().isProducer:
                template_values['can_edit'] = True
                template_values['edit_link'] = '/editproduct?%s' % urllib.urlencode({'id': ID})
                template_values['show_qr'] = True
        # interactions - consumer
        template_values['in_closet'] = False
        template_values['add_closet'] = False
        if user:
            if bene_query.getCurrentUser().isConsumer:
                consumer = bene_query.getCurrentConsumer()
                if consumer:
                    if consumer.hasProduct(product.key()):
                        template_values['in_closet'] = True
                        template_values['rem_closet_link'] = '/removefromcloset?%s' % urllib.urlencode({'id': ID})
                    else:
                        template_values['add_closet'] = True
                        template_values['add_closet_link'] = '/addtocloset?%s' % urllib.urlencode({'id': ID})
                        
        template_values['num_configs'] = product.numConfigs()
        template_values['configs'] = product.getConfigs()
        
        template_values['num_products'] = product.numProducts()
        template_values['closet_count'] = product.getClosetCount()
        path = os.path.join(os.path.dirname(__file__), 'viewproduct.html')
        self.response.out.write(template.render(path, template_values).decode('utf-8'))
        return
    
    '''
    Exception handler
    '''
    def handle_exception(self, exception, debug_mode):
        if debug_mode:
            super(ViewProduct, self).handle_exception(exception, debug_mode)
        else:
            template_values = bene_util.initTemplate(self.request.uri)
            path = os.path.join(os.path.dirname(__file__), 'not_found.html')
            self.response.out.write(template.render(path, template_values))
            return