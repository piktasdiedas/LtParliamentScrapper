from typing import *
from datetime import date

from XmlParser import *
from ParlamentResources import *
from DatabaseConnector import *

def TermsOfOffice_Sessions_Members_UpdateTask() -> None:
 
    doUpdate = lambda x: True

    resources = ParlamentResources()
    database = DatabaseConnector()
    parser = XmlParser()


    testId = '-501401'
    aggg = resources.GetData('seimo_posedzio_darbotvarke?posedzio_id=' + testId)
    agendaModels = parser.ParseAgendaQuestionsFromXml(aggg, testId)
    assssss = parser.ParseAgendasFromXml(aggg, testId)
    meet = resources.GetData('seimo_posedzio_eiga_full?posedzio_id=' + testId)
    ddd = parser.ParseMeetingQuestionsFromXml(meet, agendaModels)
    #database.WriteToDatabase(ddd, 'MeetingQuestions', meetingQuestionMap, ['MeetingQuestionId', 'QuestionId'], doUpdate)
    database.WriteToDatabase(agendaModels, 'AgendaQuestions', agendaQuestionMap, ['QuestionId', 'Number'], doUpdate)

    #####

    termOfOfficeXml = resources.GetData('seimo_kadencijos')
    termOfOffice = parser.ParseTermOfOfficeFromXml(termOfOfficeXml)
    database.WriteToDatabase(termOfOffice, 'TermOfOffice', termOfOfficeMap, ['Id'])


    sessionsXml = resources.GetData('seimo_sesijos?ar_visos=T')
    sessions = parser.ParseSessionsFromXml(sessionsXml)
    database.WriteToDatabase(sessions, 'Sessions', sessionMap, ['Id'])

    currentTermOfOfficeStart = datetime.datetime.strptime(getattr(termOfOffice[len(termOfOffice) - 1], 'From'), '%Y-%m-%d').date()

    def shouldUpdateDelegate(obj):
        d = datetime.datetime.strptime(obj.From, '%Y-%m-%d').date()
        return d >= currentTermOfOfficeStart
    


    termOfOffice.reverse()
    for t in termOfOffice:
        break
        #if t.Id != '8':
        #    continue

        membersXml = resources.GetData('seimo_nariai?kadencijos_id=' + str(t.Id))
        members = parser.ParseMembersFromXml(membersXml)
        database.WriteToDatabase(members, 'Members', memberMap, ['Id'])

        termOfOfficeMembersXml = resources.GetData('seimo_nariai?kadencijos_id=' + str(t.Id))
        termOfOfficeMembers = parser.ParseTermOfOfficeMembersFromXml(termOfOfficeMembersXml)
        database.WriteToDatabase(termOfOfficeMembers, 'TermOfOfficeMembers', termOfOfficeMemberMap, ['TermOfOfficeId', 'MemberId'])
        
        committees = parser.ParseCommitteesFromXmlFromMembers(membersXml)
        committeeMembers = parser.ParseCommitteeMembersFromXmlFromMembers(membersXml)

        commissions = parser.ParseCommissionsFromXmlFromMembers(membersXml)
        commissionMembers = parser.ParseCommissionMembersFromXmlFromMembers(membersXml)

        factions = parser.ParseFactionsFromXmlFromMembers(membersXml)
        factionMembers = parser.ParseFactionMembersFromXmlFromMembers(membersXml)

        parlamentGroups = parser.ParseParlamentGroupsFromXmlFromMembers(membersXml)
        parlamentGroupMembers = parser.ParseParlamentGroupMembersFromXmlFromMembers(membersXml)

        database.WriteToDatabase(committees, 'Committees', committeeMap, ['Id'])
        database.WriteToDatabase(commissions, 'Commissions', commissionMap, ['Id'])
        database.WriteToDatabase(factions, 'Factions', factionMap, ['Id'])
        database.WriteToDatabase(parlamentGroups, 'ParlamentGroups', parlamentGroupMap, ['Id'])
        database.WriteToDatabase(committeeMembers, 'CommitteeMembers', committeeMemberMap, ['MemberId', 'CommitteeId', 'From'], shouldUpdateDelegate)
        database.WriteToDatabase(commissionMembers, 'CommissionMembers', commissionMemberMap, ['MemberId', 'CommissionId', 'From'], shouldUpdateDelegate)
        database.WriteToDatabase(factionMembers, 'FactionMembers', factionMemberMap, ['MemberId', 'FactionId', 'From'], shouldUpdateDelegate)
        database.WriteToDatabase(parlamentGroupMembers, 'ParlamentGroupMembers', parlamentGroupMemberMap, ['MemberId', 'ParlamentGroupId', 'From'], shouldUpdateDelegate)



    sessions.reverse()
    for s in sessions:
        #if int(s.Id) > 50:
        #    continue

        meetingsXml = resources.GetData('seimo_posedziai?sesijos_id=' + s.Id) 
        meetings = parser.ParseMeetingsFromXml(meetingsXml)
        meetingDocuments = parser.ParseMeetingDocumentsFromXml(meetingsXml)
        database.WriteToDatabase(meetings, 'Meetings', meetingMap, ['Id'], doUpdate)
        database.WriteToDatabase(meetingDocuments, 'MeetingDocuments', meetingDocumentMap, ['MeetingId', 'Url'])

        for m in meetings:
            agendaXml = resources.GetData(f'seimo_posedzio_darbotvarke?posedzio_id={m.Id}')

            agendas = parser.ParseAgendasFromXml(agendaXml, m.Id)
            agendaQuestions = parser.ParseAgendaQuestionsFromXml(agendaXml, m.Id)
            agendaQuestionSpeakers = parser.ParseAgendaQuestionSpeakersFromXml(agendaXml, m.Id)

            database.WriteToDatabase(agendas, 'Agendas', agendaMap, ['MeetingId', 'Number'], doUpdate)
            database.WriteToDatabase(agendaQuestions, 'AgendaQuestions', agendaQuestionMap, ['QuestionId', 'Number'], doUpdate)
            database.WriteToDatabase(agendaQuestionSpeakers, 'AgendaQuestionSpeakers', agendaQuestionSpeakerMap, ['MeetingId', 'Number', 'Person'], doUpdate)

            
            actualMeetingXml = resources.GetData(f'seimo_posedzio_eiga_full?posedzio_id={m.Id}')

            meetingQuestions = parser.ParseMeetingQuestionsFromXml(actualMeetingXml, agendaQuestions)
            votings = parser.ParseVotingsFromXml(actualMeetingXml)
            database.WriteToDatabase(votings, 'Votings', votingMap, ['VotingId'])
            database.WriteToDatabase(meetingQuestions, 'MeetingQuestions', meetingQuestionMap, ['MeetingId', 'Number'], doUpdate)
            
            for v in votings:
                break
                if 'bendru sutarimu' in v.Description:
                    continue # skip votings if there was no actual voting

                votesXml = resources.GetData(f'sp_balsavimo_rezultatai?balsavimo_id={v.VotingId}')
                votes = parser.ParseVotesFromXml(votesXml)
                if len(list(filter(lambda x: x.Vote == 3, votes))) == len(votes):
                    continue # skip votings if there was no actual voting

                database.WriteToDatabase(votes, 'Votes', voteMap, ['VotingId', 'MemberId'])
                hhhhh = 5555

