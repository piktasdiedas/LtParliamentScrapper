import sys
import xml.etree.ElementTree as xmlTree
from datetime import datetime
import pymysql #PyMySQL-0.9.3
from typing import *
import collections

from Models import *

class XmlParser:

    #def ParseVotesFromXml(self, xml: str) -> str:
    #    xmlDom = xmlTree.fromstring(xml)
    #    votes = xmlDom.find("SeimoNariųBalsavimas")
    #    for node in votes:
    #        if node.tag == "BendriBalsavimoRezultatai":
    #            approved = "Taip" if (node.attrib["už"] > node.attrib["prieš"]) else "NE"
    #            print(node.attrib["viso"] + " --> " + approved)
    #        elif node.tag == "IndividualusBalsavimoRezultatas":
    #             print(node.attrib['pavardė'] + " " + node.attrib['vardas'] + " --> ")



    def ParseMembersFromXml(self, xml: str) -> List[Member]:
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




    def ParseTermOfOfficeMembersFromXml(self, xml: str) -> List[TermOfOfficeMember]:
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





    def ParseSessionsFromXml(self, xml: str) -> List[Session]:
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


    def ParseCommisionsFromXml(self, xml: str) -> List[Commission]:
        parsed = []

        xmlDom = xmlTree.fromstring(xml)
        root = xmlDom.find("SeimoKadencija")
        for node in root:
            id = node.attrib["padalinio_id"]
            name = node.attrib["padalinio_pavadinimas"]
        
            parsed.append(Commission(Id = id, Name = name))

        return parsed



    def ParseFactionsFromXml(self, xml: str) -> List[Faction]:
        parsed = []

        xmlDom = xmlTree.fromstring(xml)
        root = xmlDom.find("SeimoKadencija")
        for node in root:
            id = node.attrib["padalinio_id"]
            name = self.fixQuotes(node.attrib["padalinio_pavadinimas"])
            shortName = node.attrib["padalinio_pavadinimo_santrumpa"]
        
            parsed.append(Faction(Id = id, Name = name, ShortName = shortName))

        return parsed



    def ParseTermOfOfficeFromXml(self, xml: str) -> List[TermOfOffice]:
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




    def ParseMeetingsFromXml(self, xml: str) -> List[Meeting]:
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

            parsed.append(Meeting(Id = id, SessionId = sessionId, Type = type, From = dateFrom, To = dateTo, Protocol = protocol, Stenogram = stenogram, Video = video))

        return parsed
    
    


    def ParseMeetingDocumentsFromXml(self, xml: str) -> List[Meeting]:
        parsed = []

        xmlDom = xmlTree.fromstring(xml)
        root = xmlDom.find('SeimoSesija')
        #root = root.find('SeimoPosėdis')
        sessionId = root.attrib['sesijos_id']
        for node in root:
            meetingId = node.attrib["posėdžio_id"]
            type = 0
            typeName = ''
            url = ''

            for child in node:
                if child.tag == "Protokolas":
                    url = child.attrib["protokolo_nuoroda"] if 'protokolo_nuoroda' in child.attrib else ''
                    type = 1
                    typeName = 'protocol'
                if child.tag == "Stenograma":
                    url = child.attrib["stenogramos_nuoroda"] if 'stenogramos_nuoroda' in child.attrib else ''
                    type = 2
                    typeName = 'stenogram'
                if child.tag == "VaizdoĮrašas":
                    url = child.attrib["vaizdo_įrašo_nuoroda"] if 'vaizdo_įrašo_nuoroda' in child.attrib else ''
                    type = 3
                    typeName = 'video'

        
                parsed.append(MeetingDocument(MeetingId = meetingId,Type = type, TypeName = typeName, Url = url))

        return parsed
    


    def ParseCommitteesFromXml(self, xml: str) -> List[Committee]:
        parsed = []

        xmlDom = xmlTree.fromstring(xml)
        root = xmlDom.find("SeimoKadencija")
        for node in root:
            id = node.attrib["padalinio_id"]
            name = self.fixQuotes(node.attrib["padalinio_pavadinimas"])
        
            parsed.append(Commission(Id = id, Name = name))

        return parsed

    #####
    def ParseCommitteesFromXmlFromMembers(self, xml: str) -> List[Committee]:
        parsed = []
    
        xmlDom = xmlTree.fromstring(xml)
        root = xmlDom.find("SeimoKadencija")
        for node in root:
            for nodeChild in node:
                if nodeChild.tag == 'Pareigos':
                    if 'padalinio_pavadinimas' in nodeChild.attrib and ('komitet' in nodeChild.attrib['pareigos'].lower()):
                        id = nodeChild.attrib['padalinio_id']
                        name = self.fixQuotes(nodeChild.attrib['padalinio_pavadinimas'])
                        parsed.append(Committee(Id = id, Name = name))

        return parsed


    def ParseCommitteeMembersFromXmlFromMembers(self, xml: str) -> List[CommitteeMember]:
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
    def ParseCommissionsFromXmlFromMembers(self, xml: str) -> List[Commission]:
        parsed = []
    
        xmlDom = xmlTree.fromstring(xml)
        root = xmlDom.find("SeimoKadencija")
        for node in root:
            for nodeChild in node:
                if nodeChild.tag == 'Pareigos':
                    if 'padalinio_pavadinimas' in nodeChild.attrib and ('komisij' in nodeChild.attrib['pareigos'].lower()):
                        id = nodeChild.attrib['padalinio_id']
                        name = self.fixQuotes(nodeChild.attrib['padalinio_pavadinimas'])
                        parsed.append(Commission(Id = id, Name = name))

        return parsed


    def ParseCommissionMembersFromXmlFromMembers(self, xml: str) -> List[CommissionMember]:
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
    def ParseFactionsFromXmlFromMembers(self, xml: str) -> List[Faction]:
        parsed = []
    
        xmlDom = xmlTree.fromstring(xml)
        root = xmlDom.find("SeimoKadencija")
        for node in root:
            for nodeChild in node:
                if nodeChild.tag == 'Pareigos':
                    if 'padalinio_pavadinimas' in nodeChild.attrib and ('frakcij' in nodeChild.attrib['pareigos'].lower()):
                        id = nodeChild.attrib['padalinio_id']
                        name = self.fixQuotes(nodeChild.attrib['padalinio_pavadinimas'])
                        parsed.append(Faction(Id = id, Name = name, ShortName = ''))

        return parsed


    def ParseFactionMembersFromXmlFromMembers(self, xml: str) -> List[FactionMember]:
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
    def ParseParlamentGroupsFromXmlFromMembers(self, xml: str) -> List[ParlamentGroup]:
        parsed = []
    
        xmlDom = xmlTree.fromstring(xml)
        root = xmlDom.find("SeimoKadencija")
        for node in root:
            for nodeChild in node:
                if nodeChild.tag == 'Pareigos':
                    if 'parlamentinės_grupės_pavadinimas' in nodeChild.attrib:
                        id = nodeChild.attrib['parlamentinės_grupės_id']
                        name = self.fixQuotes(nodeChild.attrib['parlamentinės_grupės_pavadinimas'])
                        parsed.append(ParlamentGroup(Id = id, Name = name))

        return parsed


    def ParseParlamentGroupMembersFromXmlFromMembers(self, xml: str) -> List[ParlamentGroupMember]:
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


    def ParseAgendasFromXml(self, xml: str, id = 0) -> List[Agenda]:
        parsed = []
        xmlFixed = self.fixXml(xml, id)

        xmlDom = xmlTree.fromstring(xmlFixed)
        root = xmlDom.find("SeimoPosėdis")
        meetingId = root.attrib['posėdžio_id']
        for node in root:
            number = node.attrib["numeris"]
            name = self.fixQuotes(node.attrib['pavadinimas'])
            dateFrom = None if node.attrib["laikas_nuo"] == '' else node.attrib["laikas_nuo"] 
            dateTo = None if node.attrib["laikas_iki"] == '' else node.attrib["laikas_iki"] 

            parsed.append(Agenda(MeetingId = meetingId, Name = name,  Number = number, From = dateFrom, To = dateTo))

        return parsed

    

    def ParseAgendaQuestionsFromXml(self, xml: str, id = 0) -> List[AgendaQuestion]:
        parsed = []
        xmlFixed = self.fixXml(xml, id)
    
        xmlDom = xmlTree.fromstring(xmlFixed)
        root = xmlDom.find("SeimoPosėdis")
        meetingId = root.attrib['posėdžio_id']
        for node in root:
            number = node.attrib["numeris"]
            name = self.fixQuotes(node.attrib['pavadinimas'])
            for nodeChild in node:
                if nodeChild.tag == 'KlausimoStadija':
                    questionId = nodeChild.attrib['darbotvarkės_klausimo_id']
                    stage = nodeChild.attrib['pavadinimas']
                    url = nodeChild.attrib['dokumento_nuoroda']

                    #print(f"{number} {stage} -- {name} -- {questionId}")
                    parsed.append(AgendaQuestion(MeetingId = meetingId, QuestionId = questionId,  Number = number, Stage = stage, DocumentUrl = url))

        return parsed
    
    def ParseAgendaQuestionSpeakersFromXml(self, xml: str, id = 0) -> List[AgendaQuestionSpeaker]:
        parsed = []
        
        xmlFixed = self.fixXml(xml, id)

        xmlDom = xmlTree.fromstring(xmlFixed)
        root = xmlDom.find("SeimoPosėdis")
        meetingId = root.attrib['posėdžio_id']
        for node in root:
            number = node.attrib["numeris"]
            for nodeChild in node:
                if nodeChild.tag == 'KlausimoPranešėjas':
                    person = nodeChild.attrib['asmuo']
                    position = nodeChild.attrib['pareigos']

                    #print(f"{number}. {person} -- {position}")
                    parsed.append(AgendaQuestionSpeaker(MeetingId = meetingId,  Person = person, Position = position, Number = number))

        return parsed



    
    
    def ParseVotingsFromXml(self, xml: str) -> List[Voting]:
        parsed = []
        
        xmlFixed = self.fixXml(xml, id)

        xmlDom = xmlTree.fromstring(xmlFixed)
        root = xmlDom.find("posedis")
        meetingId = root.attrib['pos_id']
        root = root.find('posedzio-eiga')
        for node in root:
            votings = node.find("balsavimai")
            for v in votings:
                votingId = v.attrib['bals_id']
                resolution = v.find('aprasas').text
                description = v.find('antraste').text
                
                parsed.append(Voting(VotingId = votingId, MeetingId = meetingId,  Resolution = resolution, Description = description,))

        return parsed


    
    
    def ParseVotesFromXml(self, xml: str) -> List[Vote]:
        parsed = []
        
        xmlFixed = self.fixXml(xml, id)

        xmlDom = xmlTree.fromstring(xmlFixed)
        root = xmlDom.find("SeimoNariųBalsavimas")
        votingId = root.attrib['balsavimo_id']
        for node in root:
            if node.tag == 'BendriBalsavimoRezultatai':
                dateOn = node.attrib['balsavimo_laikas']

            if node.tag == 'IndividualusBalsavimoRezultatas':
                memberId = node.attrib['asmens_id']
                voteStr = node.attrib['kaip_balsavo']
                vote = 0 if voteStr.lower() == 'prieš' else\
                   1 if voteStr.lower() == 'už' else\
                   2 if voteStr.lower() == 'susilaikė' else\
                   3 if voteStr.lower() == '' else -1
                if vote == -1:
                    raise Exception('Unknown voting status', 'Vote')
                parsed.append(Vote(VotingId = votingId, MemberId = memberId, Vote = vote, VoteStr = voteStr, DateOn = dateOn))

        return parsed



    def ParseRegistrationFromXml(self, xml: str) -> List[Registration]:
        parsed = []
        
        xmlFixed = self.fixXml(xml, id)

        xmlDom = xmlTree.fromstring(xmlFixed)
        root = xmlDom.find("SeimoNariųBalsavimas")
        votingId = root.attrib['balsavimo_id']
        for node in root:
            if node.tag == 'BendriBalsavimoRezultatai':
                dateOn = node.attrib['balsavimo_laikas']

            if node.tag == 'IndividualusBalsavimoRezultatas':
                memberId = node.attrib["asmens_id"]
                vote = node.attrib['kaip_balsavo']
                parsed.append(Registration(VotingId = votingId, MemberId = memberId, Vote = vote, DateOn = dateOn))

        return parsed










    def fixXml(self, xml: str, id = 0) -> str:
        temp = xml

        if id == '-501249' or id == -501249:
            temp = temp.replace('"Žemaičių legiono"', '„Žemaičių legiono”')
            temp = temp.replace('"Misija Sibiras”', '„Misija Sibiras')

        if id == '-500481' or id == -500481:
            temp = temp.replace('judėjimo "Černobylis" pirmininkas', 'judėjimo „Černobylis” pirmininkas')

        return temp

    def fixQuotes(self, text: str) -> str:
        temp = text.replace('„', '"').replace('”', '"').replace('„', '"').replace('quot;', '"')
        return temp
