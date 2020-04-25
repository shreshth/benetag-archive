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
about product units
"""
class CreateUnitsPage(webapp.RequestHandler):
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
        _productconfig = db.get(ID)
        ''' an error in getting the product will be redirected to exception handler'''
        
        if _productconfig.owner != user: # if current user doesn't own product
            self.redirect('/producerhome?%s' % urllib.urlencode({'not_owner': True}))
            return
                        
        _locations_old = _productconfig.getLocations()
        _workers_old = _productconfig.getWorkers()
        _badges_old = _productconfig.getBadges()
        template_values = bene_util.initTemplate(self.request.uri)
        template_values['id'] = ID
        template_values['productline_id'] = _productconfig.getProductLine().key()
        template_values['config'] = _productconfig
        template_values['locations'] = _productconfig.getLocations()
        template_values['workers'] = _productconfig.getWorkers()
        template_values['badges'] = _productconfig.getBadges()
        template_values['name'] = _productconfig.getName()
        template_values['configname'] = _productconfig.config_name
        template_values['description'] = _productconfig.getDescription()
        template_values['path'] = "product"
       
        path = os.path.join(os.path.dirname(__file__), 'createunits.html')
        self.response.out.write(template.render(path, template_values))
        return
    
    '''
    Exception handler
    '''
    def handle_exception(self, exception, debug_mode):
        if debug_mode:
            super(CreateUnitsPage, self).handle_exception(exception, debug_mode)
        else:
            template_values = bene_util.initTemplate(self.request.uri)
            path = os.path.join(os.path.dirname(__file__), 'not_found.html')
            self.response.out.write(template.render(path, template_values))
            return
                             
"""
Page that stores Product in datastore
"""
class StoreUnitsPage(webapp.RequestHandler):
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
        _productconfig = db.get(ID)
        ''' an error in getting the product will be redirected to exception handler'''
        
        if _productconfig.owner != user: # if current user doesn't own product
            self.redirect('/producerhome?%s' % urllib.urlencode({'not_owner': True}))
            return
        
        _num_products = bene_util.sanitize(self.request.get('num_products'))
        if not _num_products:
            self.redirect('/')
        
        _productkeys = []
        for i in range(0, int(_num_products)):
            p = entities.Product(owner=user,
                                 isLine=False,
                                 isConfig=False,
                                 isUnit=True) 
            p.addProducer(_producer)
            p.addProductConfig(_productconfig)
            p.addProductLine(_productconfig.getProductLine())
            
            p.put()
                          
            _productkeys.append(p.key())  
        
        template_values = bene_util.initTemplate(self.request.uri)
        template_values['id'] = ID
        template_values['productkeys'] = _productkeys
       
        path = os.path.join(os.path.dirname(__file__), 'viewunitsqr.html')
        self.response.out.write(template.render(path, template_values))
        return           
    
    '''
    Exception handler
    '''
    def handle_exception(self, exception, debug_mode):
        if debug_mode:
            super(StoreUnitsPage, self).handle_exception(exception, debug_mode)
        else:
            template_values = bene_util.initTemplate(self.request.uri)
            path = os.path.join(os.path.dirname(__file__), 'not_found.html')
            self.response.out.write(template.render(path, template_values))
            return