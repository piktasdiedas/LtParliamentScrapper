import sys
import time
from timeit import default_timer as timer
import datetime


def SimpleBenchmarkToConsole(method):
    def wrapper(*args, **kw):

        print(f".")
        print(f"-------------")
        print(f"Method '{method.__name__}' started at {datetime.datetime.now()}.")

        ts = timer()
        result = method(*args, **kw)
        te = timer()
        
        print(f".")
        print(f"-------------")
        print(f"Method '{method.__name__}' execution time - {int((te - ts) * 1000)}ms")

        return result
    return wrapper
