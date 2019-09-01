from typing import *

from XmlParser import *
from ParlamentResources import *
from DatabaseConnector import *

def TermsOfOffice_Sessions_Members_UpdateTask() -> None:
 
    doUpdate = lambda x: True

    resources = ParlamentResources()
    database = DatabaseConnector()
    parser = XmlParser()


    #termOfOfficeXml = resources.GetData('seimo_kadencijos')
    #termOfOffice = parser.ParseTermOfOfficeFromXml(termOfOfficeXml)
    #database.WriteToDatabase(termOfOffice, 'TermOfOffice', termOfOfficeMap, ['Id'])


    #sessionsXml = resources.GetData('seimo_sesijos?ar_visos=T')
    #sessions = parser.ParseSessionsFromXml(sessionsXml)
    #database.WriteToDatabase(sessions, 'Sessions', sessionMap, ['Id'])

    #currentTermOfOfficeStart = datetime.datetime.strptime(getattr(termOfOffice[len(termOfOffice) - 1], 'From'), '%Y-%m-%d').date()

    #def shouldUpdateDelegate(obj):
    #    d = datetime.datetime.strptime(obj.From, '%Y-%m-%d').date()
    #    return d >= currentTermOfOfficeStart
    


    #termOfOffice.reverse()
    #for t in termOfOffice:
    #    membersXml = resources.GetData('seimo_nariai?kadencijos_id=' + str(t.Id))
    #    members = parser.ParseMembersFromXml(membersXml)
    #    database.WriteToDatabase(members, 'Members', memberMap, ['Id'])
    #    termOfOfficeMembersXml = resources.GetData('seimo_nariai?kadencijos_id=' + str(t.Id))
    #    termOfOfficeMembers = parser.ParseTermOfOfficeMembersFromXml(termOfOfficeMembersXml)
    #    database.WriteToDatabase(termOfOfficeMembers, 'TermOfOfficeMembers', termOfOfficeMemberMap, ['TermOfOfficeId', 'MemberId'])
        
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



    existing = database.ExecuteMultipleRaw('SELECT * FROM (SELECT DISTINCT MeetingId FROM `AgendaQuestions` x UNION SELECT DISTINCT MeetingId From `Agendas` c UNION SELECT DISTINCT MeetingId FROM `AgendaQuestionSpeakers`) v')
    print(existing)
    
    sessionsXml = resources.GetData('seimo_sesijos?ar_visos=T')
    sessions = parser.ParseSessionsFromXml(sessionsXml)
    for s in sessions:
        if s.TermOfOffice != '6':
            continue

        meetingsXml = resources.GetData('seimo_posedziai?sesijos_id=' + s.Id) 
        meetings = parser.ParseMeetingsFromXml(meetingsXml)
        meetingDocuments = parser.ParseMeetingDocumentsFromXml(meetingsXml)
        database.WriteToDatabase(meetings, 'Meetings', meetingMap, ['Id'])
        database.WriteToDatabase(meetingDocuments, 'MeetingDocuments', meetingDocumentMap, ['MeetingId', 'Url'])

        for m in meetings:
            agendaXml = resources.GetData(f'seimo_posedzio_darbotvarke?posedzio_id={m.Id}')

            agendas = parser.ParseAgendasFromXml(agendaXml, m.Id)
            agendaQuestions = parser.ParseAgendaQuestionsFromXml(agendaXml, m.Id)
            agendaQuestionSpeakers = parser.ParseAgendaQuestionSpeakersFromXml(agendaXml, m.Id)


            database.WriteToDatabase(agendas, 'Agendas', agendaMap, ['MeetingId', 'Number'], doUpdate)
            database.WriteToDatabase(agendaQuestions, 'AgendaQuestions', agendaQuestionMap, ['QuestionId', 'Number'], doUpdate)
            database.WriteToDatabase(agendaQuestionSpeakers, 'AgendaQuestionSpeakers', agendaQuestionSpeakerMap, ['MeetingId', 'Number', 'Person'], doUpdate)




