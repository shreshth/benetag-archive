from google.appengine.api import users
from google.appengine.ext import db, webapp
from google.appengine.ext.webapp import template
import bene_query
import bene_util
import os
import urllib



"""
Creates a form to create a Worker
"""
class EditWorkerPage(webapp.RequestHandler):
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
            TODO: If no ID sent, default to ?
            '''
            self.redirect('/')
            return
        _worker = db.get(ID)
        ''' an error in getting the worker will be redirected to exception handler'''
        
        if _worker.owner != user: # not 'owner' of worker. I know it sounds very pre-emancipation
            self.redirect('/producerhome?%s' % urllib.urlencode({'not_owner': True}))
            return
        
        template_values = bene_util.initTemplate(self.request.uri)
        template_values['id'] = ID
        template_values['cropentity'] = _worker
        template_values['name_old'] = _worker.name
        template_values['profile_old'] = _worker.profile
        template_values['unique_old'] = _worker.unique
        template_values['path'] = "worker"
                        
        template_values['no_locations'] = True
        _locations_old = [_worker.getLocation()]
        if _worker.getLocation():
            template_values['no_locations'] = False
            template_values['locations_old'] = _locations_old
        '''
        TODO: Make this more efficient. For some reason, 'location not in _locations_old' doesn't work
        '''
        _locations = _producer.getLocations()
        if len(_locations.fetch(1)) != 0:
            template_values['locations'] = []
            if _locations:
                for location in _locations:
                    if location:
                        add = True
                        if _locations_old:
                            for location_old in _locations_old:
                                if location_old:
                                    if location_old.key() == location.key():
                                        add = False
                        if add:
                            template_values['no_locations'] = False
                            template_values['locations'].append(location)
            
                                            
        path = os.path.join(os.path.dirname(__file__), 'editworker.html')
        self.response.out.write(template.render(path, template_values))
        return
    
    '''
    Exception handler
    '''
    def handle_exception(self, exception, debug_mode):
        if debug_mode:
            super(EditWorkerPage, self).handle_exception(exception, debug_mode)
        else:
            template_values = bene_util.initTemplate(self.request.uri)
            path = os.path.join(os.path.dirname(__file__), 'not_found.html')
            self.response.out.write(template.render(path, template_values))
            return
                   
                   
"""
Puts a worker in the database
"""
class StoreEditedWorkerPage(webapp.RequestHandler):
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
            TODO: If no ID sent, default to ?
            '''
            self.redirect('/')
            return
        _worker = db.get(ID)
        ''' an error in getting the worker will be redirected to exception handler'''
        
        if _worker.owner != user: # not 'owner' of worker. I know it sounds very pre-emancipation
            self.redirect('/producerhome?%s' % urllib.urlencode({'not_owner': True}))
            return
                            
        _worker.name = bene_util.sanitize(self.request.get('name'))
        _worker.profile = bene_util.sanitize(self.request.get('profile'))
        _unique_save = _worker.unique
        _worker.unique = bene_util.sanitize(self.request.get('unique'))
        if bene_util.doesExactWorkerExist(_worker) and _unique_save != _worker.unique: # if worker already exists
            self.redirect('/editworker?%s' % (urllib.urlencode({'id' : ID, 'repeateditid' : True})))
            return
        if not _worker.unique:
            if bene_util.doesSimilarWorkerExist(_worker, key=True): # if worker already exists
                self.redirect('/editworker?%s' % (urllib.urlencode({'id' : ID, 'repeateditname' : True})))
                return

        _location = bene_util.sanitize(self.request.get('location'))
        if _location:
            _worker.addLocation(db.get(_location))
        else:
            _worker.clearLocation()
                        
        _picture = self.request.get('picturedata')
        _worker.addPicture(_picture)
                
        _worker.put()
        self.redirect('/viewworker?%s' % urllib.urlencode({'id': ID}))
        return
    
    '''
    Exception handler
    '''
    def handle_exception(self, exception, debug_mode):
        if debug_mode:
            super(StoreEditedWorkerPage, self).handle_exception(exception, debug_mode)
        else:
            template_values = bene_util.initTemplate(self.request.uri)
            path = os.path.join(os.path.dirname(__file__), 'not_found.html')
            self.response.out.write(template.render(path, template_values))
            return  
        
        