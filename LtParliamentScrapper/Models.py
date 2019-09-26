from typing import *
import collections


termOfOfficeMap = collections.OrderedDict([('Id', 'Id'), ('Name', 'Name'), ('From', 'From'), ('To', 'To')])
TermOfOffice = collections.namedtuple('TermOfOffice', ' '.join(termOfOfficeMap.keys()))

sessionMap = collections.OrderedDict([('Id', 'Id'), ('From', 'From'), ('To', 'To'), ('TermOfOffice', 'TermOfOffice'), ('Name', 'Name')])
Session = collections.namedtuple('Session', ' '.join(sessionMap.keys()))


memberMap = collections.OrderedDict([('Id', 'Id'), ('FirstName', 'FirstName'), ('LastName', 'LastName'), ('Email', 'Email'), ('BioUrl', 'BioUrl')])
Member = collections.namedtuple('Member', ' '.join(memberMap.keys()))


termOfOfficeMemberMap = collections.OrderedDict([('TermOfOfficeId', 'TermOfOfficeId'), ('MemberId', 'MemberId'), ('Party', 'Party'), ('From', 'From'), ('To', 'To')])
TermOfOfficeMember = collections.namedtuple('TermOfOfficeMember', ' '.join(termOfOfficeMemberMap.keys()))


meetingMap = collections.OrderedDict([('Id', 'Id'), ('SessionId', 'SessionId'), ('Type', 'Type'), ('From', 'From'), ('To', 'To'), ('Protocol', 'Protocol'), ('Stenogram', 'Stenogram'), ('Video', 'Video')])
Meeting = collections.namedtuple('Meeting', ' '.join(meetingMap.keys()))


meetingDocumentMap = collections.OrderedDict([('MeetingId', 'MeetingId'), ('Type', 'Type'), ('TypeName', 'TypeName'), ('Url', 'Url')])
MeetingDocument = collections.namedtuple('MeetingDocument', ' '.join(meetingDocumentMap.keys()))





committeeMap = collections.OrderedDict([('Id', 'Id'), ('Name', 'Name')])
Committee = collections.namedtuple('Committee', ' '.join(committeeMap.keys()))

committeeMemberMap = collections.OrderedDict([('CommitteeId', 'CommitteeId'), ('MemberId', 'MemberId'), ('From', 'From'), ('To', 'To'), ('Position', 'Position')])
CommitteeMember = collections.namedtuple('CommitteeMember', ' '.join(committeeMemberMap.keys()))


commissionMap = collections.OrderedDict([('Id', 'Id'), ('Name', 'Name')])
Commission = collections.namedtuple('Commission', ' '.join(commissionMap.keys()))

commissionMemberMap = collections.OrderedDict([('CommissionId', 'CommissionId'), ('MemberId', 'MemberId'), ('From', 'From'), ('To', 'To'), ('Position', 'Position')])
CommissionMember = collections.namedtuple('CommissionMember', ' '.join(commissionMemberMap.keys()))


factionMap = collections.OrderedDict([('Id', 'Id'), ('Name', 'Name'), ('ShortName', 'ShortName')])
Faction = collections.namedtuple('Faction', ' '.join(factionMap.keys()))

factionMemberMap = collections.OrderedDict([('FactionId', 'FactionId'), ('MemberId', 'MemberId'), ('From', 'From'), ('To', 'To'), ('Position', 'Position')])
FactionMember = collections.namedtuple('FactionMember', ' '.join(factionMemberMap.keys()))


parlamentGroupMap = collections.OrderedDict([('Id', 'Id'), ('Name', 'Name')])
ParlamentGroup = collections.namedtuple('ParlamentGroup', ' '.join(parlamentGroupMap.keys()))

parlamentGroupMemberMap = collections.OrderedDict([('ParlamentGroupId', 'ParlamentGroupId'), ('MemberId', 'MemberId'), ('From', 'From'), ('To', 'To'), ('Position', 'Position')])
ParlamentGroupMember = collections.namedtuple('ParlamentGroupMember', ' '.join(parlamentGroupMemberMap.keys()))



agendaMap = collections.OrderedDict([('MeetingId', 'MeetingId'), ('Name', 'Name'), ('Number', 'Number'), ('From', 'From'), ('To', 'To')])
Agenda = collections.namedtuple('Agenda', ' '.join(agendaMap.keys()))

agendaQuestionMap = collections.OrderedDict([('QuestionId', 'QuestionId'), ('MeetingId', 'MeetingId'), ('Stage', 'Stage'), ('DocumentUrl', 'DocumentUrl'), ('Number', 'Number')])
AgendaQuestion = collections.namedtuple('AgendaQuestion', ' '.join(agendaQuestionMap.keys()))

agendaQuestionSpeakerMap = collections.OrderedDict([('MeetingId', 'MeetingId'), ('Person', 'Person'), ('Position', 'Position'), ('Number', 'Number')])
AgendaQuestionSpeaker = collections.namedtuple('AgendaQuestionSpeakers', ' '.join(agendaQuestionSpeakerMap.keys()))




meetingQuestionMap = collections.OrderedDict([('MeetingQuestionId', 'MeetingQuestionId'), ('QuestionId', 'QuestionId'), ('MeetingId', 'MeetingId'), ('Name', 'Name'), ('Stage', 'Stage'), ('Type', 'Type'), ('DocumentId', 'DocumentId'), ('Number', 'Number'), ('From', 'From'), ('To', 'To')])
MeetingQuestion = collections.namedtuple('MeetingQuestion', ' '.join(meetingQuestionMap.keys()))

votingMap = collections.OrderedDict([('VotingId', 'VotingId'), ('MeetingId', 'MeetingId'), ('Resolution', 'Resolution'), ('Description', 'Description')])
Voting = collections.namedtuple('Vote', ' '.join(votingMap.keys()))

voteMap = collections.OrderedDict([('VotingId', 'VotingId'), ('MemberId', 'MemberId'), ('Vote', 'Vote'), ('DateOn', 'DateOn')])
Vote = collections.namedtuple('Vote', ' '.join(votegMap.keys()))



registrationMap = collections.OrderedDict([('RegistrationId', 'RegistrationId'), ('MeetingId', 'MeetingId'), ('From', 'From'), ('TotalRegistered', 'TotalRegistered')])
Registration = collections.namedtuple('Vote', ' '.join(registrationMap.keys()))


userRegistrationMap = collections.OrderedDict([('RegistrationId', 'RegistrationId'), ('MemberId', 'MemberId'), ('HasRegistered', 'HasRegistered'), ('DateOn', 'DateOn')])
UserRegistration = collections.namedtuple('Registration', ' '.join(userRegistrationMap.keys()))



meetingQuestionSpeakerMap = collections.OrderedDict([('MeetingId', 'MeetingId'), ('Person', 'Person'), ('PersonId', 'PersonId'), ('DiscussionId', 'DiscussionId'), ('Position', 'Position'), ('Number', 'Number'), ('From', 'From'), ('To', 'To')])
MeetingQuestionSpeaker = collections.namedtuple('MeetingQuestionSpeaker', ' '.join(meetingQuestionSpeakerMap.keys()))
