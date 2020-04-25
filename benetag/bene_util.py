from google.appengine.api import users
import bene_query
import difflib
import entities
import os

#---------------------------------
#---------- SIGNED IN ------------
#---------------------------------
def isSignedInProducer(user):
    ''' is the user a signed-in producer'''
    if user:
        if bene_query.getCurrentUser().isProducer:
            return True
    return False

def isSignedInConsumer(user):
    ''' is the user a signed in consumer '''
    if user:
        if bene_query.getCurrentUser().isConsumer:
            return True
    return False     

#---------------------------------
#---------- PRODUCER -------------
#---------------------------------

""" 
Does a similar producer already exist?
"""
def doesSimilarProducerExist(producer_add):
    ''' Does a similar producer already exist? Use to warn the user. '''
    producers = entities.Producer.all().filter('name =', producer_add.name)
    for producer in producers:
        if producer:
            return True
    return False   

#---------------------------------
#---------- FACTORY  -------------
#---------------------------------

"""
Does the location already exist under the current producer? 
"""
def doesExactLocationExist(location_add):
    ''' DON'T USE THIS. Use doesLocationExist() '''
    if location_add.unique:
        producer = bene_query.getCurrentProducer()
        if producer:
            # if two have same unique ID
            locations = producer.getLocations().filter('unique = ', location_add.unique)
            for location in locations:
                if location: return True
    return False

"""
Does a similar location already exist under the current producer?
"""
def doesSimilarLocationExist(location_add, key=False):
    ''' DON'T USE THIS. Use doesLocationExist() '''
    # checks for same location name
    producer = bene_query.getCurrentProducer()
    if producer:
        locations = producer.getLocations().filter('name = ', location_add.name)
        for location in locations:
            if location : 
                if key:
                    if location_add.key() != location.key(): 
                        return True
                else: return True    
    return False

"""
Does the location exist under the current producer? 
"""
def doesLocationExist(location_add):
    ''' Does the location exist under the current producer? Use to warn user. '''
    if location_add.unique: # if no unique ID, then need location name to be unique
        return doesExactLocationExist(location_add)
    return doesSimilarLocationExist(location_add) 

#---------------------------------
#---------- BADGES ---------------
#---------------------------------

"""
Does the badge already exist?
"""
def doesBadgeExist(badge_add):
    ''' Does the badge already exist? '''
    # checks for same badge name
    badges = entities.Badge.all().filter('name =', badge_add.name)
    for badge in badges:
        if badge: return True    
    return False

#---------------------------------
#---------- WORKER ---------------
#---------------------------------

"""
Does the exact worker already exist under the current producer?
"""
def doesExactWorkerExist(worker_add):
    ''' DON'T USE THIS. Use doesWorkerExist() '''
    if worker_add.unique: 
        producer = bene_query.getCurrentProducer()
        if producer:
            # if two workers have same unique ID
            workers = producer.getWorkers().filter('unique =', worker_add.unique)
            for worker in workers:
                if worker: return True
    return False

"""
Does a similar worker already exist under the current producer?
"""
def doesSimilarWorkerExist(worker_add, key=False):
    ''' DON'T USE THIS. Use doesWorkerExist() '''
    # checks for same worker name
    producer = bene_query.getCurrentProducer()
    if producer:
        workers = producer.getWorkers().filter('name =', worker_add.name)
        for worker in workers:
            if worker:
                if key:
                    if worker_add.key() != worker.key(): 
                        return True
                else: return True    
    return False

""" 
Does the worker exist under the current producer?
"""
def doesWorkerExist(worker_add):
    ''' Does the worker exist under the current producer? Use to warn user. ''' 
    if worker_add.unique: # if no unique ID, then need unique names in location
        return doesExactWorkerExist(worker_add)
    return doesSimilarWorkerExist(worker_add) 

#---------------------------------
#---------- PRODUCT --------------
#---------------------------------

"""
Does similar product configuration already exist under the current producer?
"""
def doesSimilarProductConfigExist(productconfig_add, product_line):
    ''' Does a similar product config exist under this product line'''
    if productconfig_add:
        productconfigs = product_line.getConfigs().filter('config_name =', productconfig_add.config_name)
        if productconfigs:
            for productconfig in productconfigs:
                if productconfig: return True
    return False   

"""
Does a similar product line already exist?
"""
def doesSimilarProductLineExist(product_line_add):
    ''' Does a similar product line exist '''
    # checks for same product line name 
    if not product_line_add:
        return True
    producer = bene_query.getCurrentProducer()
    if producer:
        product_lines = producer.getProductLines()
        if product_lines:
            for product_line in product_lines:
                if product_line: 
                    if product_line.name == product_line_add.name:
                        return True    
    return False


#---------------------------------
#-------------- MISC -------------
#---------------------------------

"""
Initialize the template for each page with the consumer/producer/not-signed-in dashboard
Also puts in values from the URL
"""
def initTemplate(url):
    '''Initialize the template for each page with the consumer/producer/not-signed-in dashboard. Also puts in values from the URL'''
    dictionary = urldecode(url)
    user = users.get_current_user()
    
    # Exactly one of these three will be true
    signedinconsumer = isSignedInConsumer(user)
    if os.environ.get('HTTP_HOST'): 
        url = os.environ['HTTP_HOST'] 
    elif os.environ.get('SERVER_NAME'): 
        url = os.environ['SERVER_NAME'] 
    else:
        url = 'localhost:8080'; 
    
    dictionary['HOSTNAME'] = url;
    dictionary['signedinconsumer'] = signedinconsumer
    if signedinconsumer:
        _consumer = bene_query.getCurrentConsumer()
        if _consumer:
            dictionary['hasunread'] = _consumer.has_unread
    dictionary['signedinproducer'] = isSignedInProducer(user)
    dictionary['notsignedin'] = False
    if not user:
        dictionary['notsignedin'] = True
    return dictionary         

"""
Decode a url into a dictionary of arguments
Assumption: Only one value per argument
"""
def urldecode(url):
    ''' Decode a url into a dictionary of arguments. Assumption: Only one value per argument '''
    queries = url.split('?') 
    dictionary = {} 
    for query in queries:
        args = query.split('&') 
        for arg in args: 
            if '=' in arg: 
                key,val = arg.split('=') 
                dictionary[key] = val
    return dictionary


"""
Get email for a user
"""
def getEmail(user):
    ''' Get email for a user '''
    if user:
        return user.email()
    return None

"""
Sanitize input (string)
"""
def sanitize(user_in):
    ''' sanitize a string'''
    return (user_in)

"""
Sanitize input (list)
"""
def sanitizeList(user_in_list):
    ''' sanitize a list'''
    return [(user_in) for user_in in user_in_list]

def unique(s):
    """Return a list of the elements in s, but without duplicates.

    For example, unique([1,2,3,1,2,3]) is some permutation of [1,2,3],
    unique("abcabc") some permutation of ["a", "b", "c"], and
    unique(([1, 2], [2, 3], [1, 2])) some permutation of
    [[2, 3], [1, 2]].

    For best speed, all sequence elements should be hashable.  Then
    unique() will usually work in linear time.

    If not possible, the sequence elements should enjoy a total
    ordering, and if list(s).sort() doesn't raise TypeError it's
    assumed that they do enjoy a total ordering.  Then unique() will
    usually work in O(N*log2(N)) time.

    If that's not possible either, the sequence elements must support
    equality-testing.  Then unique() will usually work in quadratic
    time.
    """

    n = len(s)
    if n == 0:
        return []

    # Try using a dict first, as that's the fastest and will usually
    # work.  If it doesn't work, it will usually fail quickly, so it
    # usually doesn't cost much to *try* it.  It requires that all the
    # sequence elements be hashable, and support equality comparison.
    u = {}
    try:
        for x in s:
            u[x] = 1
    except TypeError:
        del u  # move on to the next method
    else:
        return u.keys()

    # We can't hash all the elements.  Second fastest is to sort,
    # which brings the equal elements together; then duplicates are
    # easy to weed out in a single pass.
    # NOTE:  Python's list.sort() was designed to be efficient in the
    # presence of many duplicate elements.  This isn't true of all
    # sort functions in all languages or libraries, so this approach
    # is more effective in Python than it may be elsewhere.
    try:
        t = list(s)
        t.sort()
    except TypeError:
        del t  # move on to the next method
    else:
        assert n > 0
        last = t[0]
        lasti = i = 1
        while i < n:
            if t[i] != last:
                t[lasti] = last = t[i]
                lasti += 1
            i += 1
        return t[:lasti]
    # Brute force is all that's left.
    u = []
    for x in s:
        if x not in u:
            u.append(x)
    return u

def bestMatch(query, resultList):
    '''
    return resultList reordered by order of closeness of search
    resultList should have entities with a name
    '''
    # find ratios of similarity (low ratio = low similarity)
    ratios = []
    for result in resultList:
        ratios.append(difflib.SequenceMatcher(None, query.lower(), result.name.lower()).ratio())
        
    # reverse sort based on similarity
    return [x for (y,x) in sorted(zip(ratios, resultList), reverse=True)]
