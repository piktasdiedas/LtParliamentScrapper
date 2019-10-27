import sys
import xml.etree.ElementTree as xmlTree
from datetime import datetime
import pymysql #PyMySQL-0.9.3
from typing import *
import collections
import datetime
import re

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
            dateFrom = None if node.attrib["pradžia"] == '' else node.attrib["pradžia"]
            dateTo = None if node.attrib["pabaiga"] == '' else node.attrib["pabaiga"]
            
            if dateFrom is None and dateFrom is None:
                continue

            parsed.append(Meeting(Id = id, SessionId = sessionId, Type = type, From = dateFrom, To = dateTo))

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
        year = root.attrib['laikas_nuo'][0:10]
        currentQuestionGroupNr = None
        questionGroupStartTime = None
        questionGroupFinishTime = None

        for node in root:
            number = node.attrib["numeris"]
            number = self.fixAgendaNumber(number)
            name = self.fixQuotes(node.attrib['pavadinimas'])
            dateFrom = None if node.attrib["laikas_nuo"] == '' else year + " " + node.attrib["laikas_nuo"] + ':00'
            dateTo = None if node.attrib["laikas_iki"] == '' else year + " " + node.attrib["laikas_iki"] + ':00' 

            patern = '[a-zA-ZąĄčČęĘėĖįĮšŠųŲūŪžŽ]+'
            if len(number) != 0 and number[len(number) - 1].isalpha():
                startIndex = re.search(patern, number[1:]).start() + 1 if number[0] == 'r' else re.search(patern, number).start()
                nr = number[:startIndex]
                alpha = number[startIndex:len(number)]
                if alpha == 'a':
                    currentQuestionGroupNr = nr
                    questionGroupStartTime = dateFrom
                    questionGroupFinishTime = dateTo
                else:
                    if currentQuestionGroupNr == nr: 
                        dateFrom = questionGroupStartTime if dateFrom is None else dateFrom
                        dateTo = questionGroupFinishTime if dateTo is None else dateTo


                
            if '.' in number:
                nr = (number.split('.')[0].split('-')[1]) if '-' in number else number.split('.')[0]
                if number.split('.')[1] == '1':
                    currentQuestionGroupNr = nr
                    questionGroupStartTime = dateFrom
                    questionGroupFinishTime = dateTo
                else:
                    if currentQuestionGroupNr == nr:
                        dateFrom = questionGroupStartTime if dateFrom is None else dateFrom
                        dateTo = questionGroupFinishTime if dateTo is None else dateTo


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

                    number = self.fixAgendaNumber(number)
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

                    number = self.fixAgendaNumber(number)
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
            questionId = node.attrib['svarst_kl_stad_id']
            votings = node.find("balsavimai")
            for v in votings:
                votingId = v.attrib['bals_id']
                resolution = v.find('aprasas').text
                description = v.find('antraste').text
                
                parsed.append(Voting(VotingId = votingId, MeetingId = meetingId,  Resolution = resolution, Description = description, QuestionId = questionId))

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


    def ParseMeetingQuestionsFromXml(self, xml: str, agendaModels: List[AgendaQuestion]) -> List[MeetingQuestion]:
        parsed = []
        
        xmlFixed = self.fixXml(xml, id)

        xmlDom = xmlTree.fromstring(xmlFixed)
        root = xmlDom.find("posedis")
        meetingId = root.attrib['pos_id']
        root = root.find('posedzio-eiga')
        for node in root:
            meetingQuestionId = node.attrib['svarst_kl_stad_id']
            #agendaQuestionId = node.attrib['kl_stad_id'] if 'kl_stad_id' in node.attrib else None

            documentId = ''
            if 'dok_key' in node.attrib:
                documentId = node.attrib['dok_key']

            number = "" if node.find('nr') is None else node.find('nr').text
            number = self.fixAgendaNumber(number)

            name = "" if node.find('pavadinimas') is None else node.find('pavadinimas').text
            
            stage = ""
            if node.find('stadija') is not None:
                stage = node.find('stadija').text

            type = '' if node.find('tipas') is None else node.find('tipas').text

            dateFrom = node.find('nuo').text
            dateTo = dateFrom if node.find('iki') is None else node.find('iki').text

            questionGroupId = None
            numbers = []
            if 'kl_gr_id' in node.attrib:
                questionGroupId = node.attrib['kl_gr_id']
            numbers = number.split(",")

            for n in numbers:
                agendaQuestionId = node.attrib['kl_stad_id'] if 'kl_stad_id' in node.attrib else None
                if agendaQuestionId is None:
                    for a in agendaModels:
                        if a.Number == n:
                            agendaQuestionId = a.QuestionId
                            break

                if agendaQuestionId is None:
                    aaaaa = 8888


                parsed.append(MeetingQuestion(MeetingId = meetingId, MeetingQuestionId = meetingQuestionId, QuestionId = agendaQuestionId, Name = name, Stage = stage, Type = type, DocumentId = documentId, Number = n, From = dateFrom, To = dateTo, QuestionGroupId = questionGroupId))
            #else:
            #    parsed.append(MeetingQuestion(MeetingId = meetingId, MeetingQuestionId = meetingQuestionId, QuestionId = 0, Name = name, Stage = stage, Type = type, DocumentId = documentId, Number = number, From = dateFrom, To = dateTo, QuestionGroupId = questionGroupId))
        validDate = ''
        for p in parsed:
            try:
                datetime.datetime.strptime(getattr(p, "From"), '%Y-%m-%d %H:%M:%S')
                validDate = getattr(p, "From")[0:10]
                break
            except ValueError:
                pass
        parsedAndFixed = []
        for p in parsed:
            if len(getattr(p, "From")) < 10:
                oldFrom = getattr(p, "From")
                oldTo = getattr(p, "To")
                #p._replace(From = validDate + " " + oldFrom)
                #p._replace(To = validDate + " " + oldTo)
                n = MeetingQuestion(MeetingId = p.MeetingId, MeetingQuestionId = p.MeetingQuestionId, QuestionId = p.QuestionId, Name = p.Name, Stage = p.Stage, Type = p.Type, DocumentId = p.DocumentId, Number = p.Number, From = validDate + " " + oldFrom, To = validDate + " " + oldTo, QuestionGroupId = p.QuestionGroupId)
                parsedAndFixed.append(n)
            else:
                parsedAndFixed.append(p)


        return parsedAndFixed





    
      
    def ParseLegislationsFromXml(self, xml: str) -> List[InitiatedLegislation]:
        parsed = []
        
        xmlFixed = self.fixXml(xml, id)

        xmlDom = xmlTree.fromstring(xmlFixed)
        root = xmlDom.find("SeimoNarys")
        if root is None:
            return parsed

        memberId = root.attrib['asmens_id']
        for node in root:
            type = node.attrib["požymis"]
            registrationDate = node.attrib["registracijos_data"]
            registrationNumber = node.attrib["registracijos_numeris"]
            name = node.attrib["pavadinimas"]

            
            parsed.append(InitiatedLegislation(MemberId = memberId, Type = type,  RegistrationDate = registrationDate, RegistrationNumber = registrationNumber, Name = name))

        return parsed

   
    def ParseLegislationSuggestionsFromXml(self, xml: str) -> List[InitiatedLegislationSuggestion]:
        parsed = []
        
        xmlFixed = self.fixXml(xml, id)

        xmlDom = xmlTree.fromstring(xmlFixed)
        root = xmlDom.find("SeimoNarys")
        if root is None:
            return parsed

        memberId = root.attrib['asmens_id']
        for node in root:
            type = node.attrib["požymis"]
            registrationDate = node.attrib["registracijos_data"]
            registrationNumber = node.attrib["registracijos_numeris"]
            name = node.attrib["pavadinimas"]

            
            parsed.append(InitiatedLegislationSuggestion(MemberId = memberId, Type = type,  RegistrationDate = registrationDate, RegistrationNumber = registrationNumber, Name = name))

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
        temp = text.replace('„', '"').replace('”', '"').replace('„', '"').replace('“', '"').replace('quot;', '"').replace('&;', '').replace('&', '')
        return temp
    
    def fixAgendaNumber(self, text: str) -> str:
        temp = text.replace("'", '"').replace(" ", "")

        
        if len(temp) == 0:
            return temp

        if temp[-1] == '.':
            strLen = len(temp) - 1
            temp = temp[0 : strLen]

        return temp
