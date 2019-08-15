import urllib.request
import sys
import xml.etree.ElementTree as xmlTree
from datetime import datetime
import pymysql #PyMySQL-0.9.3
from typing import *
import collections
from datetime import datetime

from Models import *
from ParlamentResources import *
from SimpleBenchmarkToConsole import *
from DatabaseConnector import *


def ParseVotesFromXml(xml: str) -> str:
    xmlDom = xmlTree.fromstring(xml)
    votes = xmlDom.find("SeimoNariųBalsavimas")
    for node in votes:
        if node.tag == "BendriBalsavimoRezultatai":
            approved = "Taip" if (node.attrib["už"] > node.attrib["prieš"]) else "NE"
            print(node.attrib["viso"] + " --> " + approved)
        elif node.tag == "IndividualusBalsavimoRezultatas":
             print(node.attrib['pavardė'] + " " + node.attrib['vardas'] + " --> ")



def ParseMembersFromXml(xml: str) -> List[Member]:
    parsed = []

    xmlDom = xmlTree.fromstring(xml)
    root = xmlDom.find("SeimoKadencija")
    for node in root:
        id = node.attrib["asmens_id"]
        firstName = node.attrib["vardas"]
        lastName = node.attrib["pavardė"]
        bioUrl = node.attrib["biografijos_nuoroda"] if 'biografijos_nuoroda' in node.attrib else ''
        email = ""
        for child in node:
            if child.tag == "Kontaktai":
                email = child.attrib["reikšmė"] if child.attrib["rūšis"] == "El. p." else email
            
        parsed.append(Member(Id = id, FirstName = firstName, LastName = lastName, Email = email, BioUrl = bioUrl))

    return parsed




def ParseTermOfOfficeMembersFromXml(xml: str) -> List[TermOfOfficeMember]:
    parsed = []

    xmlDom = xmlTree.fromstring(xml)
    root = xmlDom.find("SeimoKadencija")
    termOfOfficeId = root.attrib['kadencijos_id']
    for node in root:
        memberId = node.attrib["asmens_id"]
        dateFrom = None if node.attrib["data_nuo"] == '' else node.attrib["data_nuo"] 
        dateTo = None if node.attrib["data_iki"] == '' else node.attrib["data_iki"] 
        party = node.attrib["iškėlusi_partija"] if 'iškėlusi_partija' in node.attrib else ''
            
        parsed.append(TermOfOfficeMember(TermOfOfficeId = termOfOfficeId, MemberId = memberId, From = dateFrom, To = dateTo, Party = party))

    return parsed





def ParseSessionsFromXml(xml: str) -> List[Session]:
    parsedSessions = []

    xmlDom = xmlTree.fromstring(xml)
    root = xmlDom.find("SeimoKadencija")
    for root in xmlDom: 
        cadencyId = root.attrib["kadencijos_id"]
        for node in root:
            sessionId = node.attrib["sesijos_id"]
            name = node.attrib["pavadinimas"]
            dateFrom = node.attrib["data_nuo"]
            dateTo = None if node.attrib["data_iki"] == '' else node.attrib["data_iki"]
        
            parsedSessions.append(Session(Id = sessionId, Name = name, From = dateFrom, To = dateTo, TermOfOffice = cadencyId))

    return parsedSessions


def ParseCommisionsFromXml(xml: str) -> List[Commission]:
    parsed = []

    xmlDom = xmlTree.fromstring(xml)
    root = xmlDom.find("SeimoKadencija")
    for node in root:
        id = node.attrib["padalinio_id"]
        name = node.attrib["padalinio_pavadinimas"]
        
        parsed.append(Commission(Id = id, Name = name))

    return parsed



def ParseFactionsFromXml(xml: str) -> List[Faction]:
    parsed = []

    xmlDom = xmlTree.fromstring(xml)
    root = xmlDom.find("SeimoKadencija")
    for node in root:
        id = node.attrib["padalinio_id"]
        name = node.attrib["padalinio_pavadinimas"]
        shortName = node.attrib["padalinio_pavadinimo_santrumpa"]
        
        parsed.append(Faction(Id = id, Name = name, ShortName = shortName))

    return parsed



def ParseTermOfOfficeFromXml(xml: str) -> List[TermOfOffice]:
    parsed = []

    xmlDom = xmlTree.fromstring(xml)
    root = xmlDom
    for node in root:
        id = node.attrib["kadencijos_id"]
        name = node.attrib["pavadinimas"]
        dateFrom = node.attrib["data_nuo"]
        dateTo = None if node.attrib["data_iki"] == '' else node.attrib["data_iki"]
        
        parsed.append(TermOfOffice(Id = id, Name = name, From = dateFrom, To = dateTo))

    return parsed




def ParseMeetingsFromXml(xml: str) -> List[Meeting]:
    parsed = []

    xmlDom = xmlTree.fromstring(xml)
    root = xmlDom.find('SeimoSesija')
    sessionId = root.attrib['sesijos_id']
    for node in root:
        id = node.attrib["posėdžio_id"]
        type = node.attrib["tipas"]
        dateFrom = node.attrib["pradžia"]
        dateTo = node.attrib["pabaiga"]
        protocol = ''
        stenogram = ''
        video = ''

        for child in node:
            if child.tag == "Protokolas":
                protocol = child.attrib["protokolo_nuoroda"] if 'protokolo_nuoroda' in child.attrib else protocol
            if child.tag == "Stenograma":
                stenogram = child.attrib["stenogramos_nuoroda"] if 'stenogramos_nuoroda' in child.attrib else stenogram
            if child.tag == "VaizdoĮrašas":
                video = child.attrib["vaizdo_įrašo_nuoroda"] if 'vaizdo_įrašo_nuoroda' in child.attrib else video

        
        parsed.append(Meeting(Id = id, SessionId = sessionId, Type = type, From = dateFrom, To = dateTo, Protocol = protocol, Stenogram = stenogram, Video = video))

    return parsed



def ParseCommitteesFromXml(xml: str) -> List[Committee]:
    parsed = []

    xmlDom = xmlTree.fromstring(xml)
    root = xmlDom.find("SeimoKadencija")
    for node in root:
        id = node.attrib["padalinio_id"]
        name = node.attrib["padalinio_pavadinimas"]
        
        parsed.append(Commission(Id = id, Name = name))

    return parsed

#####
def ParseCommitteesFromXmlFromMembers(xml: str) -> List[Committee]:
    parsed = []
    
    xmlDom = xmlTree.fromstring(xml)
    root = xmlDom.find("SeimoKadencija")
    for node in root:
        for nodeChild in node:
            if nodeChild.tag == 'Pareigos':
                if 'padalinio_pavadinimas' in nodeChild.attrib and ('komitet' in nodeChild.attrib['pareigos'].lower()):
                    id = nodeChild.attrib['padalinio_id']
                    name = nodeChild.attrib['padalinio_pavadinimas']
                    parsed.append(Committee(Id = id, Name = name))

    return parsed


def ParseCommitteeMembersFromXmlFromMembers(xml: str) -> List[CommitteeMember]:
    parsed = []
    
    xmlDom = xmlTree.fromstring(xml)
    root = xmlDom.find("SeimoKadencija")
    for node in root:
        for nodeChild in node:
            if nodeChild.tag == 'Pareigos':
                if 'padalinio_pavadinimas' in nodeChild.attrib and ('komitet' in nodeChild.attrib['pareigos'].lower()):
                    memberId = node.attrib["asmens_id"]
                    committeeId = nodeChild.attrib['padalinio_id']
                    dateFrom = None if nodeChild.attrib["data_nuo"] == '' else nodeChild.attrib["data_nuo"] 
                    dateTo = None if nodeChild.attrib["data_iki"] == '' else nodeChild.attrib["data_iki"] 
                    position = nodeChild.attrib['pareigos']

                    parsed.append(CommitteeMember(CommitteeId = committeeId, MemberId = memberId, From = dateFrom, To = dateTo, Position = position))

    return parsed


#####
def ParseCommissionsFromXmlFromMembers(xml: str) -> List[Commission]:
    parsed = []
    
    xmlDom = xmlTree.fromstring(xml)
    root = xmlDom.find("SeimoKadencija")
    for node in root:
        for nodeChild in node:
            if nodeChild.tag == 'Pareigos':
                if 'padalinio_pavadinimas' in nodeChild.attrib and ('komisij' in nodeChild.attrib['pareigos'].lower()):
                    id = nodeChild.attrib['padalinio_id']
                    name = nodeChild.attrib['padalinio_pavadinimas']
                    parsed.append(Commission(Id = id, Name = name))

    return parsed


def ParseCommissionMembersFromXmlFromMembers(xml: str) -> List[CommissionMember]:
    parsed = []
    
    xmlDom = xmlTree.fromstring(xml)
    root = xmlDom.find("SeimoKadencija")
    for node in root:
        for nodeChild in node:
            if nodeChild.tag == 'Pareigos':
                if 'padalinio_pavadinimas' in nodeChild.attrib and ('komisij' in nodeChild.attrib['pareigos'].lower()):
                    memberId = node.attrib["asmens_id"]
                    commissionId = nodeChild.attrib['padalinio_id']
                    dateFrom = None if nodeChild.attrib["data_nuo"] == '' else nodeChild.attrib["data_nuo"] 
                    dateTo = None if nodeChild.attrib["data_iki"] == '' else nodeChild.attrib["data_iki"] 
                    position = nodeChild.attrib['pareigos']

                    parsed.append(CommissionMember(CommissionId = commissionId, MemberId = memberId, From = dateFrom, To = dateTo, Position = position))

    return parsed



#####
def ParseFactionsFromXmlFromMembers(xml: str) -> List[Faction]:
    parsed = []
    
    xmlDom = xmlTree.fromstring(xml)
    root = xmlDom.find("SeimoKadencija")
    for node in root:
        for nodeChild in node:
            if nodeChild.tag == 'Pareigos':
                if 'padalinio_pavadinimas' in nodeChild.attrib and ('frakcij' in nodeChild.attrib['pareigos'].lower()):
                    id = nodeChild.attrib['padalinio_id']
                    name = nodeChild.attrib['padalinio_pavadinimas']
                    parsed.append(Faction(Id = id, Name = name, ShortName = ''))

    return parsed


def ParseFactionMembersFromXmlFromMembers(xml: str) -> List[FactionMember]:
    parsed = []
    
    xmlDom = xmlTree.fromstring(xml)
    root = xmlDom.find("SeimoKadencija")
    for node in root:
        for nodeChild in node:
            if nodeChild.tag == 'Pareigos':
                if 'padalinio_pavadinimas' in nodeChild.attrib and ('frakcij' in nodeChild.attrib['pareigos'].lower()):
                    memberId = node.attrib["asmens_id"]
                    factionId = nodeChild.attrib['padalinio_id']
                    dateFrom = None if nodeChild.attrib["data_nuo"] == '' else nodeChild.attrib["data_nuo"] 
                    dateTo = None if nodeChild.attrib["data_iki"] == '' else nodeChild.attrib["data_iki"] 
                    position = nodeChild.attrib['pareigos']

                    parsed.append(FactionMember(FactionId = factionId, MemberId = memberId, From = dateFrom, To = dateTo, Position = position))

    return parsed



#####
def ParseParlamentGroupsFromXmlFromMembers(xml: str) -> List[ParlamentGroup]:
    parsed = []
    
    xmlDom = xmlTree.fromstring(xml)
    root = xmlDom.find("SeimoKadencija")
    for node in root:
        for nodeChild in node:
            if nodeChild.tag == 'Pareigos':
                if 'parlamentinės_grupės_pavadinimas' in nodeChild.attrib:
                    id = nodeChild.attrib['parlamentinės_grupės_id']
                    name = nodeChild.attrib['parlamentinės_grupės_pavadinimas']
                    parsed.append(ParlamentGroup(Id = id, Name = name))

    return parsed


def ParseParlamentGroupMembersFromXmlFromMembers(xml: str) -> List[ParlamentGroupMember]:
    parsed = []
    
    xmlDom = xmlTree.fromstring(xml)
    root = xmlDom.find("SeimoKadencija")
    for node in root:
        for nodeChild in node:
            if nodeChild.tag == 'Pareigos':
                if 'parlamentinės_grupės_pavadinimas' in nodeChild.attrib:
                    memberId = node.attrib["asmens_id"]
                    parlamentGroupId = nodeChild.attrib['parlamentinės_grupės_id']
                    dateFrom = None if nodeChild.attrib["data_nuo"] == '' else nodeChild.attrib["data_nuo"] 
                    dateTo = None if nodeChild.attrib["data_iki"] == '' else nodeChild.attrib["data_iki"] 
                    position = nodeChild.attrib['pareigos']

                    parsed.append(ParlamentGroupMember(ParlamentGroupId = parlamentGroupId, MemberId = memberId, From = dateFrom, To = dateTo, Position = position))

    return parsed


def main(): 
    database = DatabaseConnector()

    currentTermOfOfficeStart = 0
    def shouldUpdateDelegate(obj):
        d = datetime.datetime.strptime(obj.From, '%Y-%m-%d').date()
        return d >= currentTermOfOfficeStart
 

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
    currentTermOfOfficeStart = database.ExecuteRawSingle('SELECT `From` FROM TermOfOffice ORDER BY Id DESC LIMIT 1')
    resources = ParlamentResources()
    print(ParlamentResources.membersUrl)
    print(resources.membersUrl)
    
    termOfOfficeXml = resources.GetData(resources.termsOfOfficeUrl)
    termOfOffice = ParseTermOfOfficeFromXml(termOfOfficeXml)
    termOfOffice.reverse()
    for t in termOfOffice:
        if t.Id == '2' or t.Id == '1':
            continue
        membersXml = resources.GetData('seimo_nariai?kadencijos_id=' + str(t.Id))
        members = ParseMembersFromXml(membersXml)
        memberIndex = 0
        #for m in members:
        committees = ParseCommitteesFromXmlFromMembers(membersXml)
        committeeMembers = ParseCommitteeMembersFromXmlFromMembers(membersXml)

        commissions = ParseCommissionsFromXmlFromMembers(membersXml)
        commissionMembers = ParseCommissionMembersFromXmlFromMembers(membersXml)

        factions = ParseFactionsFromXmlFromMembers(membersXml)
        factionMembers = ParseFactionMembersFromXmlFromMembers(membersXml)

        parlamentGroups = ParseParlamentGroupsFromXmlFromMembers(membersXml)
        parlamentGroupMembers = ParseParlamentGroupMembersFromXmlFromMembers(membersXml)

        database.WriteToDatabase(committees, 'Committees', committeeMap, ['Id'])
        database.WriteToDatabase(commissions, 'Commissions', commissionMap, ['Id'])
        database.WriteToDatabase(factions, 'Factions', factionMap, ['Id'])
        database.WriteToDatabase(parlamentGroups, 'ParlamentGroups', parlamentGroupMap, ['Id'])
        database.WriteToDatabase(committeeMembers, 'CommitteeMembers', committeeMemberMap, ['MemberId', 'CommitteeId', 'From'], shouldUpdateDelegate)
        database.WriteToDatabase(commissionMembers, 'CommissionMembers', commissionMemberMap, ['MemberId', 'CommissionId', 'From'], shouldUpdateDelegate)
        database.WriteToDatabase(factionMembers, 'FactionMembers', factionMemberMap, ['MemberId', 'FactionId', 'From'], shouldUpdateDelegate)
        database.WriteToDatabase(parlamentGroupMembers, 'ParlamentGroupMembers', parlamentGroupMemberMap, ['MemberId', 'ParlamentGroupId', 'From'], shouldUpdateDelegate)

        print('-----')
        print(f'Member index - {memberIndex}')
        memberIndex = memberIndex + 1

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
        


