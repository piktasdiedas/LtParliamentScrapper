import urllib.request
import sys
import xml.etree.ElementTree as xmlTree
from datetime import datetime
import pymysql #PyMySQL-0.9.3
from typing import *
import collections
from datetime import datetime

#sys.path.insert(0, 'SyncTasks/TermsOfOffice_Sessions_Members_UpdateTask')

from Models import *
from SimpleBenchmarkToConsole import *
from ParlamentResources import *
from DatabaseConnector import *
from XmlParser import *
from SyncTasks.TermsOfOffice_Sessions_Members_UpdateTask import *
from SyncTasks.TempUpdate import *



def main(): 


    TermsOfOffice_Sessions_Members_UpdateTask()


    #database = DatabaseConnector()
    #parser = XmlParser()
    #resources = ParlamentResources()

    #currentTermOfOfficeStart = 0
    #def shouldUpdateDelegate(obj):
    #    d = datetime.datetime.strptime(obj.From, '%Y-%m-%d').date()
    #    return d >= currentTermOfOfficeStart
 
    #TempUpdate()
    #asdasd = 5


    #termOfOfficeXml = GetData('seimo_kadencijos')
    #termOfOffice = ParseTermOfOfficeFromXml(termOfOfficeXml)
    #WriteToDatabase(termOfOffice, 'TermOfOffice', termOfOfficeMap, ['Id'])


    #sessionsXml = GetData('seimo_sesijos?ar_visos=T')
    #sessions = ParseSessionsFromXml(sessionsXml)
    #WriteToDatabase(sessions, 'Sessions', sessionMap, ['Id'])

    #for id in range(1,9):
    #    membersXml = GetData('seimo_nariai?kadencijos_id=' + str(id))
    #    members = ParseMembersFromXml(membersXml)
    #    WriteToDatabase(members, 'Members', memberMap, ['Id'])
        #termOfOfficeMembersXml = GetData('seimo_nariai?kadencijos_id=' + str(id))
        #termOfOfficeMembers = ParseTermOfOfficeMembersFromXml(termOfOfficeMembersXml)
        #WriteToDatabase(termOfOfficeMembers, 'TermOfOfficeMembers', termOfOfficeMemberMap, ['TermOfOfficeId', 'MemberId'])
        
    #sessionsXml = GetData('seimo_sesijos?ar_visos=T')
    #sessions = ParseSessionsFromXml(sessionsXml)
    #for s in sessions:
    #    meetingsXml = GetData('seimo_posedziai?sesijos_id=' + s.Id) 
    #    meetings = ParseMeetingsFromXml(meetingsXml)
    #    WriteToDatabase(meetings, 'Meetings', meetingMap, ['Id'])

    #currentTermOfOfficeStart = database.ExecuteRawSingle('SELECT `From` FROM TermOfOffice ORDER BY Id DESC LIMIT 1')
    
    #print(ParlamentResources.membersUrl)
    #print(resources.membersUrl)
    
    #termOfOfficeXml = resources.GetData(resources.termsOfOfficeUrl)
    #termOfOffice = parser.ParseTermOfOfficeFromXml(termOfOfficeXml)
    #termOfOffice.reverse()
    #for t in termOfOffice:
    #    if t.Id == '2' or t.Id == '1':
    #        continue
    #    membersXml = resources.GetData('seimo_nariai?kadencijos_id=' + str(t.Id))
    #    members = parser.ParseMembersFromXml(membersXml)
    #    memberIndex = 0
    #    #for m in members:
    #    committees = parser.ParseCommitteesFromXmlFromMembers(membersXml)
    #    committeeMembers = parser.ParseCommitteeMembersFromXmlFromMembers(membersXml)

    #    commissions = parser.ParseCommissionsFromXmlFromMembers(membersXml)
    #    commissionMembers = parser.ParseCommissionMembersFromXmlFromMembers(membersXml)

    #    factions = parser.ParseFactionsFromXmlFromMembers(membersXml)
    #    factionMembers = parser.ParseFactionMembersFromXmlFromMembers(membersXml)

    #    parlamentGroups = parser.ParseParlamentGroupsFromXmlFromMembers(membersXml)
    #    parlamentGroupMembers = parser.ParseParlamentGroupMembersFromXmlFromMembers(membersXml)

    #    database.WriteToDatabase(committees, 'Committees', committeeMap, ['Id'])
    #    database.WriteToDatabase(commissions, 'Commissions', commissionMap, ['Id'])
    #    database.WriteToDatabase(factions, 'Factions', factionMap, ['Id'])
    #    database.WriteToDatabase(parlamentGroups, 'ParlamentGroups', parlamentGroupMap, ['Id'])
    #    database.WriteToDatabase(committeeMembers, 'CommitteeMembers', committeeMemberMap, ['MemberId', 'CommitteeId', 'From'], shouldUpdateDelegate)
    #    database.WriteToDatabase(commissionMembers, 'CommissionMembers', commissionMemberMap, ['MemberId', 'CommissionId', 'From'], shouldUpdateDelegate)
    #    database.WriteToDatabase(factionMembers, 'FactionMembers', factionMemberMap, ['MemberId', 'FactionId', 'From'], shouldUpdateDelegate)
    #    database.WriteToDatabase(parlamentGroupMembers, 'ParlamentGroupMembers', parlamentGroupMemberMap, ['MemberId', 'ParlamentGroupId', 'From'], shouldUpdateDelegate)



    #    print('-----')
    
    #sessionsXml = GetData('seimo_sesijos?ar_visos=T')
    #sessions = parser.ParseSessionsFromXml(sessionsXml)
    #for session in sessions:
    #    pass


    #votesXml = GetData('sp_balsavimo_rezultatai?balsavimo_id=-27089')
    #ParseVotesFromXml(votesXml)


    #commissionsXml = GetData('seimo_komisijos')
    #commissions = ParseCommisionsFromXml(commissionsXml)

    #committeesXml = GetData('seimo_komitetai')
    #committees = ParseCommisionsFromXml(committeesXml)

    #factionsXml = GetData('seimo_frakcijos')
    #factions = ParseFactionsFromXml(factionsXml)


    
    #sessionsXml = GetData('seimo_sesijos?kadencijos_id=7')
    #sessions = ParseSessionsFromXml(sessionsXml)
    #WriteToDatabase(sessions, 'Sessions', sessionMap, ['Id'])

    print('FINISH')





if __name__ == '__main__':
    sys.exit(int(main() or 0))
        


