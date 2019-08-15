from typing import *
from SimpleBenchmarkToConsole import *
import sys
import urllib.request

class ParlamentResources:
    
    __baseUrl = 'http://apps.lrs.lt/sip/p2b.ad_'

    termsOfOfficeUrl = 'seimo_kadencijos'
    membersUrl = 'seimo_nariai?kadencijos_id='

    @SimpleBenchmarkToConsole
    def GetData(self, url: str) -> str:
        request = urllib.request.urlopen(self.__baseUrl + url)
        if request.status == 200:
            contents = request.read().decode('utf-8')
            return contents

        raise Exception(request.reason)

