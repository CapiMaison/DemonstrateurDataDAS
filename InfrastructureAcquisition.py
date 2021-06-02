""" Created by Guillaume WELLER on 04/05/2021 """
""" Last modifications on 04/05/2021 by Guillaume WELLER """

######### ######### ######### ######### ####9#### ######### ######### ######### #########

##########################
### Modules à importer ###
##########################

import os
import lxml.etree
import pickle
import xlrd
from Classes import Debug



##########################
### Début du programme ###
##########################



class Infrastructure :
    """ Classe permettant de stocker toutes les différentes informations de l'infrastructure du RFN contenues dans SIPH """

    def __init__(self) :

        self.debug = Debug()
        self.rootPath = os.getcwd()
        self.tree = lxml.etree.parse(self.rootPath + r"\Infrastructure\REFI-2021-V8.7.1_PUB.xml")
        self.vitessesVoies = {}
        self.gradientsVoies = {}
        self.radiusesVoies = {}
        self.signauxVoies = {}
        self.electrificationVoies = {}
        #self.acquisitionSignauxSpeedIndicators()
        #print(self.chargementSignauxSpeedIndicators())


    def acquisitionVitessesVoies(self) :
        self.vitesseInfrastructure = self.tree.xpath("/infrastructure/profiles/speedLimits")
        for i in range(len(self.vitesseInfrastructure[0])) :
            self.debug.progression(i, len(self.vitesseInfrastructure[0]))
            if len(self.vitesseInfrastructure[0][i]) == 4 :
                try :
                    temp = self.vitessesVoies[self.vitesseInfrastructure[0][i][0].text, self.vitesseInfrastructure[0][i][2].text]
                    temp.append([self.vitesseInfrastructure[0][i][1][0][0].text, self.vitesseInfrastructure[0][i][1][1][0].text, "All", self.vitesseInfrastructure[0][i][3].text])
                    self.vitessesVoies.update({ (self.vitesseInfrastructure[0][i][0].text, self.vitesseInfrastructure[0][i][2].text) : temp })
                except :
                    self.vitessesVoies[self.vitesseInfrastructure[0][i][0].text, self.vitesseInfrastructure[0][i][2].text] = [[self.vitesseInfrastructure[0][i][1][0][0].text, self.vitesseInfrastructure[0][i][1][1][0].text, "All", self.vitesseInfrastructure[0][i][3].text]]
            else :
                try :
                    temp = self.vitessesVoies[self.vitesseInfrastructure[0][i][0].text, self.vitesseInfrastructure[0][i][2].text]
                    temp.append([self.vitesseInfrastructure[0][i][1][0][0].text, self.vitesseInfrastructure[0][i][1][1][0].text, self.vitesseInfrastructure[0][i][3].text, self.vitesseInfrastructure[0][i][4].text])
                    self.vitessesVoies.update({ (self.vitesseInfrastructure[0][i][0].text, self.vitesseInfrastructure[0][i][2].text) : temp })
                except :
                    self.vitessesVoies[self.vitesseInfrastructure[0][i][0].text, self.vitesseInfrastructure[0][i][2].text] = [[self.vitesseInfrastructure[0][i][1][0][0].text, self.vitesseInfrastructure[0][i][1][1][0].text, self.vitesseInfrastructure[0][i][3].text, self.vitesseInfrastructure[0][i][4].text]]
        with open(self.rootPath + r"\Infrastructure\VitessesVoies.pickle", "wb") as binaryFile :
            pickle.dump(self.vitessesVoies, binaryFile)

    def acquisitionGradients(self) :
        self.profilInfrastructure = self.tree.xpath("/infrastructure/profiles/gradients")
        for i in range(len(self.profilInfrastructure[0])) :
            self.debug.progression(i, len(self.profilInfrastructure[0]))
            try :
                temp = self.gradientsVoies[self.profilInfrastructure[0][i][0].text]
                temp.append([self.profilInfrastructure[0][i][1][0][0].text, self.profilInfrastructure[0][i][1][1][0].text, self.profilInfrastructure[0][i][2].text])
                self.gradientsVoies.update({ (self.profilInfrastructure[0][i][0].text) : temp })
            except :
                self.gradientsVoies[self.profilInfrastructure[0][i][0].text] = [[self.profilInfrastructure[0][i][1][0][0].text, self.profilInfrastructure[0][i][1][1][0].text, self.profilInfrastructure[0][i][2].text]]
        with open(self.rootPath + r"\Infrastructure\GradientsVoies.pickle", "wb") as binaryFile :
            pickle.dump(self.gradientsVoies, binaryFile)

    def acquisitionRadiuses(self) :
        self.courbureInfrastructure = self.tree.xpath("/infrastructure/profiles/radiuses")
        for i in range(len(self.courbureInfrastructure[0])) :
            self.debug.progression(i, len(self.courbureInfrastructure[0]))
            try :
                temp = self.radiusesVoies[self.courbureInfrastructure[0][i][0].text]
                temp.append([self.courbureInfrastructure[0][i][1][0][0].text, self.courbureInfrastructure[0][i][1][1][0].text, self.courbureInfrastructure[0][i][2].text])
                self.radiusesVoies.update({ (self.courbureInfrastructure[0][i][0].text) : temp })
            except :
                self.radiusesVoies[self.courbureInfrastructure[0][i][0].text] = [[self.courbureInfrastructure[0][i][1][0][0].text, self.courbureInfrastructure[0][i][1][1][0].text, self.courbureInfrastructure[0][i][2].text]]
        with open(self.rootPath + r"\Infrastructure\RadiusesVoies.pickle", "wb") as binaryFile :
            pickle.dump(self.radiusesVoies, binaryFile)

    def acquisitionSignaux(self) :
        self.signauxInfrastructure = self.tree.xpath("/infrastructure/interlocking/signals")
        self.speedIndicatorsInfrastructure = self.tree.xpath("/infrastructure/interlocking/speedIndicators")
        for signal in self.signauxInfrastructure[0] :
            try :
                speedSections = signal.find("speedSections")
            except :
                pass
            voieSignal = signal.find("position")[0].text
            sens = signal.find("position")[2].text
            section = []
            if speedSections != None :
                for speedSection in speedSections :
                    temp = []
                    temp.append(signal.find("key").text)
                    temp.append(speedSection.find("speed").text)
                    temp.append(speedSection.find("velocityProfileSet").text)
                    temp.append([])
                    try :
                        for path in speedSection.find("path") :
                            temp[3].append([path.find("sectionKey").text, path.find("begin")[0].text, path.find("end")[0].text])
                        section.append(temp)
                    except :
                        print(signal.find("key").text)
            #print(section)            
            try :
                temp = self.signauxVoies[voieSignal, sens]
                temp.append(section)
                self.signauxVoies.update({ (voieSignal, sens) : temp })
            except :
                self.signauxVoies[voieSignal, sens] = [section]
        for signal in self.speedIndicatorsInfrastructure[0] :
            try :
                speedSections = signal.find("speedSections")
            except :
                pass
            voieSignal = signal.find("position")[0].text
            sens = signal.find("position")[2].text
            section = []
            if speedSections != None :
                for speedSection in speedSections :
                    temp = []
                    temp.append(signal.find("key").text)
                    temp.append(speedSection.find("speed").text)
                    temp.append(speedSection.find("velocityProfileSet").text)
                    temp.append([])
                    try :
                        for path in speedSection.find("path") :
                            temp[3].append([path.find("sectionKey").text, path.find("begin")[0].text, path.find("end")[0].text])
                        section.append(temp)
                    except :
                        print(signal.find("key").text)                        
            #print(section)           
            if section != [] :
                try :
                    temp = self.signauxVoies[voieSignal, sens]
                    temp.append(section)
                    self.signauxVoies.update({ (voieSignal, sens) : temp })
                except :
                    self.signauxVoies[voieSignal, sens] = [section]
        with open(self.rootPath + r"\Infrastructure\SignauxVoies.pickle", "wb") as binaryFile :
            pickle.dump(self.signauxVoies, binaryFile)

    def acquisitionSignaux1(self) :
        self.signauxInfrastructure = self.tree.xpath("/infrastructure/interlocking/speedIndicators")
        print(len(self.signauxInfrastructure[0]))
        for signal in self.signauxInfrastructure[0] :
            try :
                speed = signal.find("speed").text
                print(speed)
            except :
                print("pas de vitesse")
            
            #self.debug.progression(i, len(self.signauxInfrastructure[0]))
            #self.signauxVoies[self.signauxInfrastructure[0][i][0].text] = [self.signauxInfrastructure[0][i][1][0][0].text, self.signauxInfrastructure[0][i][1][1][0].text, self.signauxInfrastructure[0][i][2].text]
        #with open(self.rootPath + r"\Infrastructure\SignauxVoies.pickle", "wb") as binaryFile :
            #pickle.dump(self.signauxVoies, binaryFile)

    def acquisitionSignauxSpeedIndicators(self) :
        self.signauxInfrastructure = self.tree.xpath("/infrastructure/interlocking/speedIndicators")
        position = []
        #for position1 in self.signauxInfrastructure.xpath("postion") :
            #position.append(position1.find("position").text)
        temp = []
        #print(len(self.signauxInfrastructure[0]))
        for i in range(len(self.signauxInfrastructure[0])) :
            self.debug.progression(i, len(self.signauxInfrastructure[0]))
            temp1 = []


            if len(self.signauxInfrastructure[0][i]) == 4 :
                #print(0)
                pass

            elif len(self.signauxInfrastructure[0][i]) == 5 and len(self.signauxInfrastructure[0][i][4]) == 0 :
                #print(0)
                pass
            elif len(self.signauxInfrastructure[0][i]) == 5 and len(self.signauxInfrastructure[0][i][4]) != 0 :
                temp2 = []
                temp3 = []
                temp1.append([self.signauxInfrastructure[0][i][3][0].text])
                #print(self.signauxInfrastructure[0][i][0].text)
                for j in range(len(self.signauxInfrastructure[0][i][4])) :
                    speedSection = []
                    temp2.append([self.signauxInfrastructure[0][i][4][j][0].text, self.signauxInfrastructure[0][i][4][j][2].text])
                    temp3.append(self.signauxInfrastructure[0][i][4][j][0].text)
                    temp3.append(self.signauxInfrastructure[0][i][4][j][2].text)
                    #print([self.signauxInfrastructure[0][i][4][j][3][n][0].text, self.signauxInfrastructure[0][i][4][j][3][n][1][0].text, self.signauxInfrastructure[0][i][4][j][3][n][2][0].text])
                    try :
                        for n in range(len(self.signauxInfrastructure[0][i][4][j][3])) :
                            speedSection.append([self.signauxInfrastructure[0][i][4][j][3][n][0].text, self.signauxInfrastructure[0][i][4][j][3][n][1][0].text, self.signauxInfrastructure[0][i][4][j][3][n][2][0].text])
                    except :
                        print("Signal vide")
                    temp3.append(speedSection)
                    temp2[-1].append(speedSection)
                #temp1[-1][1].append(temp2)

            elif len(self.signauxInfrastructure[0][i]) == 6 :
                #print(2)
                temp2 = []
                temp3 = []
                temp1.append([self.signauxInfrastructure[0][i][3][0].text])
                #print(self.signauxInfrastructure[0][i][0].text)
                for j in range(len(self.signauxInfrastructure[0][i][5])) :
                    speedSection = []
                    temp2.append([self.signauxInfrastructure[0][i][5][j][0].text, self.signauxInfrastructure[0][i][5][j][2].text])
                    temp3.append(self.signauxInfrastructure[0][i][5][j][0].text)
                    temp3.append(self.signauxInfrastructure[0][i][5][j][2].text)
                    try :
                        for n in range(len(self.signauxInfrastructure[0][i][5][j][3])) :
                            speedSection.append([self.signauxInfrastructure[0][i][5][j][3][n][0].text, self.signauxInfrastructure[0][i][5][j][3][n][1][0].text, self.signauxInfrastructure[0][i][5][j][3][n][2][0].text])
                    except :
                        print("Signal vide")
                    temp2[-1].append(speedSection)
                    temp3.append(speedSection)
                temp1[-1].append(temp2)
                print("1",temp1)
                print("2",temp2)
                print("3",temp3)

            else : ### longueur = 7
                #print(self.signauxInfrastructure[0][i][0].text)
                #print(3)
                temp2 = []
                temp3 = []
                temp1.append([self.signauxInfrastructure[0][i][3][1].text])
                #print(self.signauxInfrastructure[0][i][0].text)
                for j in range(len(self.signauxInfrastructure[0][i][5])) :
                    speedSection = []
                    temp2.append([self.signauxInfrastructure[0][i][5][j][0].text, self.signauxInfrastructure[0][i][5][j][2].text])
                    temp3.append(self.signauxInfrastructure[0][i][5][j][0].text)
                    temp3.append(self.signauxInfrastructure[0][i][5][j][2].text)
                    try :
                        for n in range(len(self.signauxInfrastructure[0][i][5][j][3])) :
                            speedSection.append([self.signauxInfrastructure[0][i][5][j][3][n][0].text, self.signauxInfrastructure[0][i][5][j][3][n][1][0].text, self.signauxInfrastructure[0][i][5][j][3][n][2][0].text])
                    except :
                        print("Signal vide")
                    temp2[-1].append(speedSection)
                    temp3.append(speedSection)
                #temp1[-1].append(temp2)
            if temp1 == [] :
                pass
            else :
                try :
                    temp = self.signauxVoies[self.signauxInfrastructure[0][i][3][0].text, self.signauxInfrastructure[0][i][3][2].text]
                    temp.append(temp3)#[self.signauxInfrastructure[0][i][1][0][0].text, self.signauxInfrastructure[0][i][1][1][0].text, self.signauxInfrastructure[0][i][2].text])
                    self.signauxVoies.update({ (self.signauxInfrastructure[0][i][3][0].text, self.signauxInfrastructure[0][i][3][2].text) : temp })
                except :
                    self.signauxVoies[self.signauxInfrastructure[0][i][3][0].text, self.signauxInfrastructure[0][i][3][2].text] = [temp3]
        with open(self.rootPath + r"\Infrastructure\SignauxVoiesSpeedIndicators.pickle", "wb") as binaryFile :
            pickle.dump(self.signauxVoies, binaryFile)

    def acquisitionSignauxBlocks(self) :
        self.signauxInfrastructure = self.tree.xpath("/infrastructure/interlocking/blocks")
        for i in range(len(self.signauxInfrastructure[0])) :
            self.debug.progression(i, len(self.signauxInfrastructure[0]))
            self.signauxVoies[self.signauxInfrastructure[0][i][0].text] = [self.signauxInfrastructure[0][i][1][0][0].text, self.signauxInfrastructure[0][i][1][1][0].text, self.signauxInfrastructure[0][i][2].text]
        with open(self.rootPath + r"\Infrastructure\SignauxVoiesBlocks.pickle", "wb") as binaryFile :
            pickle.dump(self.signauxVoies, binaryFile)

    def acquisitionElectrification(self) :
        self.electrificationInfrastructure = self.tree.xpath("/infrastructure/electrification/sectionElectricProfiles")
        for i in range(len(self.electrificationInfrastructure[0])) :
            self.debug.progression(i, len(self.electrificationInfrastructure[0]))
            if len(self.electrificationInfrastructure[0][i]) == 5 :
                try :
                    temp = self.electrificationVoies[self.electrificationInfrastructure[0][i][0].text, self.electrificationInfrastructure[0][i][2].text]
                    temp.append([self.electrificationInfrastructure[0][i][1][0][0].text, self.electrificationInfrastructure[0][i][1][1][0].text, self.electrificationInfrastructure[0][i][3].text, self.electrificationInfrastructure[0][i][4].text])
                    self.electrificationVoies.update({ (self.electrificationInfrastructure[0][i][0].text, self.electrificationInfrastructure[0][i][2].text) : temp })
                except :
                    self.electrificationVoies[self.electrificationInfrastructure[0][i][0].text, self.electrificationInfrastructure[0][i][2].text] = [[self.electrificationInfrastructure[0][i][1][0][0].text, self.electrificationInfrastructure[0][i][1][1][0].text, self.electrificationInfrastructure[0][i][3].text, self.electrificationInfrastructure[0][i][4].text]]
                else :
                    try :
                        temp = self.electrificationVoies[self.electrificationInfrastructure[0][i][0].text, self.electrificationInfrastructure[0][i][2].text]
                        temp.append([self.electrificationInfrastructure[0][i][1][0][0].text, self.electrificationInfrastructure[0][i][1][1][0].text, "", self.electrificationInfrastructure[0][i][3].text])
                        self.electrificationVoies.update({ (self.electrificationInfrastructure[0][i][0].text, self.electrificationInfrastructure[0][i][2].text) : temp })
                    except :
                        self.electrificationVoies[self.electrificationInfrastructure[0][i][0].text, self.electrificationInfrastructure[0][i][2].text] = [[self.electrificationInfrastructure[0][i][1][0][0].text, self.electrificationInfrastructure[0][i][1][1][0].text, "", self.electrificationInfrastructure[0][i][3].text]]
        with open(self.rootPath + r"\Infrastructure\ElectrificationVoies.pickle", "wb") as binaryFile :
            pickle.dump(self.electrificationVoies, binaryFile)

    def acquisitionGPS(self) :
        fichierREFTRA = self.rootPath + r"\Infrastructure\IGRE_VOIE_XY_PK2.xlsx"
        self.dataGPS = {}
        self.clesGPS = []
        self.wb = xlrd.open_workbook(fichierREFTRA)
        self.sh = self.wb.sheet_by_name(u'LRef')
        self.dataGPS = {}
        i = 0
        memoire_ligne_voie = []
        donnees = []
        for rownum in range(1,self.sh.nrows) :
            self.debug.progression(rownum, self.sh.nrows)
            pkd = float(self.sh.row_values(rownum)[5])
            pkf = float(self.sh.row_values(rownum)[6])
            if pkf - pkd >= 0 :
                tampon = [pkd / 1000, pkf / 1000]
            else :
                tampon = [pkf / 1000, pkd / 1000]
            if int(self.sh.row_values(rownum)[2]) not in self.donnees_GPS_ligne :
                self.donnees_GPS_ligne[int(self.sh.row_values(rownum)[2])] = []
            if [int(self.sh.row_values(rownum)[2]),self.sh.row_values(rownum)[3]] != memoire_ligne_voie and i != 0 :
                self.donneesGPS[int(self.sh.row_values(rownum-1)[2]),self.sh.row_values(rownum-1)[3]] = donnees
                self.clesGPS.append([int(self.sh.row_values(rownum-1)[2]),self.sh.row_values(rownum-1)[3]])
                self.donnees_GPS_ligne[int(self.sh.row_values(rownum-1)[2])].append(donnees)
                donnees = [tampon]
                memoire_ligne_voie = [int(self.sh.row_values(rownum)[2]),self.sh.row_values(rownum)[3]]                
            else : 
                donnees.append(tampon)
            if rownum == self.sh.nrows - 1 :
                self.donneesGPS[int(self.sh.row_values(rownum)[2]),self.sh.row_values(rownum)[3]] = donnees
                self.clesGPS.append([int(self.sh.row_values(rownum)[2]),self.sh.row_values(rownum)[3]])
                self.donnees_GPS_ligne[int(self.sh.row_values(rownum-1)[2])].append(donnees)
            i += 1
        with open(self.rootPath + r"\Infrastructure\GPSVoies.pickle", "wb") as binaryFile :
            pickle.dump(self.dataGPS, binaryFile)

    def acquisitionHierarchieIndiceCompo (self):
        fichierVITESSES = self.rootPath + r"\Infrastructure\Hiérarchie Indice Compo et Signaux.xlsx"
        wb = xlrd.open_workbook(fichierVITESSES)
        sh = wb.sheet_by_name(u'Hierarchie calculée')
        liste_materiels = []
        for rownum in range(1,sh.nrows) :
            liste_materiels.append(sh.row_values(rownum)[1:])
        dico_materiels = {}
        for i in range (len(liste_materiels)) :
            dico_materiels[(liste_materiels[i][0])] = liste_materiels[i][1:]
        with open(self.rootPath + r"\Infrastructure\HierarchieIndiceCompo.pickle", "wb") as binaryFile :
            pickle.dump(dico_materiels, binaryFile)


    def acquisitionHierarchieTIV (self):
        fichierVITESSES = self.rootPath + r"\Infrastructure\Hiérarchie Indice Compo et Signaux.xlsx"
        wb = xlrd.open_workbook(fichierVITESSES)
        sh2 = wb.sheet_by_name(u'Profils de vitesse-TIV')
        liste_profilsvitesse = []
        for rownum in range(sh2.nrows) :
            if sh2.row_values(rownum)[3:] == ['-' for i in range(14)] :
                listevaleurs=['X' for i in range(14)]
                listevaleurs.insert(0,sh2.row_values(rownum)[2])
            else :
                listevaleurs=sh2.row_values(rownum)[2:]
            liste_profilsvitesse.append(listevaleurs)
        dico_profils = {}
        for i in range (len(liste_profilsvitesse)) :
            dico_profils[(liste_profilsvitesse[i][0])] = liste_profilsvitesse[i][1:]
        with open(self.rootPath + r"\Infrastructure\HierarchieProfilVitesse.pickle", "wb") as binaryFile :
            pickle.dump(dico_profils, binaryFile)

    def chargementVitesses(self) :
        with open(self.rootPath + r"\Infrastructure\VitessesVoies.pickle", "rb") as binaryFile :
            return pickle.load(binaryFile)

    def chargementGradients(self) :
        with open(self.rootPath + r"\Infrastructure\GradientsVoies.pickle", "rb") as binaryFile :
            return pickle.load(binaryFile)

    def chargementRadiuses(self) :
        with open(self.rootPath + r"\Infrastructure\RadiusesVoies.pickle", "rb") as binaryFile :
            return pickle.load(binaryFile)

    def chargementSignaux(self) :
        with open(self.rootPath + r"\Infrastructure\SignauxVoies.pickle", "rb") as binaryFile :
            return pickle.load(binaryFile)

    def chargementSignauxSpeedIndicators(self) :
        with open(self.rootPath + r"\Infrastructure\SignauxVoiesSpeedIndicators.pickle", "rb") as binaryFile :
            return pickle.load(binaryFile)

    def chargementSignauxBlocks(self) :
        with open(self.rootPath + r"\Infrastructure\SignauxVoiesBlocks.pickle", "rb") as binaryFile :
            return pickle.load(binaryFile)

    def chargementElectrification(self) :
        with open(self.rootPath + r"\Infrastructure\ElectrificationVoies.pickle", "rb") as binaryFile :
            return pickle.load(binaryFile)

    def chargementGPS(self) :
        with open(self.rootPath + r"\Infrastructure\GPSVoies.pickle", "rb") as binaryFile :  
            return pickle.load(binaryFile)

    def chargementHierarchieIndiceCompo(self) :
        with open(self.rootPath + r"\Infrastructure\HierarchieIndiceCompo.pickle", "rb") as binaryFile :  
            #print(pickle.load(binaryFile))
            return pickle.load(binaryFile)
    
    def chargementHierarchieTIV(self) :
        with open(self.rootPath + r"\Infrastructure\HierarchieProfilVitesse.pickle", "rb") as binaryFile :  
            #print(pickle.load(binaryFile))
            return pickle.load(binaryFile)

#infrastructure = Infrastructure()
#infrastructure.acquisitionHierarchieIndiceCompo()
#infrastructure.chargementHierarchieIndiceCompo()
#infrastructure.acquisitionHierarchieTIV()
#infrastructure.chargementHierarchieTIV()

#vitessesVoies = { (ligne / voie = SRV ; VelocityProfile ; sens de circulation) : [[0.000 = pk début, 127.328 = pk fin, 60 = valeur vitesse], ... ] ; ... }
#gradientsVoies = { (ligne / voie = SRV) : [[0.000 = pk début, 127.328 = pk fin, -5.7 = valeur gradient], ... ] ; ... }
#radiusesVoies = { (ligne / voie = SRV ; sens de circulation) : [[0.000 = pk début, 127.328 = pk fin, 650 = valeur radius], ... ] ; ... }
#signauxVoies = { (ligne / voie ; sens de circulation ? ) : [ [pk de positionnement du signal ; vitesse imposée par la signal ; [listes des chemins à emprunter afin d'avoir l'application de la vitesse du signal] ] ; ... ] }
#electrificationVoies = {A définir}