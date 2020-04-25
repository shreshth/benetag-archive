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

class ProducerTutorial(webapp.RequestHandler):
    def get(self):
        template_values = bene_util.initTemplate(self.request.uri)
        path = os.path.join(os.path.dirname(__file__), 'producertutorial.html')
        self.response.out.write(template.render(path, template_values))
        return
        
        
class ConsumerTutorial(webapp.RequestHandler):
    def get(self):
        template_values = bene_util.initTemplate(self.request.uri)
        path = os.path.join(os.path.dirname(__file__), 'consumertutorial.html')
        self.response.out.write(template.render(path, template_values))
        return
        
                