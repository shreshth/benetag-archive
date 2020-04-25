from google.appengine.api import users
from google.appengine.ext import db, webapp
from google.appengine.ext.webapp import template
import bene_query
import bene_util
import entities
import os
import urllib
        

"""
Delete a config cleanly
"""
class DeleteConfigPage(webapp.RequestHandler):
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
                        
        # remove from locations
        _locations = _productconfig.getLocations()
        if _locations:
            for _location in _locations:
                if _location:
                    _location.remProductConfig(ID)
                    _location.put()
                    
        # clear out path elements
        _productconfig.clearPath()
        
        # remove from workers
        _workers = _productconfig.getWorkers()
        if _workers:
            for _worker in _workers:
                if _worker:
                    _worker.remProductConfig(ID)
                    _worker.put()

        # delete units
        _units = _productconfig.getProducts()
        if _units:
            for _unit in _units:
                if _unit:
                    db.delete(_unit.key())
            
        # delete messages
        for _msg in _producer.getSentMsg():
            if _msg:
                if _msg.receiver.key() == _productconfig.key():
                    db.delete(_msg.key())
            
        # if product line is now empty, then delete it
        _productline = _productconfig.getProductLine()
        if _productline.numConfigs() == 1:
            db.delete(_productline.key())       
            # delete messages
            for _msg in _producer.getSentMsg():
                if _msg:
                    if _msg.receiver.key() == _productline.key():
                        db.delete(_msg.key())     
            
        # delete from datastore
        db.delete(_productconfig.key())
        
        self.redirect('/myproducts')
        return
    
    
    '''
    Exception handler
    '''
    def handle_exception(self, exception, debug_mode):
        if debug_mode:
            super(DeleteConfigPage, self).handle_exception(exception, debug_mode)
        else:
            template_values = bene_util.initTemplate(self.request.uri)
            path = os.path.join(os.path.dirname(__file__), 'not_found.html')
            self.response.out.write(template.render(path, template_values))
            return