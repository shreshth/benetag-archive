from google.appengine.api import users
from google.appengine.ext import db, webapp
from google.appengine.ext.webapp import template
import bene_query
import bene_util
import entities
import os
import urllib

"""
Creates a form to send message to consumers of a productline/config
"""
class WriteMessageProducer(webapp.RequestHandler):
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
        _productgeneric = db.get(ID)
        ''' an error in getting the product will be redirected to exception handler'''
        
        if _productgeneric.owner != user: # if current user doesn't own product
            self.redirect('/producerhome?%s' % urllib.urlencode({'not_owner': True}))
            return
                        
        template_values = bene_util.initTemplate(self.request.uri)
        
        template_values['id'] = ID
        template_values['path'] = "message"
        template_values['num_sent'] = _productgeneric.getClosetCount()
        if _productgeneric.isConfig:
            template_values['name'] = _productgeneric.getName()
            template_values['is_config'] = True
            template_values['config'] = _productgeneric
            template_values['line'] = _productgeneric.getProductLine()
        elif _productgeneric.isLine:
            template_values['name'] = _productgeneric.name
            template_values['is_line'] = True
            template_values['line'] = _productgeneric
        
        path = os.path.join(os.path.dirname(__file__), 'producermsg.html')
        self.response.out.write(template.render(path, template_values))
        return
    
    '''
    Exception handler
    '''
    def handle_exception(self, exception, debug_mode):
        if debug_mode:
            super(WriteMessageProducer, self).handle_exception(exception, debug_mode)
        else:
            template_values = bene_util.initTemplate(self.request.uri)
            path = os.path.join(os.path.dirname(__file__), 'not_found.html')
            self.response.out.write(template.render(path, template_values))
            return
        
        
"""
Stores message from producer
"""
class SendMessageProducer(webapp.RequestHandler):
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
        _productgeneric = db.get(ID)
        ''' an error in getting the product will be redirected to exception handler'''
        
        if _productgeneric.owner != user: # if current user doesn't own product
            self.redirect('/producerhome?%s' % urllib.urlencode({'not_owner': True}))
            return
        
        _text = bene_util.sanitize(self.request.get('text'))
        
        msg = entities.MessageFromProducer(text=_text,
                                           sender=_producer,
                                           receiver=_productgeneric,
                                           num_receivers=_productgeneric.getClosetCount())
        msg.put()
        
        msg_key = msg.key()
        _consumers = _productgeneric.getConsumers()
        if _consumers:
            for _consumer in _consumers:
                if _consumer:
                    _consumer.addReceivedMsg(msg_key)
                    _consumer.has_unread += 1
                    _consumer.put()
        
        self.redirect('/myoutbox')
        return
    
    '''
    Exception handler
    '''
    def handle_exception(self, exception, debug_mode):
        if debug_mode:
            super(SendMessageProducer, self).handle_exception(exception, debug_mode)
        else:
            template_values = bene_util.initTemplate(self.request.uri)
            path = os.path.join(os.path.dirname(__file__), 'not_found.html')
            self.response.out.write(template.render(path, template_values))
            return
        
        
        
        