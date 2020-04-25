from google.appengine.api import users
from google.appengine.ext import db, webapp
from google.appengine.ext.webapp import template
import bene_query
import bene_util
import entities
import os
import urllib
import logging


"""
Creates a form for Producers to enter information 
about a Product Line
"""
class CreateProductPage(webapp.RequestHandler):
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
        
        if not _producer.verified: # if producer is not verified
            self.redirect('/producerhome?%s' % urllib.urlencode({'verify': True}))
            return
        
        template_values = bene_util.initTemplate(self.request.uri)
        _locations = _producer.getLocations()
        template_values['locations'] = _locations
        
        count = 0
        if _locations:
            for location in _locations:
                if location:
                    count += 1
                    if len(location.name) > 10:
                        count += 1
        if not count:
            count = 1
        template_values['pathheight'] = count*40 
        
        if count == 0: template_values['no_locations'] = True
        elif count > 0: template_values['no_locations'] = False
        template_values['workers'] = _producer.getWorkers()
        template_values['badges'] = entities.Badge.all()
        template_values['path'] = "product"
        path = os.path.join(os.path.dirname(__file__), 'createproduct.html')
        self.response.out.write(template.render(path, template_values))
        return
    
    '''
    Exception handler
    '''
    def handle_exception(self, exception, debug_mode):
        if debug_mode:
            super(CreateProductPage, self).handle_exception(exception, debug_mode)
        else:
            template_values = bene_util.initTemplate(self.request.uri)
            path = os.path.join(os.path.dirname(__file__), 'not_found.html')
            self.response.out.write(template.render(path, template_values))
            return
            
      
"""
Page that stores Product line in datastore
"""
class StoreProductPage(webapp.RequestHandler):
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
        
        if not _producer.verified: # if producer is not verified
            self.redirect('/producerhome?%s' % urllib.urlencode({'verify': True}))
            return
        
        _name = bene_util.sanitize(self.request.get('name'))
        _description = bene_util.sanitize(self.request.get('description'))
        _locations = bene_util.sanitize(self.request.get('orderedlocations'))
        _workers = bene_util.sanitizeList(self.request.get_all('workers'))
        _badges = bene_util.sanitizeList(self.request.get_all('badges'))
        _picture = self.request.get('picturedata')
        product_line = entities.ProductLine(name=_name,
                                            owner=user,
                                            description=_description,                                            
                                            isLine=True,
                                            isConfig=False,
                                            isUnit=False)
        if bene_util.doesSimilarProductLineExist(product_line): # already exists
            self.redirect('/createproduct?%s' % urllib.urlencode({'repeat': True}))
            return
        
        product_line.addProducer(_producer)
        product_line.addPicture(_picture)      
        product_line.put()
        
        s_price = bene_util.sanitize(self.request.get('storePrice'))
        s_name = bene_util.sanitize(self.request.get('storeName'))
        s_url = bene_util.sanitize(self.request.get('storeLink'))
        s_link = None
        if s_name and s_url:
            if not s_price:
                s_price = "0.0"
            try:
                s_price = float(s_price)
            except ValueError:
                s_price= 0.0
            s_link = entities.StoreLink(name=s_name,
                                            url=s_url,
                                            price=s_price)
            s_link.put()
        _displayAmazon = False
        if self.request.get('displayAmazon'):
            _displayAmazon = True
        p = entities.ProductConfig(name=_name,
                                 config_name="Default config",
                                 owner=user,
                                 rating=0.0,
                                 _num_ratings=0,
                                 _num_closet=0,
                                 isLine=False,
                                 isConfig=True,
                                 isUnit=False,
                                 store_link=s_link,
                                 displayAmazon=_displayAmazon)
        p.addProducer(_producer)
        p.addProductLine(product_line)
        for _badge in _badges:
            p.addBadge(db.Key(_badge))
                    
        if _locations:
            _locations = _locations.split(",")
            locations = db.get(_locations)
            i = 0
            for location in locations:
                p.addLocationToPath(location, "", i)
                i = i + 1
                    
        p.put()
            
        config_key = p.key() 
        # add product to workers
        if _workers:
            for _worker in _workers:
                if _worker:
                    worker = db.get(_worker)
                    worker.addProductConfig(config_key)
                    worker.put()
                        
        # add product to locations
        if _locations:
            for location in locations:
                location.addProductConfig(config_key)
                location.put()  
                            
        if bene_util.sanitize(self.request.get('more')): # want to add more
            self.redirect('/createproduct?%s' % urllib.urlencode({'added': True}))
            return
        
        # otherwise redirect to product page
        self.redirect('/view?%s' % urllib.urlencode({'id' : product_line.key()}))
                   
            
    '''
    Exception handler
    '''
    def handle_exception(self, exception, debug_mode):
        if debug_mode:
            super(StoreProductPage, self).handle_exception(exception, debug_mode)
        else:
            template_values = bene_util.initTemplate(self.request.uri)
            path = os.path.join(os.path.dirname(__file__), 'not_found.html')
            self.response.out.write(template.render(path, template_values))
            return