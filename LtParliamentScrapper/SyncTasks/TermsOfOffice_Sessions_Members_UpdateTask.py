from typing import *
from datetime import datetime, date, timedelta

from XmlParser import *
from ParlamentResources import *
from DatabaseConnector import *

def TermsOfOffice_Sessions_Members_UpdateTask() -> None:
 
    def is28DaysAgo(o: object, prop: str = None) -> bool:
        _28DaysAgo = date.today() + timedelta(days=-28)
        prop = prop if prop is not None else 'To'
        dateStr = getattr(o, prop)

        if (dateStr is not None and len(dateStr) != len('xxxx-xx-xx')):
            dateStr = dateStr[0:len('xxxx-xx-xx')]

        return dateStr is not None and _28DaysAgo > date.fromisoformat(dateStr)

    allowToBreak = True


    doUpdate = lambda x: True

    resources = ParlamentResources()
    database = DatabaseConnector()
    parser = XmlParser()


    testId = '967'
    aggg = resources.GetData(resources.agendaUrl + testId)
    agendaModels = parser.ParseAgendaQuestionsFromXml(aggg, testId)
    assssss = parser.ParseAgendasFromXml(aggg, testId)
    meet = resources.GetData(resources.meetingUrl + testId)
    ddd = parser.ParseMeetingQuestionsFromXml(meet, agendaModels)
    #database.WriteToDatabase(ddd, 'MeetingQuestions', meetingQuestionMap, ['MeetingQuestionId', 'QuestionId'], doUpdate)
    database.WriteToDatabase(agendaModels, 'AgendaQuestions', agendaQuestionMap, ['QuestionId', 'Number'], doUpdate)

    #####

    termOfOfficeXml = resources.GetData(resources.allTermsOfOffice)
    termOfOffice = parser.ParseTermOfOfficeFromXml(termOfOfficeXml)
    database.WriteToDatabase(termOfOffice, 'TermOfOffice', termOfOfficeMap, ['Id'])


    sessionsXml = resources.GetData(resources.allSessions)
    sessions = parser.ParseSessionsFromXml(sessionsXml)
    database.WriteToDatabase(sessions, 'Sessions', sessionMap, ['Id'])

    currentTermOfOfficeStart = datetime.datetime.strptime(getattr(termOfOffice[len(termOfOffice) - 1], 'From'), '%Y-%m-%d').date()

    def shouldUpdateDelegate(obj):
        d = datetime.datetime.strptime(obj.From, '%Y-%m-%d').date()
        return d >= currentTermOfOfficeStart


    _28DaysAgo = date.today() + timedelta(days=-28)

    termOfOffice.reverse()
    for t in termOfOffice:

        if(is28DaysAgo(t) and allowToBreak):
            break

        
        membersXml = resources.GetData(resources.membersByTermsOfOfficeUrl + str(t.Id))
        members = parser.ParseMembersFromXml(membersXml)
        database.WriteToDatabase(members, 'Members', memberMap, ['Id'])

        termOfOfficeMembers = parser.ParseTermOfOfficeMembersFromXml(membersXml)
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


        for m in members:
            memberId = m.Id
            legislationsXml = resources.GetData(resources.initiatedLegislations + str(memberId))        
            legislationSuggestionsXml = resources.GetData(resources.legislationSuggestions + str(memberId))

            legislations = parser.ParseLegislationsFromXml(legislationsXml)
            legislationSuggestions = parser.ParseLegislationSuggestionsFromXml(legislationSuggestionsXml)

        
            database.WriteToDatabase(legislations, 'InitiatedLegislations', initiatedLegislationMap, ['MemberId', 'RegistrationNumber'], doUpdate)
            database.WriteToDatabase(legislationSuggestions, 'InitiatedLegislationSuggestions', initiatedLegislationSuggestionMap, ['MemberId', 'RegistrationNumber'], doUpdate)



    sessions.reverse()
    for s in sessions:
        
        if(is28DaysAgo(s) and allowToBreak):
            break

        meetingsXml = resources.GetData(resources.meetingsUrl + s.Id) 
        meetings = parser.ParseMeetingsFromXml(meetingsXml)
        meetingDocuments = parser.ParseMeetingDocumentsFromXml(meetingsXml)
        database.WriteToDatabase(meetings, 'Meetings', meetingMap, ['Id'], doUpdate)
        database.WriteToDatabase(meetingDocuments, 'MeetingDocuments', meetingDocumentMap, ['MeetingId', 'Url'])

        for m in meetings:

            if(is28DaysAgo(m) and allowToBreak):
                break

            agendaXml = resources.GetData(resources.agendaUrl + m.Id)

            agendas = parser.ParseAgendasFromXml(agendaXml, m.Id)
            agendaQuestions = parser.ParseAgendaQuestionsFromXml(agendaXml, m.Id)
            agendaQuestionSpeakers = parser.ParseAgendaQuestionSpeakersFromXml(agendaXml, m.Id)

            database.WriteToDatabase(agendas, 'Agendas', agendaMap, ['MeetingId', 'Number'], doUpdate)
            database.WriteToDatabase(agendaQuestions, 'AgendaQuestions', agendaQuestionMap, ['QuestionId', 'Number'], doUpdate)
            database.WriteToDatabase(agendaQuestionSpeakers, 'AgendaQuestionSpeakers', agendaQuestionSpeakerMap, ['MeetingId', 'Number', 'Person'], doUpdate)

            
            actualMeetingXml = resources.GetData(resources.meetingUrl + m.Id)

            meetingQuestions = parser.ParseMeetingQuestionsFromXml(actualMeetingXml, agendaQuestions)
            votings = parser.ParseVotingsFromXml(actualMeetingXml)
            database.WriteToDatabase(votings, 'Votings', votingMap, ['VotingId'], doUpdate)
            database.WriteToDatabase(meetingQuestions, 'MeetingQuestions', meetingQuestionMap, ['MeetingId', 'Number'], doUpdate)
            
            for v in votings:
                break
                if 'bendru sutarimu' in v.Description:
                    continue # skip votings if there was no actual voting

                votesXml = resources.GetData(resources.votingResultsUrl + v.VotingId)
                votes = parser.ParseVotesFromXml(votesXml)
                if len(list(filter(lambda x: x.Vote == 3, votes))) == len(votes):
                    continue # skip votings if there was no actual voting

                database.WriteToDatabase(votes, 'Votes', voteMap, ['VotingId', 'MemberId'])
                hhhhh = 5555

