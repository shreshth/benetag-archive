from google.appengine.api import users
from google.appengine.ext import db, webapp
from google.appengine.ext.webapp import template
import bene_query
import bene_util
import entities
import os
import urllib


"""
Creates a form for Producers to enter information 
about a Product
"""
class CreateConfigPage(webapp.RequestHandler):
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
                    
        ID = bene_util.sanitize(self.request.get('id'))
        if not ID:
            '''
            TODO: If no ID sent?
            '''
            self.redirect('/')
            return
        _productline = db.get(ID)
        ''' an error in getting the product will be redirected to exception handler'''
        
        if _productline.owner != user: # if current user doesn't own product
            self.redirect('/producerhome?%s' % urllib.urlencode({'not_owner': True}))
            return
        
        template_values = bene_util.initTemplate(self.request.uri)
        template_values['id'] = ID
        template_values['name_old'] = _productline.name
        template_values['description_old'] = _productline.description
        template_values['path'] = "product" 
        template_values['workers'] = _producer.getWorkers()        
        template_values['badges'] = entities.Badge.all()
        template_values['product'] = _productline
        template_values['cropentity'] = _productline
        
        template_values['no_locations'] = True
        _locations = _producer.getLocations()
        if _locations.get(): template_values['no_locations'] = False
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
        
        path = os.path.join(os.path.dirname(__file__), 'createconfig.html')
        self.response.out.write(template.render(path, template_values))
        return
    
    '''
    Exception handler
    '''
    def handle_exception(self, exception, debug_mode):
        if debug_mode:
            super(CreateConfigPage, self).handle_exception(exception, debug_mode)
        else:
            template_values = bene_util.initTemplate(self.request.uri)
            path = os.path.join(os.path.dirname(__file__), 'not_found.html')
            self.response.out.write(template.render(path, template_values))
            return
                             
"""
Page that stores Product in datastore
"""
class StoreConfigPage(webapp.RequestHandler):
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
                    
        ID = bene_util.sanitize(self.request.get('id'))
        if not ID:
            '''
            TODO: If no ID sent?
            '''
            self.redirect('/')
            return
        _productline = db.get(ID)
        ''' an error in getting the product will be redirected to exception handler'''
        
        if _productline.owner != user: # if current user doesn't own product
            self.redirect('/producerhome?%s' % urllib.urlencode({'not_owner': True}))
            return
        
        _configname = bene_util.sanitize(self.request.get('configname'))
        _locations = bene_util.sanitize(self.request.get('orderedlocations'))
        _workers = bene_util.sanitizeList(self.request.get_all('workers'))
        _badges = bene_util.sanitizeList(self.request.get_all('badges'))
        
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
        
        p = entities.ProductConfig(config_name=_configname,
                                   owner=user,
                                   rating=0.0,
                                   _num_ratings=0,
                                   _num_closet=0,
                                   isLine=False,
                                   isConfig=True,
                                   isUnit=False,
                                   store_link=s_link,
                                   displayAmazon=_displayAmazon)
        
        if bene_util.doesSimilarProductConfigExist(p, _productline): # already exists
            self.redirect('/createconfig?%s' % urllib.urlencode({'repeateditname': True, 'id': ID}))
            return
          
        p.addProducer(_producer)
        p.addProductLine(_productline)
        for _badge in _badges:
            p.addBadge(db.Key(_badge))
                    
        if _locations:
            _locations = _locations.split(',')
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
                
        # edit product line
        _name = bene_util.sanitize(self.request.get('name'))
        _description = bene_util.sanitize(self.request.get('description'))
        _picture = self.request.get('picturedata')
        if _name != _productline.name or _description != _productline.description or _picture:
            _name_save = _productline.name
            _productline.name = _name
            _productline.description = _description
            if bene_util.doesSimilarProductLineExist(_productline) and _name_save != _productline.name: # already exists
                self.redirect('/createconfig?%s' % urllib.urlencode({'id': ID, 'repeatprodname': True}))
                return
            
            _productline.addPicture(_picture)
            _productline.put()      
            
        if bene_util.sanitize(self.request.get('more')): # want to add more
            self.redirect('/createconfig?%s' % urllib.urlencode({'id': ID, 'added': True}))
            return 
                            
        self.redirect('/view?%s' % urllib.urlencode({'id': config_key}))
        return
    
    '''
    Exception handler
    '''
    def handle_exception(self, exception, debug_mode):
        if debug_mode:
            super(StoreConfigPage, self).handle_exception(exception, debug_mode)
        else:
            template_values = bene_util.initTemplate(self.request.uri)
            path = os.path.join(os.path.dirname(__file__), 'not_found.html')
            self.response.out.write(template.render(path, template_values))
            return