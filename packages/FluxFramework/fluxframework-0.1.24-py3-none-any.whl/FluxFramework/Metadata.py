################################################################################
import functools
import inspect

def register():
    def wrapped(fn):
        @functools.wraps(fn)
        def wrapped_f(*args, **kwargs):
            return fn(*args, **kwargs)
        wrapped_f.methodName = wrapped_f.__name__ 
        wrapped_f.methodDescription = wrapped_f.__doc__ 
        return wrapped_f
    return wrapped

metadataOrderCache = dict()

def assignOrder():
    def do_assignment(to_func):
        module = inspect.getmodule(to_func)
        currentNum = metadataOrderCache.get(module,-1)
        if currentNum == -1:
            metadataOrderCache[module] = 0
        to_func.order = metadataOrderCache[module]
        metadataOrderCache[module] += 1
        return to_func
    return do_assignment

@register()
def GetMethodOrder(method):
    '''Returns the value of the .order property on the provided method. -1 if no order is assigned'''
    try:
        return int(method.order)
    except:
        return int(-1)
@register()

def GetMethodName(method):
    '''Returns the value of the .methodName property on the provided method. __name__ if no order is assigned'''
    try:
        return str(method.methodName)
    except:
        return str(method.__name__)
    
def GetMethodDescription(method):
    '''Returns the value of the .methodDescription property on the provided method. __doc__ if no order is assigned'''
    try:
        return str(method.methodDescription)
    except:
        return str(method.__doc__)
    
@register()
def OutputMethodMetadata(method):
    '''Outputs the stored metadata for the given method object'''
    print(method.methodName)
    print(method.methodDescription)

################################################################################