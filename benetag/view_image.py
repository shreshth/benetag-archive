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

class ProductImage(webapp.RequestHandler):
    def get(self):
        # Get the id from the get parameter
        ID = bene_util.sanitize(self.request.get('id'))
        if not ID:
            '''
            TODO: what to do here?
            '''
            return
        # Fetch the image for this product
        product = db.get(ID)
        ''' an error in getting the product image will be redirected to exception handler'''
        
        if product.hasImage():
            self.response.headers['Content-Type'] = 'image'
            self.response.out.write(product.getPicture())
            return
        else:
            self.redirect('/img/defaultproduct.jpg')
            return
    
    '''
    Exception handler
    '''
    def handle_exception(self, exception, debug_mode):
        if debug_mode:
            super(ProductImage, self).handle_exception(exception, debug_mode)
        else:
            template_values = bene_util.initTemplate(self.request.uri)
            path = os.path.join(os.path.dirname(__file__), 'not_found.html')
            self.response.out.write(template.render(path, template_values))
            return

class BadgeImage(webapp.RequestHandler):
    def get(self):
        key = bene_util.sanitize(self.request.get('key'))
        if not key:
            '''
            TODO: what to do here?
            '''
            return
        badge = db.get(key)
        ''' an error in getting the badge image will be redirected to exception handler'''
        
        if badge.hasImage():
            self.response.headers['Content-Type'] = 'image'
            self.response.out.write(badge.getPicture())
            return
        else:
            self.redirect('/img/defaultbadge.jpg')
            return
    
    '''
    Exception handler
    '''
    def handle_exception(self, exception, debug_mode):
        if debug_mode:
            super(BadgeImage, self).handle_exception(exception, debug_mode)
        else:
            template_values = bene_util.initTemplate(self.request.uri)
            path = os.path.join(os.path.dirname(__file__), 'not_found.html')
            self.response.out.write(template.render(path, template_values))
            return


class WorkerImage(webapp.RequestHandler):
    def get(self):
        # Get the id from the get parameter
        ID = bene_util.sanitize(self.request.get('id')) 
        if not ID:
            '''
            TODO: what to do here?
            '''
            return
        # Fetch the image for this worker
        worker = db.get(ID)
        ''' an error in getting the worker will be redirected to exception handler'''
        
        if worker.hasImage():
            self.response.headers['Content-Type'] = 'image'
            self.response.out.write(worker.getPicture())
            return
        else:
            self.redirect('/img/defaultworker.jpg')
            return
        
    
    '''
    Exception handler
    '''
    def handle_exception(self, exception, debug_mode):
        if debug_mode:
            super(WorkerImage, self).handle_exception(exception, debug_mode)
        else:
            template_values = bene_util.initTemplate(self.request.uri)
            path = os.path.join(os.path.dirname(__file__), 'not_found.html')
            self.response.out.write(template.render(path, template_values))
            return
        
class LocationImage(webapp.RequestHandler):
    def get(self):
        # Get the id from the get parameter
        ID = bene_util.sanitize(self.request.get('id')) 
        if not ID:
            '''
            TODO: what to do here?
            '''
            return
        # Fetch the image for this worker
        location = db.get(ID)
        ''' an error in getting the worker will be redirected to exception handler'''
        
        if location.hasImage():
            self.response.headers['Content-Type'] = 'image'
            self.response.out.write(location.getPicture())
            return
        else:
            self.redirect('/img/defaultlocation.jpg')
            return        
    
    '''
    Exception handler
    '''
    def handle_exception(self, exception, debug_mode):
        if debug_mode:
            super(LocationImage, self).handle_exception(exception, debug_mode)
        else:
            template_values = bene_util.initTemplate(self.request.uri)
            path = os.path.join(os.path.dirname(__file__), 'not_found.html')
            self.response.out.write(template.render(path, template_values))
            return
        
class ProducerImage(webapp.RequestHandler):
    def get(self):
        # Get the id from the get parameter
        ID = bene_util.sanitize(self.request.get('id')) 
        if not ID:
            '''
            TODO: what to do here?
            '''
            return
        # Fetch the image for this worker
        producer = db.get(ID)
        ''' an error in getting the worker will be redirected to exception handler'''
        
        if producer.hasImage():
            self.response.headers['Content-Type'] = 'image'
            self.response.out.write(producer.getPicture())
            return
        else:
            self.redirect('/img/defaultproducer.jpg')
            return        
    
    '''
    Exception handler
    '''
    def handle_exception(self, exception, debug_mode):
        if debug_mode:
            super(ProducerImage, self).handle_exception(exception, debug_mode)
        else:
            template_values = bene_util.initTemplate(self.request.uri)
            path = os.path.join(os.path.dirname(__file__), 'not_found.html')
            self.response.out.write(template.render(path, template_values))
            return
        
class ConsumerImage(webapp.RequestHandler):
    def get(self):
        # Get the id from the get parameter
        ID = bene_util.sanitize(self.request.get('id')) 
        if not ID:
            '''
            TODO: what to do here?
            '''
            return
        # Fetch the image for this worker
        consumer = db.get(ID)
        ''' an error in getting the worker will be redirected to exception handler'''
        
        if consumer.hasImage():
            self.response.headers['Content-Type'] = 'image'
            self.response.out.write(consumer.getPicture())
            return
        else:
            self.redirect('/img/defaultconsumer.jpg')
            return        
    
    '''
    Exception handler
    '''
    def handle_exception(self, exception, debug_mode):
        if debug_mode:
            super(ConsumerImage, self).handle_exception(exception, debug_mode)
        else:
            template_values = bene_util.initTemplate(self.request.uri)
            path = os.path.join(os.path.dirname(__file__), 'not_found.html')
            self.response.out.write(template.render(path, template_values))
            return