import sys
import time
from timeit import default_timer as timer
import datetime


def SimpleBenchmarkToConsole(method):
    def wrapper(*args, **kw):

        print(f"-------> Method '{method.__name__}'")
        print(f"Started ---> {datetime.datetime.now()}.")

        ts = timer()
        result = method(*args, **kw)
        te = timer()
        
        print(f"Execution time ---> {int((te - ts) * 1000)}ms")

        return result
    return wrapper
