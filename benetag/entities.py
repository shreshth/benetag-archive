from google.appengine.ext import db
import base64
import bene_util
import re
    

######################## 
# USER
########################

empty_val = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAJYAAACWCAYAAAA8AXHiAAACoUlEQVR4Xu3SMQ0AAAzDsJU/6aHI5wLoEXlnCgQFFny6VODAgiApAFaS1SlYDCQFwEqyOgWLgaQAWElWp2AxkBQAK8nqFCwGkgJgJVmdgsVAUgCsJKtTsBhICoCVZHUKFgNJAbCSrE7BYiApAFaS1SlYDCQFwEqyOgWLgaQAWElWp2AxkBQAK8nqFCwGkgJgJVmdgsVAUgCsJKtTsBhICoCVZHUKFgNJAbCSrE7BYiApAFaS1SlYDCQFwEqyOgWLgaQAWElWp2AxkBQAK8nqFCwGkgJgJVmdgsVAUgCsJKtTsBhICoCVZHUKFgNJAbCSrE7BYiApAFaS1SlYDCQFwEqyOgWLgaQAWElWp2AxkBQAK8nqFCwGkgJgJVmdgsVAUgCsJKtTsBhICoCVZHUKFgNJAbCSrE7BYiApAFaS1SlYDCQFwEqyOgWLgaQAWElWp2AxkBQAK8nqFCwGkgJgJVmdgsVAUgCsJKtTsBhICoCVZHUKFgNJAbCSrE7BYiApAFaS1SlYDCQFwEqyOgWLgaQAWElWp2AxkBQAK8nqFCwGkgJgJVmdgsVAUgCsJKtTsBhICoCVZHUKFgNJAbCSrE7BYiApAFaS1SlYDCQFwEqyOgWLgaQAWElWp2AxkBQAK8nqFCwGkgJgJVmdgsVAUgCsJKtTsBhICoCVZHUKFgNJAbCSrE7BYiApAFaS1SlYDCQFwEqyOgWLgaQAWElWp2AxkBQAK8nqFCwGkgJgJVmdgsVAUgCsJKtTsBhICoCVZHUKFgNJAbCSrE7BYiApAFaS1SlYDCQFwEqyOgWLgaQAWElWp2AxkBQAK8nqFCwGkgJgJVmdgsVAUgCsJKtTsBhICoCVZHUKFgNJAbCSrE7BYiApAFaS1SlYDCQFwEqyOn1BggCXptKxUAAAAABJRU5ErkJggg=="
dataUrlPattern = re.compile('data:image/(png|jpeg|bmp|tiff|svg+xml);base64,(.*)$')

"""
Data type representing a user
"""
class User(db.Model):
    email = db.StringProperty()
    isProducer = db.BooleanProperty()
    isConsumer = db.BooleanProperty()
    owner = db.UserProperty()

######################## 
# CONSUMER
########################

"""
Data type representing a consumer
"""
class Consumer(db.Model):
    #profile information
    name = db.StringProperty()
    email = db.StringProperty()
    email_public = db.StringProperty()
    profile = db.TextProperty()
    def shortDescription(self):
        if self.profile:
            if len(self.profile) > 100:
                return self.profile[0:100] + "..."
            else: 
                return self.profile[0:100]
        return ""
    productConfigsRated = db.ListProperty(db.Key)
    
    _picture = db.BlobProperty()
    def addPicture(self, picture_add):
        if picture_add:
            if picture_add == empty_val: return 
            imgb64 = dataUrlPattern.match(picture_add).group(2)
            if imgb64 is not None and len(imgb64) > 0:
                self._picture = db.Blob(base64.b64decode(imgb64))
#            ''' 
#            TODO: check for mimetype here
#            '''
#            if isinstance(picture_add, unicode):
#                self._picture = picture_add.encode('utf-8', 'replace')
#            else:
#                self._picture = picture_add
    def getPicture(self):
        if self._picture:
            return self._picture
        return None
    def hasImage(self):
        if self._picture:
            return True
        return False
    def addProductConfigRated(self, productConfigKey):
        self.productConfigsRated.add(productConfigKey)
    def checkProductConfigRated(self, productConfigKey):
        return self.productConfigsRated.contains(productConfigKey)
    
     
    # messages
    has_unread = db.IntegerProperty()
    _msgrcd = db.ListProperty(db.Key)
    def addReceivedMsg(self, key):
        if key:
            if key not in self._msgrcd:
                self._msgrcd.append(key)
    def getReceivedMsg(self):
        if self._msgrcd:
            __msgrcd = db.get(self._msgrcd)
            return [msgrcd for msgrcd in __msgrcd if msgrcd] # return non-None products
        else:
            return None
    
    def getSentMsg(self, key):
        return self.messagefromconsumer_set
        
        
    #security
    owner = db.UserProperty()
    verified = db.BooleanProperty()
    
    #rating-this is a denormalized 'tuple' - MUST add/remove concurrently 
    #from both lists!!!
    _productsRated = db.ListProperty(db.Key)
    _ratingsAdded = db.ListProperty(float)
    
    #closet
    _products = db.ListProperty(db.Key)
    def addProduct(self, key):
        if key:
            if key not in self._products:
                self._products.append(key) 
    def remProduct(self, key):
        if key:
            if key in self._products:
                self._products.remove(key)
    def getProducts(self):
        if self._products:
            __products = db.get(self._products)
            return [product for product in __products if product] # return non-None products
        else:
            return None
    def hasProduct(self, key):
        if key in self._products:
            return True
        return False

######################## 
# PRODUCER
########################

"""
Data type representing a producer
"""
class Producer(db.Model):
    #profile information
    name = db.StringProperty(required=True)
    email = db.StringProperty(required=True)
    email_public = db.StringProperty()
    description = db.TextProperty()
    def shortDescription(self):
        if self.description:
            if len(self.description) > 100:
                return self.description[0:100] + "..."
            else: 
                return self.description[0:100]
        return ""
        
    _picture = db.BlobProperty()
    def addPicture(self, picture_add):
        if picture_add:
            if picture_add == empty_val: return 
            imgb64 = dataUrlPattern.match(picture_add).group(2)
            if imgb64 is not None and len(imgb64) > 0:
                self._picture = db.Blob(base64.b64decode(imgb64))
#            ''' 
#            TODO: check for mimetype here
#            '''
#            if isinstance(picture_add, unicode):
#                self._picture = picture_add.encode('utf-8', 'replace')
#            else:
#                self._picture = picture_add
    def getPicture(self):
        if self._picture:
            return self._picture
        return None
    def hasImage(self):
        if self._picture:
            return True
        return False
    
    # messages
    _msgrcd = db.ListProperty(db.Key)
    def addReceivedMsg(self, key):
        if key:
            if key not in self._msgrcd:
                self._msgrcd.append(key)
    def getReceivedMsg(self, key):
        if self._msgrcd:
            __msgrcd = db.get(self._msgrcd)
            return [msgrcd for msgrcd in __msgrcd if msgrcd] # return non-None products
        else:
            return None

    def getSentMsg(self):
        return self.messagefromproducer_set
        
        
    #security
    owner = db.UserProperty()
    verified = db.BooleanProperty()
       
    #hierarchical information    
    def getLocations(self):
        return self.location_set
    def getWorkers(self):
        return self.worker_set
    def getProducts(self):
        return self.product_set
    def getProductLines(self):
        return self.productline_set
    
    
######################## 
# MESSAGES
########################
"""
Data type representing a message from producer
"""
class MessageFromProducer(db.Model):
    text = db.TextProperty()
    receiver = db.ReferenceProperty()
    sender = db.ReferenceProperty(Producer)
    num_receivers = db.IntegerProperty()

"""
Data type representing a message from consumer
"""
class MessageFromConsumer(db.Model):
    text = db.TextProperty()
    receiver = db.ReferenceProperty(Producer)
    sender = db.ReferenceProperty(Consumer)
 
######################## 
# LOCATION
########################   
 
"""
Data type representing a location
"""
class Location(db.Model):
    #profile information
    name = db.StringProperty()
    address = db.PostalAddressProperty()
    location = db.GeoPtProperty()
    description = db.TextProperty()
    def shortDescription(self):
        if self.description:
            if len(self.description) > 100:
                return self.description[0:100] + "..."
            else: 
                return self.description[0:100]
        return ""
    
    _picture = db.BlobProperty()
    def addPicture(self, picture_add):
        if picture_add:
            if picture_add == empty_val: return 
            imgb64 = dataUrlPattern.match(picture_add).group(2)
            if imgb64 is not None and len(imgb64) > 0:
                self._picture = db.Blob(base64.b64decode(imgb64))
#            ''' 
#            TODO: check for mimetype here
#            '''
#            if isinstance(picture_add, unicode):
#                self._picture = picture_add.encode('utf-8', 'replace')
#            else:
#                self._picture = picture_add
    def getPicture(self):
        if self._picture:
            return self._picture
        return None
    def hasImage(self):
        if self._picture:
            return True
        return False
    
    #security
    owner = db.UserProperty()
    unique = db.StringProperty()
    
    #hierarchical information
    _producer = db.ReferenceProperty(Producer)
    def getProducer(self):
        return self._producer
    def addProducer(self, producer_add):
        self._producer = producer_add
        
    def getWorkers(self):
        return self.worker_set
            
    _productconfigs = db.ListProperty(db.Key)
    def addProductConfig(self, key):
        if key:
            if key not in self._productconfigs:
                self._productconfigs.append(key) 
    def remProductConfig(self, key):
        if key:
            if key in self._productconfigs:
                self._productconfigs.remove(key) 
    def getProductConfigs(self):
        if self._productconfigs:
            __productconfigs = db.get(self._productconfigs)
            return [productconfig for productconfig in __productconfigs if productconfig] # return non-None products
        else:
            return None
        ''' 
        None products appear if a certain productconfig was deleted from
        datastore manually
        '''
    
    def getProductLines(self):
        _productconfigs = self.getProductConfigs()
        _productlineskeys = []
        _productlines = []
        if _productconfigs:
            for _productconfig in _productconfigs:
                if _productconfig:
                    _productline = _productconfig.getProductLine()
                    if _productline.key() not in _productlineskeys:
                        _productlineskeys.append(_productline.key())
                        _productlines.append(_productline)
        if len(_productlines) > 0: return _productlines
        return None     
        
######################## 
# PATH
########################
    
"""
Location in path (with list order)
"""
class LocationInPath(db.Model):
    location = db.ReferenceProperty(Location)
    index = db.IntegerProperty()
    text = db.TextProperty()
    
######################## 
# WORKER
########################
    
"""
Data type representing a worker
"""
class Worker(db.Model):
    # profile information
    name = db.StringProperty()
    profile = db.TextProperty()
    def shortDescription(self):
        if self.profile:
            if len(self.profile) > 100:
                return self.profile[0:100] + "..."
            else: 
                return self.profile[0:100]
        return ""
    
    _picture = db.BlobProperty()
    def addPicture(self, picture_add):
        if picture_add:
            if picture_add == empty_val: return 
            imgb64 = dataUrlPattern.match(picture_add).group(2)
            if imgb64 is not None and len(imgb64) > 0:
                self._picture = db.Blob(base64.b64decode(imgb64))
#            ''' 
#            TODO: check for mimetype here
#            '''
#            if isinstance(picture_add, unicode):
#                self._picture = picture_add.encode('utf-8', 'replace')
#            else:
#                self._picture = picture_add
    def getPicture(self):
        if self._picture:
            return self._picture
        return None
    def hasImage(self):
        if self._picture:
            return True
        return False
    
    # security
    owner = db.UserProperty()
    unique = db.StringProperty()

    # hierarchical information
    _producer = db.ReferenceProperty(Producer)
    def getProducer(self):
        return self._producer
    def addProducer(self, producer_add):
        self._producer = producer_add
        
    _location = db.ReferenceProperty(Location)
    def getLocation(self):
        return self._location
    def addLocation(self, location_add):
        self._location = location_add
    def remLocation(self, location_rem):
        if self._location.key() == location_rem.key():
            self._location = None
    def clearLocation(self):
        self._location = None        
        
    _productconfigs = db.ListProperty(db.Key)
    def addProductConfig(self, key):
        if key:
            if key not in self._productconfigs:
                self._productconfigs.append(key) 
    def remProductConfig(self, key):
        if key:
            if key in self._productconfigs:
                self._productconfigs.remove(key) 
    def getProductConfigs(self):
        if self._productconfigs:
            __productconfigs = db.get(self._productconfigs)
            return [productconfig for productconfig in __productconfigs if productconfig] # return non-None products
        else:
            return None
        ''' 
        None products appear if a certain productconfig was deleted from
        datastore manually
        '''

    def getProductLines(self):
        _productconfigs = self.getProductConfigs()
        _productlineskeys = []
        _productlines = []
        if _productconfigs:
            for _productconfig in _productconfigs:
                if _productconfig:
                    _productline = _productconfig.getProductLine()
                    if _productline.key() not in _productlineskeys:
                        _productlineskeys.append(_productline.key())
                        _productlines.append(_productline)
        if len(_productlines) > 0: return _productlines
        return None     
        

######################## 
# STORE LINK
########################
"""
Data type representing an external store link
"""
class StoreLink(db.Model):
    name = db.StringProperty()
    url = db.StringProperty()
    logo = db.BlobProperty()
    price = db.FloatProperty()
    # simple reliability score of the link
    score = db.IntegerProperty()
    
    hasThumbnail = db.BooleanProperty()
    hasPrice = db.BooleanProperty()
    
    def addLogo(self, picture_add):
        if picture_add:
            ''' 
            TODO: check for mimetype here
            '''
            if isinstance(picture_add, unicode):
                self._picture = picture_add.encode('utf-8', 'replace')
            else:
                self._picture = picture_add
 
######################## 
# PRODUCT LINE
########################
        
"""
Data type representing a product line
"""
class ProductLine(db.Model):
    name = db.StringProperty()
    description = db.TextProperty()
    def shortDescription(self):
        if self.description:
            if len(self.description) > 100:
                return self.description[0:100] + "..."
            else: 
                return self.description[0:100]
        return ""
    
    isLine = db.BooleanProperty()
    isConfig = db.BooleanProperty()
    isUnit = db.BooleanProperty()
    
    def getRating(self):
        sumRatings = 0.0
        count = 0
        _productconfigs = self.getConfigs()
        for productConfig in _productconfigs:
            sumRatings = sumRatings + (productConfig.rating * productConfig._num_ratings) 
            count = count + productConfig._num_ratings
        if count == 0: return 0
        return sumRatings / count  
    
    def getClosetCount(self):
        _configs = self.getConfigs()
        count = 0
        if _configs:
            for config in _configs:
                if config:
                    count += config.getClosetCount()
        return count
    def getConsumers(self):
        _configs = self.getConfigs()
        _consumers = []
        if _configs:
            for _config in _configs:
                if _config:
                    _consumers = _consumers + list(set(_config._consumers))
        if len(_consumers) > 0:
            return db.get(_consumers)
        return None
            
    def numProducts(self):
        _configs = self.getConfigs()
        count = 0
        for _config in _configs:
            count += _config.numProducts()
        return count
    
    def getProducts(self):
        return self.product_set
    def getConfigs(self):
        return self.productconfig_set
    
    def numConfigs(self):
        _configs = self.getConfigs()
        count = 0
        for _config in _configs: count += 1
        return count
    
    _picture = db.BlobProperty()
    def addPicture(self, picture_add):
        if picture_add:
            if picture_add == empty_val: return 
            imgb64 = dataUrlPattern.match(picture_add).group(2)
            if imgb64 is not None and len(imgb64) > 0:
                self._picture = db.Blob(base64.b64decode(imgb64))
#            ''' 
#            TODO: check for mimetype here
#            '''
#            if isinstance(picture_add, unicode):
#                self._picture = picture_add.encode('utf-8', 'replace')
#            else:
#                self._picture = picture_add
    def getPicture(self):
        if self._picture:
            return self._picture
        return None
    def hasImage(self):
        if self._picture:
            return True
        return False
    
    # security
    owner = db.UserProperty()
    unique = db.StringProperty()
    
    # hierarchical information
    _producer = db.ReferenceProperty(Producer)
    def getProducer(self):
        return self._producer
    def addProducer(self, producer_add):
        self._producer = producer_add

######################## 
# PRODUCT CONFIG
########################

"""
Data type representing a product configuration
"""
class ProductConfig(db.Model):
    # profile information
    def name(self):
        return self.getProductLine().name
    def getName(self):
        return self.getProductLine().name
    config_name = db.StringProperty()
    def description(self):
        return self.getProductLine().description
    def getDescription(self):
        return self.getProductLine().description
    def shortDescription(self):
        return self.getProductLine().shortDescription()
    
    isLine = db.BooleanProperty()
    isConfig = db.BooleanProperty()
    isUnit = db.BooleanProperty()
    
    _num_closet = db.IntegerProperty()
    
    store_link = db.ReferenceProperty(StoreLink)
    displayAmazon = db.BooleanProperty()
        
    def addClosetCount(self):
        self._num_closet = self._num_closet + 1
    def remClosetCount(self):
        self._num_closet = self._num_closet - 1
    def getClosetCount(self):
        return self._num_closet
    
    _consumers = db.ListProperty(db.Key)
    def addConsumer(self, key):
        if key:
            self._consumers.append(key)
    def remConsumer(self, key):
        if key:
            if key in self._consumers:
                self._consumers.remove(key)
    def getConsumers(self):
        _consumers_keys = list(set(self._consumers))
        _consumers = db.get(_consumers_keys)
        return [_consumer for _consumer in _consumers if _consumer]
    
    rating = db.FloatProperty()
    _num_ratings = db.IntegerProperty()
    def getRating(self):
        return self.rating
    def getRoundedRating(self):
        return round(self.rating*4)/4
    def updateRating(self, userRating, consumer):
        if self.key() in consumer._productsRated:
            index = consumer._productsRated.index(self.key())
            consumer._productsRated.pop(index)
            old_rating = consumer._ratingsAdded.pop(index)
            self.rating = (self._num_ratings*self.rating - old_rating) / float((self._num_ratings - 1))
            self._num_ratings = self._num_ratings - 1
           
        self.rating = (self._num_ratings*self.rating + userRating) / float((self._num_ratings + 1))
        self._num_ratings = self._num_ratings + 1
        consumer._productsRated.append(self.key())
        consumer._ratingsAdded.append(userRating)
        consumer.put()
    
    _product_line = db.ReferenceProperty(ProductLine)
    def getProductLine(self):
        return self._product_line
    def addProductLine(self, product_line_add):
        self._product_line = product_line_add
    
    def getProducts(self):
        return self.product_set
    def numProducts(self):
        products = self.product_set
        count = 0
        if products:
            for product in products:
                if product: count = count + 1 
        return count
    
    def getPicture(self):
        return self.getProductLine().getPicture()
    def hasImage(self):
        return self.getProductLine().hasImage()
            
    # security
    owner = db.UserProperty()
    unique = db.StringProperty()
    
    # hierarchical information
    # producer
    _producer = db.ReferenceProperty(Producer)
    def getProducer(self):
        return self._producer
    def addProducer(self, producer_add):
        self._producer = producer_add
        
    # path
    _path = db.ListProperty(db.Key)
    _path_primary_index = db.IntegerProperty()
    def getPath(self):
        ''' get path elements, including indices '''
        if self._path:
            __path = db.get(self._path)
            return [path for path in __path if path] # return non-None path elements
        else:
            return None
    def clearPath(self):
        ''' use when editing a product. clear path and then re-create one'''
        _path = self.getPath()
        if _path:
            for location in _path:
                self._path.remove(location.key())
                db.delete(location.key())
    def addLocationToPath(self, location_add, text_add, _index): 
        ''' self-explanatory '''
        if not _index:
            _index = len(self._path)
        if location_add:
            f = LocationInPath(location=location_add,
                              index=_index,
                              text=text_add)
            f.put()
            self._path.append(f.key())
    def setPrimaryLocation(self, location_primary):
        ''' primary location '''
        for path_element in self.getPath():
            if path_element.location.key() == location_primary.key():
                self._path_primary_index = path_element.index
                    
    # path
    _badges = db.ListProperty(db.Key)
    def addBadge(self, key):
        if key:
            if key not in self._badges:
                self._badges.append(key) 
    def remBadge(self, key):
        if key:
            if key in self._badges:
                self._badges.remove(key) 
    def getBadges(self):
        if self._badges:
            __badges = db.get(self._badges)
            return [badge for badge in __badges if badge] # return non-None badges
        else:
            return None
    
    # workers
    def getWorkers(self):
        if self._producer:
            return self._producer.getWorkers().filter('_productconfigs =', self.key())
        return Worker.all().filter('_productconfigs =', self.key)

    # locations
    def getLocations(self):
        ''' get path elements, only locations, no indices, in order '''
        if self._path:
            __path = db.get(self._path)
            return [path.location for path in __path if path] # return non-None path elements
        else:
            return None
    def getPrimaryLocation(self):
        if self._path:
            if self._path_primary_index:
                if self._path_primary_index >= 0 and self._path_primary_index < len(self._path):
                    return self.getPath()[self._path_primary_index].location
                else:
                    return self.getPath()[0].location
            else:
                return self.getPath()[0].location
        return None
    
    
######################## 
# PRODUCT UNIT
########################

class Product(db.Model):
    def name(self):
        return self.getProductLine().name
    def getName(self):
        return self.getProductLine().name
    def description(self):
        return self.getProductLine().description
    def getDescription(self):
        return self.getProductLine().description
    def shortDescription(self):
        return self.getProductLine().shortDescription()
    
    isLine = db.BooleanProperty()
    isConfig = db.BooleanProperty()
    isUnit = db.BooleanProperty()
    
    _product_line = db.ReferenceProperty(ProductLine)
    def getProductLine(self):
        return self._product_line
    def addProductLine(self, product_line_add):
        self._product_line = product_line_add
        
    _product_config = db.ReferenceProperty(ProductConfig)
    def getProductConfig(self):
        return self._product_config
    def addProductConfig(self, product_config_add):
        self._product_config = product_config_add
        
    # security
    owner = db.UserProperty()
    unique = db.StringProperty()
    
    # hierarchical information
    # producer
    _producer = db.ReferenceProperty(Producer)
    def getProducer(self):
        return self._producer
    def addProducer(self, producer_add):
        self._producer = producer_add
        
    def getPicture(self):
        return self.getProductLine().getPicture()
    def hasImage(self):
        return self.getProductLine().hasImage()

######################## 
# BADGE
########################

"""
Data type representing a badge
"""
class Badge(db.Model):
    name = db.StringProperty()
    description = db.StringProperty()
    def shortDescription(self):
        if self.description:
            if len(self.description) > 100:
                return self.description[0:100] + "..."
            else: 
                return self.description[0:100]
        return ""
    
    _picture = db.BlobProperty()
    def addPicture(self, picture_add):
        if picture_add:
            ''' 
            TODO: check for mimetype here
            '''
            if isinstance(picture_add, unicode):
                self._picture = picture_add.encode('utf-8', 'replace')
            else:
                self._picture = picture_add 
    def getPicture(self):
        if self._picture:
            return self._picture
        return None
    def hasImage(self):
        if self._picture:
            return True
        return False
    
    # hierarchical information
    def getProducts(self):
        return Product.all().filter('badges =', self)
