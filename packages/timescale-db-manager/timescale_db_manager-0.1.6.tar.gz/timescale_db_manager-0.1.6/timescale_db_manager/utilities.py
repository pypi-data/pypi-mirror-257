import time

def time_it(function):
    def wrapper(self, *args,**kwargs):
        attribute_postfix = function.__name__

        end_time = getattr(self, f'end_{attribute_postfix}')
        if end_time:
            start_time = getattr(self, f'start_{attribute_postfix}')
            setattr(self, f'start_{attribute_postfix}', end_time - start_time)
        else:
            setattr(self, f'start_{attribute_postfix}', time.time())

        return_value = function(self, *args, **kwargs)

        setattr(self, f'end_{attribute_postfix}', time.time())
        return return_value
    return wrapper