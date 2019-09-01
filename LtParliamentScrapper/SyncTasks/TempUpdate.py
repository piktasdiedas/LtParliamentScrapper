from typing import *

from XmlParser import *
from ParlamentResources import *
from DatabaseConnector import *


def TempUpdate() -> None:
    
    resources = ParlamentResources()
    database = DatabaseConnector()
    parser = XmlParser()

    
    sessionsXml = resources.GetData('seimo_sesijos?ar_visos=T')
    sessions = parser.ParseSessionsFromXml(sessionsXml)
    for s in sessions:
        meetingsXml = resources.GetData('seimo_posedziai?sesijos_id=' + s.Id) 
        meetingDocuments = parser.ParseMeetingDocumentsFromXml(meetingsXml)
        database.WriteToDatabase(meetingDocuments, 'Meetings', meetingDocumentMap, ['MeetingId', 'Value'])

