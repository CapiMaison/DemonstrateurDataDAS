""" Created by Guillaume WELLER on 04/05/2021 """
""" Last modifications on 04/05/2021 by Guillaume WELLER """

######### ######### ######### ######### ####9#### ######### ######### ######### #########

##########################
### Modules à importer ###
##########################

import os
#import sys
import datetime
import csv
import pickle
import xlrd
#import lxml.etree
#from colorama import Fore
from Classes import Debug, Fonctions

rootPath = os.getcwd()
debug = Debug()
f = Fonctions()
#archive = Archivage(rootPath)



################
### Contexte ###
################

articlesTTH = ['01 -> début TTH', '50 -> données sillons', '57 -> régions traversés', '52 -> informations points horaires', '7H -> description du parcours', '55 -> renvois', '53 -> signes conventionnels']



###############
### Classes ###
###############

### Emplacement des fichiers ###

dataCirculationPath = rootPath + r"\Circulation" +   r"\matoll_ctth_0408213054.dat" #1623003028.dat"#1623002213.dat" #r"\matoll_ctth_0408213054.dat"
testPath = rootPath + r"\Test"

#Circulation\matoll_ctth_0408213127.dat



### Classe Sillons ###

class Sillon:
    """ Classe permettant de recueillir les informations liées aux sillons du TTH """

    def __init__(self, rapportTTH):
        
        self.dataSillons = [] # Liste des données utiles pour tous les sillons et triées par sillon
        self.dataSillon50 = [] # Concaténation temporaire des données générales des sillons
        self.dataSillon7H = [] # Concaténation temporaire des données du 7H des sillons
        self.dataSillon57 = []
        self.dataSillon52 = []
        self.dataSillon53 = []
        self.dataSillon55 = []

        for row in rapportTTH :

            articleTTH = row[0][:2]
            concatenatedRow = f.concatenation(row)
            
            if articleTTH == "01" :
                pass

            elif articleTTH == "50" :
                self.numeroSillon = f.cleanString(concatenatedRow[16:22])
                self.indiceCompo =  f.cleanString(concatenatedRow[39:44])
                
                data = [concatenatedRow[2:10],
                        concatenatedRow[10:13],
                        concatenatedRow[13:16],
                        concatenatedRow[16:22],
                        concatenatedRow[22:26],
                        concatenatedRow[26:32],
                        concatenatedRow[32:33],
                        concatenatedRow[33:39],
                        concatenatedRow[39:44],
                        concatenatedRow[44:444],
                        concatenatedRow[444:450],
                        concatenatedRow[450:452],
                        concatenatedRow[452:458],
                        concatenatedRow[458:460],
                        concatenatedRow[460:464],
                        concatenatedRow[464:467],
                        concatenatedRow[467:469],
                        concatenatedRow[469:473],
                        concatenatedRow[473:475],
                        concatenatedRow[475:479],
                        concatenatedRow[479:488],
                        concatenatedRow[488:497]]
                cleanedData = f.clean(data)
                self.dataSillon50 = cleanedData

            elif articleTTH == "7H" :
                data = [concatenatedRow[2:8],
                        concatenatedRow[8:16],
                        concatenatedRow[16:22],
                        concatenatedRow[22:45],
                        concatenatedRow[45:55],
                        concatenatedRow[55:66],
                        concatenatedRow[66:67],
                        concatenatedRow[67:75],
                        concatenatedRow[75:76]]
                cleanedData = f.clean(data)
                self.dataSillon7H.append(cleanedData)
                
            elif articleTTH == "57" :
                pass

            elif articleTTH == "52" :
                data = [concatenatedRow[2:8],
                        concatenatedRow[8:10],
                        concatenatedRow[10:13],
                        concatenatedRow[13:19],
                        concatenatedRow[19:25],
                        concatenatedRow[25:26],
                        concatenatedRow[26:27],
                        concatenatedRow[27:33],
                        concatenatedRow[33:39],
                        concatenatedRow[39:45],
                        concatenatedRow[45:46],
                        concatenatedRow[46:47],
                        concatenatedRow[47:53],
                        concatenatedRow[53:59],
                        concatenatedRow[59:65],
                        ]
                cleanedData = f.clean(data)
                self.dataSillon52.append(cleanedData)

            elif articleTTH == "55" :
                data = [concatenatedRow[2:8],
                        concatenatedRow[8:10],
                        concatenatedRow[10:13],
                        concatenatedRow[13:19],
                        concatenatedRow[19:21],
                        concatenatedRow[21:24],
                        concatenatedRow[24:424],
                        concatenatedRow[424:936],
                        concatenatedRow[936:938],
                        concatenatedRow[938:1008],
                        concatenatedRow[1008:1520],
                        concatenatedRow[1520:1521]
                        ]
                cleanedData = f.clean(data)
                self.dataSillon55.append(cleanedData)

            elif articleTTH == "53" :
                pass

    def cleaned7H(self) :
        self.dataSillon7H_cleaned = []
        #del self.dataSillon7H[0]
        #for i in range(len(self.dataSillon7H)) :
            #self.dataSillon7H_cleaned.append([self.dataSillon7H[i][0], self.dataSillon7H[i][1], []])
        temp = self.dataSillon7H
        for j in range(int(len(temp)/2)) :
            if temp[2*j][6] == "1" :
                temp[2*j][6] = "Ascending"
            else :
                temp[2*j][6] = "Descending"
            self.dataSillon7H_cleaned.append([temp[2*j][7], temp[2*j][3], temp[2*j][2], temp[2*j][5], temp[2*j][4], temp[2*j][1], temp[2*j+1][1], temp[2*j][6]])
        return self.dataSillon7H_cleaned
        


### Classe HOUAT contenant les objets sillons ###

class HOUAT(Sillon):
    """ """

    def __init__(self):
        
        self.circulationPath = os.getcwd() + r"\Circulation\IN"
        self.dossierBinaire = os.getcwd() + r"\Circulation"
        self.fichiersHOUAT = os.listdir(self.circulationPath)
        self.sillonsHOUAT = []
        self.sillonsTests = ["2836", "96721" ,"9211" ,"86092" ,"19905" ,"SOUS70" ,"PILE72" 
        ,"147158" ,"122300" ,"153704" ,"118499" 
        ,"124317" ,"124336" ,"130771" ,"136805" ,"117109" ,"151813" ,"6940" 
        ,"17420" ,"8489" ,"2407" ,"3401", "14157", "3101", "868030", "887143"]

        
    
    def acquisitionSillons(self) :
        for i in range(len(self.fichiersHOUAT)) :
            print("Acquisition HOUAT :", i + 1, "/", len(self.fichiersHOUAT), end = "\n")
            with open(self.circulationPath + "//" + self.fichiersHOUAT[i], 'r', newline='') as csvfile:
                rapportTTH = csv.reader(csvfile, delimiter='!', quotechar='|')
                temp = []
                n = 0
                for row in rapportTTH :
                    articleTTH = row[0][:2]
                    if articleTTH == "01" :
                        pass
                    elif articleTTH == "50" and n != 0 :
                        objet = Sillon(temp)
                        self.sillonsHOUAT.append(objet)
                        #print(temp)
                        temp = []
                        temp.append(row)
                    else :
                        temp.append(row)
                        n =+ 1

        with open(self.dossierBinaire + "\Circulation.pickle", "wb") as binaryFile :
            pickle.dump(self.sillonsHOUAT, binaryFile)

    def chargementSillons(self) :
        with open(self.dossierBinaire + "\Circulation.pickle", "rb") as binaryFile :
            #print(len(pickle.load(binaryFile)))
            return pickle.load(binaryFile)

    def ecritureNumeroSillon(self) :
        fichierExcel = self.dossierBinaire + "\DonnéesSillonsTTH.xlsx"
        liste = self.chargementSillons()
        wb = xlrd.open_workbook(fichierExcel)
        sh2 = wb.sheet_by_name(u'Numéro des sillons')
        liste_profilsvitesse = []
        i = 0
        for sillon in range(liste) :
            #sh2.cell_value(i, 1) = sillon.numeroSillon
            i = i + 1

    def binaireSillonsTests(self) :
        sillons = self.chargementSillons()
        temp = []
        for i in range(len(sillons)) :
            print(sillons[i].numeroSillon)
            print(sillons[i].numeroSillon in self.sillonsTests)
            if sillons[i].numeroSillon in self.sillonsTests :
                temp.append(sillons[i])
        with open(self.dossierBinaire + "\CirculationSillonsTests.pickle", "wb") as binaryFile :
            pickle.dump(temp, binaryFile)

    def chargementSillonsTests(self) :
        with open(self.dossierBinaire + "\CirculationSillonsTests.pickle", "rb") as binaryFile :
            #print(len(pickle.load(binaryFile)))
            return pickle.load(binaryFile)



#houat = HOUAT()
#houat.acquisitionSillons()
#houat.chargementSillons()
#houat.binaireSillonsTests()
#sillons = houat.chargementSillonsTests()
#for sillon in sillons :
    #print(sillon.numeroSillon)
#for i in range(len(houat.sillonsHOUAT)):
#    print(houat.sillonsHOUAT[i].numeroSillon)

