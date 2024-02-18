from functools import wraps

#
# decorators for plotting functions
#

def composed(*decs):
    """
    Composition decorator to bundle multiple decorators on one line
    
    Blatantly copied from: https://stackoverflow.com/questions/5409450/can-i-combine-two-decorators-into-a-single-one-in-python
    """
    def deco(f):
        for dec in reversed(decs):
            f = dec(f)
        return f
    return deco

def addgrid(func):
    """
    Decorator for adding a grid
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        # execute function
        func(*args, **kwargs)

        # add grid in post-processing
        if kwargs is not None and 'grid' in kwargs.keys():
            args[0].grid(linestyle='--', color='black', alpha=0.5)

    return wrapper

def addtitle(func):
    """
    Decorator for adding a grid
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        # execute function
        func(*args, **kwargs)

        # add title in post-processing
        if kwargs is not None and 'title' in kwargs.keys():
            args[0].set_title(kwargs['title'])

    return wrapper

def addlimits(func):
    """
    Decorator for function limits
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        # execute function
        func(*args, **kwargs)

        if kwargs is not None and 'xlim' in kwargs.keys():
            args[0].set_xlim(kwargs['xlim'])
        
        if kwargs is not None and 'ylim' in kwargs.keys():
            args[0].set_ylim(kwargs['ylim'])

    return wrapper

def addlegend(func):
    """
    Decorator for legends
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        # execute function
        func(*args, **kwargs)

        # add legend in post-processing
        if kwargs is not None and 'legend' in kwargs.keys() and 'legendloc' in kwargs.keys():
            args[0].legend(loc=kwargs['legendloc'])
        elif kwargs is not None and 'legend' in kwargs.keys():
            args[0].legend()

    return wrapper

def addbins(func):
    """
    Decorator for binning
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        # execute function
        func(*args, **kwargs)

        xlim = args[0].get_xlim()
        dx = (xlim[1] - xlim[0]) * 0.05

        # add bins in post-processing
        if kwargs is not None and 'bins' in kwargs.keys():
            for lim in kwargs['bins']:
                args[0].hlines(lim, -dx, dx, zorder=6, color='black', 
                               linewidth=1, linestyle='--')

    return wrapper