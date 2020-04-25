from google.appengine.api import users
from google.appengine.ext import db, webapp
from google.appengine.ext.webapp import template
import bene_query
import bene_util
import os
import urllib

"""
Creates a form for Producers to enter information
about a Location
"""
class EditLocationPage(webapp.RequestHandler):
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
            TODO: If no ID sent, default to page with all locations?
            '''
            self.redirect('/')
            return
        _location = db.get(ID)
        ''' an error in getting the location will be redirected to exception handler'''
        
        if _location.owner != user: # if not owner of location
            self.redirect('/producerhome?%s' % urllib.urlencode({'not_owner': True}))
            return
        
        template_values = bene_util.initTemplate(self.request.uri)
        template_values['id'] = ID
        template_values['name_old'] = _location.name
        template_values['address_old'] = _location.address
        template_values['unique_old'] = _location.unique
        template_values['description_old'] = _location.description
        template_values['path'] = "location"
        template_values['cropentity'] = _location
        
        path = os.path.join(os.path.dirname(__file__), 'editlocation.html')
        self.response.out.write(template.render(path, template_values))
        return
    
    '''
    Exception handler
    '''
    def handle_exception(self, exception, debug_mode):
        if debug_mode:
            super(EditLocationPage, self).handle_exception(exception, debug_mode)
        else:
            template_values = bene_util.initTemplate(self.request.uri)
            path = os.path.join(os.path.dirname(__file__), 'not_found.html')
            self.response.out.write(template.render(path, template_values))
            return
                        


"""
Page that stores Location in datastore
"""
class StoreEditedLocationPage(webapp.RequestHandler):
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
            TODO: If no ID sent, default to page with all locations?
            '''
            self.redirect('/')
            return
        _location = db.get(ID)
        ''' an error in getting the location will be redirected to exception handler'''
        
        if _location.owner != user: # if not owner of location
            self.redirect('/producerhome?%s' % urllib.urlencode({'not_owner': True}))
            return
        
        _location.name = bene_util.sanitize(self.request.get('name'))
        _location.address = bene_util.sanitize(self.request.get('address'))
        _location.description = bene_util.sanitize(self.request.get('description'))
        _unique_save = _location.unique
        _location.unique = bene_util.sanitize(self.request.get('unique'))
        if bene_util.doesExactLocationExist(_location) and _unique_save != _location.unique : # if location with same unique exists
            self.redirect('/editlocation?%s' % (urllib.urlencode({'id' : ID, 'repeateditid' : True})))
            return 
        if not _location.unique:
            if bene_util.doesSimilarLocationExist(_location, key=True):
                self.redirect('/editlocation?%s' % (urllib.urlencode({'id' : ID, 'repeateditname' : True})))
                return
                  
        _picture = self.request.get('picturedata')
        _location.addPicture(_picture)
                                                                      
        location = bene_util.sanitize(self.request.get('location'))             
        fields = location.split(',')
        if len(fields) == 2:
            try:
                lat = float(fields[0])
                lon = float(fields[1])
                gp = db.GeoPt(lat, lon)
            except ValueError:
                gp = None
        else:
            gp = None
        _location.location = gp
                    
        _location.put()
        self.redirect('/viewlocation?%s' % urllib.urlencode({'id': ID}))
        return
    
    '''
    Exception handler
    '''
    def handle_exception(self, exception, debug_mode):
        if debug_mode:
            super(StoreEditedLocationPage, self).handle_exception(exception, debug_mode)
        else:
            template_values = bene_util.initTemplate(self.request.uri)
            path = os.path.join(os.path.dirname(__file__), 'not_found.html')
            self.response.out.write(template.render(path, template_values))
            return
        