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
AgendaQuestionSpeaker = collections.namedtuple('AgendaQuestionSpeakers', ' '.join(agendaQuestionSpeakersMap.keys()))



