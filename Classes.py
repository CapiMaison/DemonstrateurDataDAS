""" Created by Guillaume WELLER : 03/12/2020 """

######### ######### ######### ######### ####9#### ######### ######### ######### #########

import datetime
import time
import os
import shutil
import xlrd
import csv
import lxml.etree

class Debug:
    """ Classe permettant d'afficher des informations lors de l'utilisation d'un algorythme """

    def __init__(self):
        self.header = "[{} | {}] "
        self.heure_debut = self.h_debut_programme()
        self.action_programme = {
            "Fin" : "Fin du programme... \n                      |  Rappel, heure de début : " + self.heure_debut,
            "ProcheFinSA" : "ATTENTION\n\n/!\ \nLa fin du SA est dans moins de 25 jours.\nNe pas oublier de changer la variabe de fin de SA du programme pour un bon fonctionnement de l'algorithme...\n/!\ \n",
            "ChoixProgramme" : "Que souhaitez vous faire ?\n\n\t1 -> Mettre à jour le PowerBI\n\t2 -> Actualiser les données ADC\n\t3 -> Actualiser les données GPS de la base REFTRA\n",
            "ErreurChoixProgramme" : "Choisissez un chiffre présenté dans la liste...",
            "MauvaisEnvironnement" : "Erreur : compléter avec un environnement existant...",
            "ErreurServeurSNCF" : "Erreur : les serveurs SNCF semblent indisponibles, contacter votre administrateur...",
            "AcquisitionFichiers" : "Acquisition des fichiers pour la MAJ",
            "DateDimanche" : "Récupération de la date du dernier passage de batch",
            "PortailSIRIUS" : "Récupération des données du portail SIRIUS",
            "TCT" : "Récupération des données TCT",
            "GPS" : "Récupération des coordonnées GPS de la base REFTRA",
            "Header" : "Définition des headers des fichiers de sortie",
            "RapportSIPH" : "Création du fichier de sortie SIPH du PowerBI",
            "FichiersRouteSIPH" : "Traitement des fichiers routes issus de SIPH",
            "RapportGPS" : "Création du fichier de sortie GPS du PowerBI",
            "RapportTrajet" : "Création du fichier de sortie des trajets par sillon du PowerBI",
            "Version" : "Mise à jour de la date d'actualisation des données du PowerBI",
            "MAJGPS" : "Mise à jour de la base REFTRA",
            "FinMAJGPS" : "Fichier binaire correctement actualisé",
            "Erreur" : "Erreur : une erreur inconnue s'est produite..."
        }
        print("Created by Guillaume WELLER on 09/01/2020 \nLast modifications on 23/12/2020 by Guillaume WELLER\n")
        print(self.appel_header(), "Début du programme...")
        
    def h_debut_programme(self):
        return time.asctime()[11:19]
        
    def appel_header(self):
        return self.header.format(datetime.date.today(), time.asctime()[11:19])
    
    def completer_dictionnaire(self, cle, action_du_programme):
        self.action_programme[str(cle)] = str(action_du_programme)
        #print("Expression intégrée")
        
    def appel(self, cle):
        print(self.appel_header(), self.action_programme[str(cle)])     
        if cle == "Fin":
            os.system("pause")
        
    def progression(self, i, maximum):
        print(self.appel_header(), "Progression : {}%".format(str(i/maximum*100)[:4]), end = "\n")
        if i == maximum - 1:
            print(self.appel_header(), "Fin de la boucle...")

class Archivage:
    """ Classe permettant d'effectuer des opérations d'archivage simples """

    def __init__(self,rootPath):
        self.rootPath = rootPath

    def ArchivageFichierSIPH(self,fichierAArchiver,env):
        shutil.move(fichierAArchiver,self.rootPath + "\\Archives\\" + env + "\\" + os.path.basename(fichierAArchiver).split(".")[0] + " " + str(datetime.date.today()) + ".csv")
        
    def ArchivageFichierGPS(self,fichierAArchiver):
        shutil.move(fichierAArchiver,self.rootPath + "\\Archives\\GPS\\" + os.path.basename(fichierAArchiver).split(".")[0] + " " + str(datetime.date.today()) + ".csv")

    def ArchivageFichierTrajet(self,fichierAArchiver):
        shutil.move(fichierAArchiver,self.rootPath + "\\Archives\\Trajet\\" + os.path.basename(fichierAArchiver).split(".")[0] + " " + str(datetime.date.today()) + ".csv")

    def ArchivageFichiersADC(self,fichierAArchiver):
        shutil.move(fichierAArchiver,self.rootPath + "\\Archives\\ADC\\" + os.path.basename(fichierAArchiver).split(".")[0] + " " + str(datetime.date.today()) + ".txt")

class PortailSIRIUS:
    """ CLasse permettant de définir si un sillon est actif dans le portail SIRIUS ou non """

    def __init__(self,fichierSIRIUS):
        self.fichierSIRIUS = fichierSIRIUS
        self.wb = xlrd.open_workbook(self.fichierSIRIUS)
        self.sh = self.wb.sheet_by_name(u'Feuil1')
        self.minimum = []
        self.maximum = []
        self.activiteSIRIUS = []
        self.nombreSillonNonNumerique = 0
        for rownum in range(self.sh.nrows) :
            if self.sh.row_values(rownum)[0] != "Activité" :
                self.minimum.append(int(self.sh.row_values(rownum)[4]))
                self.maximum.append(int(self.sh.row_values(rownum)[5]))
                self.activiteSIRIUS.append(self.sh.row_values(rownum)[1]) 

    def inclusSIRIUS(self,numeroSillon):
        flag_SIRIUS = 0
        try :
            for i in range(len(self.minimum)) :            
                if self.minimum[i] <= int(numeroSillon) <= self.maximum[i] :
                    flag_SIRIUS = 1
                    break
        except :
            self.nombreSillonNonNumerique += 1
        return flag_SIRIUS

class CodesTCT:
    """ CLasse permettant de définir l'Activité d'un sillon grâce à son code TCT """

    def __init__(self,fichierTCT):
        self.fichierTCT = fichierTCT
        self.activite = {}
        self.wb = xlrd.open_workbook(self.fichierTCT)
        self.sh = self.wb.sheet_by_name(u'Feuil1')
        self.nombreSillonNonNumerique = 0
        r = 0
        for rownum in range(self.sh.nrows) :
            if r != 0 :
                self.activite[self.sh.row_values(rownum)[0]] = self.sh.row_values(rownum)[1]
            r = r + 1

    def Activite(self,TCT):
        nomActivite = "-"
        try :
            nomActivite = self.activite[TCT]
        except :
            pass
        return nomActivite

class GPS:
    """ Classe permettant de définir les dictionnaires de lignes / voies dont Opti-Conduite possède les données """

    def __init__(self,fichierREFTRA):
        self.fichierREFTRA = fichierREFTRA
        self.donneesGPS = {}
        self.clesGPS = []
        self.wb = xlrd.open_workbook(self.fichierREFTRA)
        self.sh = self.wb.sheet_by_name(u'LRef')
        self.donnees_GPS_ligne = {}
        i = 0
        memoire_ligne_voie = []
        donnees = []
        for rownum in range(1,self.sh.nrows) :
            pkd = float(self.sh.row_values(rownum)[5])
            pkf = float(self.sh.row_values(rownum)[6])
            if pkf - pkd >= 0 :
                tampon = [pkd / 1000, pkf / 1000]
            else :
                tampon = [pkf / 1000, pkd / 1000]
            os.system("pause")
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
        
    def Acquisition(self) :
        return self.donnees_GPS_ligne

class Route:
    """ Permet d'étudier en détail un fichier Route """

    def __init__(self,fichierRoute,pathSIPH,listeFichiersSIPH,compteur):
        self.fichierRoute = fichierRoute
        self.numeroSillon = (self.fichierRoute.split("_")[0]).split("\\")[-1]
        self.secondNumeroSillon = ""
        self.regimeDeuxSemaines = ""
        self.TCT = ""
        self.dateDebutValidite = self.fichierRoute.split("_")[1]
        self.dateFinValidite = self.fichierRoute.split("_")[2]
        self.dateActualisation = self.fichierRoute.split("_")[3]
        self.origine = ""
        self.destination = ""
        self.trajet = []
        self.gares = []
        self.completudeGPSSIRIUS = ""
        self.travaux = "-"
        self.problematiqueDoubleSPD = 1
        self.problematiqueTrouGEO = 1
        self.longueur = 0
        self.materiel = ""
        self.variante = "False"
        if compteur != 0 :
            self.variante = "True"

        ### Etude du fichier Route du sillon ###
        with open(self.fichierRoute, newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')                   
            FEA = []
            GEO = []
            self.GPS = []
            SPD = []
            compteurFEA = 0
            for row in spamreader:
                if str(row)[2:-2].split("\\t")[0] == "SPD" :
                    SPD.append(float(str(row)[2:-2].split("\\t")[1]))
                if str(row)[2:-2].split("\\t")[0] == "TSL" :
                    self.travaux = "Présence de chantier"
                if str(row)[2:-2].split("\\t")[0] == "GEO" :
                    GEO.append(float(str(row)[2:-2].split("\\t")[1]))
                    self.GPS.append([self.numeroSillon, compteur, float(str(row).split("\\t")[2]), float(str(row).split("\\t")[3][:-2])])
                if str(row)[2:-2].split("\\t")[0] == "FEA" :
                    if compteurFEA == 1 :
                        self.completudeGPSSIRIUS = str(row)[2:-2].split("\\t")[-2]
                        self.origine = ((str(row)[2:-2].split("\\t")[-1]).split("#OD#")[0]).split("/")[0]
                        self.destination = ((str(row)[2:-2].split("\\t")[-1]).split("#OD#")[1]).split("/")[0]
                    FEA.append(str(row)[2:-2])
                    compteurFEA += 1
            try : #Le "try" pour la recette, à enlever en prod
                self.longueur = float(SPD[-1])
            except :
                pass
            for i in range(len(SPD)) :
                if SPD[i] in SPD[:i] + SPD[i+1:] :
                    self.problematiqueDoubleSPD = 0
                    break
            for i in range(len(GEO)-1) :
                if GEO[i+1] - GEO[i] > 9 :
                    self.problematiqueTrouGEO = 0
                    break
            for i in range(len(FEA)) :
                if i == 2 :
                    try :
                        self.trajet.append([int(FEA[i].split("'")[2]),FEA[i].split("'")[4],float((FEA[i+2].split("\\t")[3]).split(" ")[0])])
                    except :
                        pass
                if i != len(FEA) and i != 2 and (FEA[i].split("\\t")[3])[:6] == "CHANGE" :
                    try :
                        self.trajet[-1].append(float((FEA[i-1].split("\\t")[3]).split(" ")[0]))
                        self.trajet.append([int(FEA[i].split("'")[2]),FEA[i].split("'")[4],float((FEA[i+1].split("\\t")[3]).split(" ")[0])])
                    except :
                        pass
                elif i == len(FEA)-1 :
                    #print(FEA[i])
                    try :
                        self.trajet[-1].append(float((FEA[i].split("\\t")[3]).split(" ")[0]))
                    except :
                        try :
                            self.trajet[-1].append(float((FEA[i-1].split("\\t")[3]).split(" ")[0]))
                        except :
                            pass
            for i in range(len(self.trajet)) :
                if self.trajet[i][2] > self.trajet[i][3] :
                    self.trajet[i][2], self.trajet[i][3] = self.trajet[i][3], self.trajet[i][2]

        ### Etude du fichier de l'EDF SIPH ###
        temp = []
        for i in range(len(listeFichiersSIPH)) :
            if listeFichiersSIPH[i].split("_")[0] == self.numeroSillon :
                temp.append(i)
        try :
            self.fichierSIPH = listeFichiersSIPH[temp[compteur]]
            tree = lxml.etree.parse(pathSIPH + "\\" + listeFichiersSIPH[temp[compteur]])
            bitset = tree.xpath("/DRIVINGDYNAMICS_REPORT/Header/Train/ODT/BITSET")[0].text
            self.regimeDeuxSemaines = self.regimeSillon(bitset)
            #print(self.regimeDeuxSemaines)
            self.materiel = tree.xpath("/DRIVINGDYNAMICS_REPORT/TRAINRUNDATA/ENTRY/MODEL_TRAIN")[0].text
            self.TCT = tree.xpath("/DRIVINGDYNAMICS_REPORT/Header/Train/TRAINTYPE")[0].text
            self.secondNumeroSillon = tree.xpath("/DRIVINGDYNAMICS_REPORT/Header/Train/SECONDARY_TRAINNUMBER")[0].text
            PR = tree.xpath("/DRIVINGDYNAMICS_REPORT/TRAINRUNDATA/ENTRY/STATION/NAME")
            memoireGare = ""
            for n in range(len(PR)) :
                if PR[n].getparent()[3].text != "Gare de passage" and PR[n].text != memoireGare :
                    self.gares.append([PR[n].text[:-3], PR[n].getparent()[3].text])
                    memoireGare = PR[n].text
            self.origine = PR[0].text
            self.destination = PR[-1].text
        except :
            pass
            #print("Pas de correspondance d'EDF pour le fichier Route du sillon n° {}".format(self.numeroSillon))

    def regimeSillon(self,bitset):
        self.bitset = bitset
        td = datetime.date.today() - datetime.date(int(self.dateDebutValidite[:4]),int(self.dateDebutValidite[4:6]),int(self.dateDebutValidite[6:]))
        debutCurseur = int(str(td).split(" ")[0])
        regimeDeuxSemaines = []
        for i in range(1,15) :
            try :
                regimeDeuxSemaines.append(self.bitset[debutCurseur + i])
            except:
                regimeDeuxSemaines.append("0")
        return regimeDeuxSemaines