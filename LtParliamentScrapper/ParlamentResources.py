from typing import *
from SimpleBenchmarkToConsole import *
import sys
import urllib.request

class ParlamentResources:
    
    __baseUrl = 'http://apps.lrs.lt/sip/p2b.ad_'

    termsOfOfficeUrl = 'seimo_kadencijos'
    membersByTermsOfOfficeUrl = 'seimo_nariai?kadencijos_id='
    agendaUrl = 'seimo_posedzio_darbotvarke?posedzio_id='
    meetingUrl = 'seimo_posedzio_eiga_full?posedzio_id='
    allTermsOfOffice = 'seimo_kadencijos'
    allSessions = 'seimo_sesijos?ar_visos=T'
    initiatedLegislations = 'sn_inicijuoti_ta_projektai?asmens_id='
    legislationSuggestions = 'sn_pasiulymai_ta_projektams?asmens_id='
    meetingsUrl = 'seimo_posedziai?sesijos_id='
    votingResultsUrl = 'sp_balsavimo_rezultatai?balsavimo_id='


    @SimpleBenchmarkToConsole
    def GetData(self, url: str) -> str:
        print('Url --> ' + url)

        request = urllib.request.urlopen(self.__baseUrl + url)
        if request.status == 200:
            contents = request.read().decode('utf-8')
            return contents

        raise Exception(request.reason)

