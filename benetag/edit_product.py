from google.appengine.api import users
from google.appengine.ext import db, webapp
from google.appengine.ext.webapp import template
import bene_query
import bene_util
import entities
import os
import urllib
        

"""
Creates a form for Producers to change a line
"""
class EditLinePage(webapp.RequestHandler):
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
        
        template_values['path'] = "product"
        
        template_values['id'] = ID
        template_values['name_old'] = _productline.name
        template_values['description_old'] = _productline.description
        template_values['num_products'] = _productline.numProducts()
        template_values['cropentity'] = _productline
                            
        path = os.path.join(os.path.dirname(__file__), 'editproduct.html')
        self.response.out.write(template.render(path, template_values))
        return
    
    '''
    Exception handler
    '''
    def handle_exception(self, exception, debug_mode):
        if debug_mode:
            super(EditLinePage, self).handle_exception(exception, debug_mode)
        else:
            template_values = bene_util.initTemplate(self.request.uri)
            path = os.path.join(os.path.dirname(__file__), 'not_found.html')
            self.response.out.write(template.render(path, template_values))
            return
                             
"""
Page that stores config in datastore
"""
class StoreEditedLinePage(webapp.RequestHandler):
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
                
        # edit product line
        _picture = self.request.get('picturedata')
        _name = bene_util.sanitize(self.request.get('name'))
        _description = bene_util.sanitize(self.request.get('description'))
        if _name != _productline.name or _description != _productline.description or _picture:
            _name_save = _productline.name
            _productline.name = _name
            _productline.description = _description
            if bene_util.doesSimilarProductLineExist(_productline) and _name_save != _productline.name: # already exists
                self.redirect('/editproduct?%s' % urllib.urlencode({'repeatedit': True, 'id': ID}))
                return
            _productline.addPicture(_picture)
            _productline.put()   
       
        self.redirect('/view?%s' % urllib.urlencode({'id': ID}))
        return
    
    '''
    Exception handler
    '''
    def handle_exception(self, exception, debug_mode):
        if debug_mode:
            super(StoreEditedLinePage, self).handle_exception(exception, debug_mode)
        else:
            template_values = bene_util.initTemplate(self.request.uri)
            path = os.path.join(os.path.dirname(__file__), 'not_found.html')
            self.response.out.write(template.render(path, template_values))
            return