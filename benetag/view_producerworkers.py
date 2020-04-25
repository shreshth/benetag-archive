from google.appengine.api import users
from google.appengine.ext import db, webapp
from google.appengine.ext.webapp import template
import bene_query
import bene_util

import os


"""
View all Workers for a Producer
"""
class ViewProducerWorkers(webapp.RequestHandler):
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
        producer = db.get(ID)
        ''' an error in getting the producer will be redirected to exception handler'''
        
        # Make a dictionary for template
        template_values = bene_util.initTemplate(self.request.uri)
        template_values['id'] = producer.key()
        template_values['producer'] = producer
        
        workers = producer.getWorkers()
        template_values['workers'] = workers
        num_workers = 0
        if workers:
            for worker in workers:
                if worker:
                    num_workers += 1
        if num_workers == 0:
            template_values['no_workers'] = True
        else:
            template_values['no_workers'] = False
        
        locations = producer.getLocations()
        template_values['locations'] = locations
        num_workers_with_loc = 0
        if locations:
            for location in locations:
                if location:
                    _workers = location.getWorkers()
                    if _workers:
                        for worker in _workers:
                            if worker:
                                num_workers_with_loc += 1
        template_values['num_worker_no_location'] = num_workers - num_workers_with_loc       
        
        template_values['can_edit_local'] = False
        user = users.get_current_user()
        if user:
            if producer.owner == user:
                template_values['can_edit_local'] = True
            
        path = os.path.join(os.path.dirname(__file__), 'viewproducerworkers.html')
        self.response.out.write(template.render(path, template_values))
        return
    
    '''
    Exception handler
    '''
    def handle_exception(self, exception, debug_mode):
        if debug_mode:
            super(ViewProducerWorkers, self).handle_exception(exception, debug_mode)
        else:
            template_values = bene_util.initTemplate(self.request.uri)
            path = os.path.join(os.path.dirname(__file__), 'not_found.html')
            self.response.out.write(template.render(path, template_values))
            return
        
        
"""
View all Workers for a Producer
"""
class ViewMyWorkers(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user() 
        if not user: # need to sign in
            self.redirect('/?signin=True')
            return
        
        if bene_query.getCurrentUser().isConsumer: # consumers can't access this
            self.redirect('/')
            return
            
        producer = bene_query.getCurrentProducer()
        if producer  == None: # no producer signed up, so ask to sign up
            self.redirect('/')
            return
        
        # Make a dictionary for template
        template_values = bene_util.initTemplate(self.request.uri)
        template_values['id'] = producer.key()
        template_values['producer'] = producer
        
        workers = producer.getWorkers()
        template_values['workers'] = workers
        num_workers = 0
        if workers:
            for worker in workers:
                if worker:
                    num_workers += 1
        if num_workers == 0:
            template_values['no_workers'] = True
        else:
            template_values['no_workers'] = False
        
        locations = producer.getLocations()
        template_values['locations'] = locations
        num_workers_with_loc = 0
        if locations:
            for location in locations:
                if location:
                    _workers = location.getWorkers()
                    if _workers:
                        for worker in _workers:
                            if worker:
                                num_workers_with_loc += 1
        template_values['num_worker_no_location'] = num_workers - num_workers_with_loc       
        
        template_values['can_edit_local'] = False
        user = users.get_current_user()
        if user:
            if producer.owner == user:
                template_values['can_edit_local'] = True
            
        path = os.path.join(os.path.dirname(__file__), 'viewproducerworkers.html')
        self.response.out.write(template.render(path, template_values))
        return
    
    '''
    Exception handler
    '''
    def handle_exception(self, exception, debug_mode):
        if debug_mode:
            super(ViewMyWorkers, self).handle_exception(exception, debug_mode)
        else:
            template_values = bene_util.initTemplate(self.request.uri)
            path = os.path.join(os.path.dirname(__file__), 'not_found.html')
            self.response.out.write(template.render(path, template_values))
            return