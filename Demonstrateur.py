""" Created by Guillaume WELLER on 09/01/2020 """
""" Last modifications on 23/12/2020 by Guillaume WELLER """

######### ######### ######### ######### ####9#### ######### ######### ######### #########

##########################
### Modules à importer ###
##########################

import os
#import sys
import datetime
import csv
import pickle
#import lxml.etree
#from colorama import Fore
from Classes import Debug, Archivage, PortailSIRIUS, CodesTCT, GPS, Route

rootPath = os.getcwd()
reporting = Debug()
archive = Archivage(rootPath)



##########################
### Variables globales ###
##########################

global ddSA 
ddSA = "2020-12-13"
global dfSA 
dfSA = "2021-12-10"



##########################
### Choix du programme ###
##########################

### Message d'alerte de fin de SA ###
td25 = datetime.timedelta(days = 25)
ajd = datetime.date.today()
if datetime.date(int(dfSA[:4]),int(dfSA[5:7]),int(dfSA[8:])) - ajd <= td25 :
    reporting.appel("ProcheFinSA")
    os.system("pause")




### Présentation des choix pour la suite du programme ###
reporting.appel("ChoixProgramme")
programme = ""
while programme != ("1" or ("2" or "3")) :
    programme = input("Réponse : ")
    try :
        ### MAJ des données du PBI ###
        if int(programme) == 1 :
            environnement = ""
            while environnement != ("prod" or "rec") :
                environnement = input("Choisir entre 'prod' --production-- ou 'rec' --recette-- : ")
                if environnement != ("prod" or "rec") :
                    reporting.appel("MauvaisEnvironnement")

        ### MAJ des données ADC (mesure de sécurité pour ne pas diffuser d'informations confidentielles) ###
        elif int(programme) == 2 : 
            table = input("Quelle table pivot")
            
        ### MAJ des données GPS du fichier binaire ###
        elif int(programme) == 3 : 
            #input("Binaire ?")
            pass

        ### Exception : choix non existant ###
        else : 
            reporting.appel("ErreurChoixProgramme")
    except :
        reporting.appel("ErreurChoixProgramme")
    
        

############################################
### Programme 1 : MAJ des données du PBI ###
############################################

if int(programme) == 1 :
    reporting.appel("AcquisitionFichiers")

    ### Chemins d'accès roots ###
    pathIN = rootPath + "\IN\\"
    pathOUT = rootPath + "\OUT"
    pathArchives = rootPath + "\Archives"
    pathArchivesREFTRA = rootPath + "\Archives\REFTRA binaire\\"

    ### Chemins d'accès serveurs ###
    pathSIPH = r"\\sirius12mid-" + environnement + r".traction.sncf.fr\SIPH\OUTPUT"
    pathRoute = r"\\sirius12mid-" + environnement + r".traction.sncf.fr\Opticonduite\route"

    listeFichiersRoute = os.listdir(pathRoute)

    ### Acquisition des fichiers ###
    listeFichiersIN = os.listdir(pathIN)
    try :
        listeFichiersSIPH = os.listdir(pathSIPH)
        listeFichiersRoute = os.listdir(pathRoute)
    except :
        reporting.appel("ErreurServeurSNCF")
        reporting.appel("Fin")
        #exit()

    ### Liste des fichiers utiles ###
    fichierTCT = pathIN + "Codes_TCT.xlsx"
    fichierREFTRA = pathIN + "GPS_REFTRA.xlsx"
    fichierREFTRAbinaire = pathArchivesREFTRA + "GPSREFTRA.pickle"
    fichierSIRIUS = pathIN + "Portail SIRIUS " + environnement + ".xlsx"
    fichierVersion = pathIN + "Version PBI.xlsx"
    fichierGPS = pathOUT + "\\GPS.csv"

    ### Date du dernier Dimanche ###
    reporting.appel("DateDimanche")
    td1 = datetime.timedelta(days = 1)
    temp = ajd
    while temp.weekday() != 6 :
        temp = temp - td1 #6 pour le Dimanche

    def inclusREFTRA(ligne,pkd,pkf,GPSREFTRA):
        flagGPS = "False"
        for i in range(len(GPSREFTRA[ligne])) :
            for j in range(len(GPSREFTRA[ligne][i])) :
                if (GPSREFTRA[ligne][i][j][0]-0.05 <= pkd <= GPSREFTRA[ligne][i][j][1]+0.05) and (GPSREFTRA[ligne][i][j][0]-0.05 <= pkf <= GPSREFTRA[ligne][i][j][1]+0.05) :
                    flagGPS = "True"
                    break
        return flagGPS
       
    def sillonDuSA(nomFichier):
        if datetime.date(int(nomFichier.split("_")[1][:4]),int(nomFichier.split("_")[1][4:6]),int(nomFichier.split("_")[1][6:])) <= ajd <= datetime.date(int(nomFichier.split("_")[2][:4]),int(nomFichier.split("_")[2][4:6]),int(nomFichier.split("_")[2][6:])) :
            return True
        else :
            return False
        
    def sillonRoule (sillon) :
        flag = "False"
        for p in range(16,30) :
            # print(sillon[p])
            if sillon[p] == "1":
                flag = "True"
        return flag
            


    reporting.appel("PortailSIRIUS")
    SIRIUS = PortailSIRIUS(fichierSIRIUS)
    reporting.appel("TCT")
    TCT = CodesTCT(fichierTCT)
    # reporting.appel("GPS")
    # with open(fichierREFTRAbinaire , "rb") as f :
    #     try :
    #         REFTRA = pickle.load(f)
    #     except :
    #         GPSREFTRA = GPS(fichierREFTRA)


    
    reporting.appel("Header")
    headerSIPH = ['N° sillon',
                  'Second numéro de sillon',
                  'Date de début de validité',
                  'Date de fin de validité',
                  'Date actualisation des données',
                  'Données GPS',
                  'Intégré portail SIRIUS',
                  'Problématique double balise SPD',
                  'Problématique trou de données GPS',
                  'TCT',
                  'Activité',
                  'Origine',
                  'Destination',
                  'Engin moteur',
                  'Longueur du trajet',
                  'Chantier',
                  'Lundi 1', 'Mardi 1', 'Mercredi 1', 'Jeudi 1', 'Vendredi 1', 'Samedi 1', 'Dimanche 1',
                  'Lundi 2', 'Mardi 2', 'Mercredi 2', 'Jeudi 2', 'Vendredi 2', 'Samedi 2', 'Dimanche 2',
                  'Nom fichier Route','Nom du fichier AGATHE', 'Variante']
    headerGPS = ['Numéro de sillon', 'Variante', 'GPS du trajet', 'Ligne', 'Voie', 'PKD', 'PKF', 'GPS sur section']
    headerTrajet = ['Numéro de sillon', 'Variante', "Gares d'arrêt"]
    headerCoordonnees = ['Numéro de sillon', 'Variante', 'Longitude', 'Latitude']

    ### Création du fichier de rapport PBI ###
    reporting.appel("RapportSIPH")
    donneesSillons = []
    donneesGPS = []
    donneesTrajet = []
    rapportCoordonnees = []
    archive.ArchivageFichierSIPH(pathOUT + "\\Rapport PBI SIPH " + str(environnement) + ".csv",environnement)
    with open(pathOUT + "\\Rapport PBI SIPH " + str(environnement) + ".csv", 'w', newline='') as csvfile:
        rapportSIPH = csv.writer(csvfile, delimiter=';', quotechar='|')
        rapportSIPH.writerow(headerSIPH)
        reporting.appel("FichiersRouteSIPH")
        memoireNumeroSillon = ""
        compteur = 0
        for n in range(len(listeFichiersRoute)) :
            reporting.progression(n+1,len(listeFichiersRoute))
            if listeFichiersRoute[n].split(".")[1] == "route" and sillonDuSA(listeFichiersRoute[n]) :
                if listeFichiersRoute[n].split("_")[0] == memoireNumeroSillon :
                    compteur += 1
                else :
                    compteur = 0
                fichierRoute = Route(pathRoute + "\\" + listeFichiersRoute[n],pathSIPH,listeFichiersSIPH,compteur)
                rapportCoordonnees = rapportCoordonnees + fichierRoute.GPS
                memoireNumeroSillon = listeFichiersRoute[n].split("_")[0]
                try :
                    donneesSillons.append([fichierRoute.numeroSillon,
                                       fichierRoute.secondNumeroSillon,
                                       fichierRoute.dateDebutValidite,
                                       fichierRoute.dateFinValidite,
                                       fichierRoute.dateActualisation,
                                       fichierRoute.completudeGPSSIRIUS,
                                       SIRIUS.inclusSIRIUS(fichierRoute.numeroSillon),
                                       fichierRoute.problematiqueDoubleSPD,
                                       fichierRoute.problematiqueTrouGEO,
                                       fichierRoute.TCT,
                                       TCT.Activite(fichierRoute.TCT),
                                       fichierRoute.origine,
                                       fichierRoute.destination,
                                       fichierRoute.materiel,
                                       fichierRoute.longueur,
                                       fichierRoute.travaux,
                                       fichierRoute.regimeDeuxSemaines[0],
                                       fichierRoute.regimeDeuxSemaines[1],
                                       fichierRoute.regimeDeuxSemaines[2],
                                       fichierRoute.regimeDeuxSemaines[3],
                                       fichierRoute.regimeDeuxSemaines[4],
                                       fichierRoute.regimeDeuxSemaines[5],
                                       fichierRoute.regimeDeuxSemaines[6],
                                       fichierRoute.regimeDeuxSemaines[7],
                                       fichierRoute.regimeDeuxSemaines[8],
                                       fichierRoute.regimeDeuxSemaines[9],
                                       fichierRoute.regimeDeuxSemaines[10],
                                       fichierRoute.regimeDeuxSemaines[11],
                                       fichierRoute.regimeDeuxSemaines[12],
                                       fichierRoute.regimeDeuxSemaines[13],
                                       fichierRoute.fichierRoute.split("\\")[-1],
                                       fichierRoute.fichierSIPH,
                                       compteur
                                       ])
                except :
                    pass
                    # donneesSillons.append([fichierRoute.numeroSillon,
                    #                    fichierRoute.secondNumeroSillon,
                    #                    fichierRoute.dateDebutValidite,
                    #                    fichierRoute.dateFinValidite,
                    #                    fichierRoute.dateActualisation,
                    #                    fichierRoute.completudeGPSSIRIUS,
                    #                    SIRIUS.inclusSIRIUS(fichierRoute.numeroSillon),
                    #                    fichierRoute.problematiqueDoubleSPD,
                    #                    fichierRoute.problematiqueTrouGEO,
                    #                    fichierRoute.TCT,
                    #                    TCT.Activite(fichierRoute.TCT),
                    #                    fichierRoute.origine,
                    #                    fichierRoute.destination,
                    #                    fichierRoute.materiel,
                    #                    fichierRoute.longueur,
                    #                    fichierRoute.travaux,
                    #                    "","","","","","","","","","","","","","",
                    #                    fichierRoute.fichierRoute.split("\\")[-1],
                    #                    "",
                    #                    compteur
                    #                    ])
                # print(donneesSillons)
                try :
                    if sillonRoule(donneesSillons[-1]) == "True" :
                        donneesGPS.append([fichierRoute.numeroSillon,compteur,fichierRoute.completudeGPSSIRIUS,fichierRoute.trajet])
                        donneesTrajet.append([fichierRoute.numeroSillon,compteur,fichierRoute.gares])
                except :
                    pass
        for i in range(len(donneesSillons)) :
            if sillonRoule(donneesSillons[i]) == "True" :
                rapportSIPH.writerow(donneesSillons[i])
        #print(rapportCoordonnees)
    #os.system("pause")
    
    ### Création du fichier des lignes / voies ###
    # reporting.appel("RapportGPS")
    # archive.ArchivageFichierGPS(pathOUT + "\\Rapport GPS.csv")
    # with open(pathOUT + "\\Rapport GPS.csv", 'w', newline='') as csvfile:
    #     rapportGPS = csv.writer(csvfile, delimiter=';', quotechar='|')
    #     rapportGPS.writerow(headerGPS)
    #     tempGPS = []
    #     for i in range(len(donneesGPS)) :
    #         for n in range(len(donneesGPS[i][3])) :
    #             resultat = "-"                
    #             try :
    #                 resultat = inclusREFTRA(donneesGPS[i][3][n][0],donneesGPS[i][3][n][2],donneesGPS[i][3][n][3],GPSREFTRA.Acquisition())
    #                 tempGPS.append([donneesGPS[i][0],donneesGPS[i][1],donneesGPS[i][2],donneesGPS[i][3][n][0],donneesGPS[i][3][n][1],donneesGPS[i][3][n][2],donneesGPS[i][3][n][3],resultat])
    #             except:
    #                 pass
    #     for i in range(len(tempGPS)) :
    #         rapportGPS.writerow(tempGPS[i])
        
    ### Création du fichier GPS ###
    with open(pathOUT + "\\Rapport Coordonnées.csv", 'w', newline='') as csvfile:
        fichierCoordonnees = csv.writer(csvfile, delimiter=';', quotechar='|')
        fichierCoordonnees.writerow(headerCoordonnees)
        for i in range(len(rapportCoordonnees)) :
            fichierCoordonnees.writerow(rapportCoordonnees[i])
        
    ### Création du fichier trajet ###
    reporting.appel("RapportTrajet")
    archive.ArchivageFichierTrajet(pathOUT + "\\Rapport Trajet.csv")
    with open(pathOUT + "\\Rapport Trajet.csv", 'w', newline='') as csvfile:
        rapportTrajet = csv.writer(csvfile, delimiter=';', quotechar='|')
        rapportTrajet.writerow(headerTrajet)
        for i in range(len(donneesTrajet)) :
            for n in range(len(donneesTrajet[i][2])):
                rapportTrajet.writerow([donneesTrajet[i][0],donneesTrajet[i][1],donneesTrajet[i][2][n][0]])



    reporting.appel("Version")
    #...


    reporting.appel("Fin")
    #exit()



###################################################
### Programme 2 : Actualisation des données ADC ###
###################################################

if int(programme) == 2 :
    
    pathIN = rootPath + "\IN"
    pathOUT = rootPath + "\OUT"
    fichierADC = listeFichiersIN + "ADC OC.xlsx"
    
    
    
###################################################
### Programme 3 : Actualisation des données GPS ###
###################################################

if int(programme) == 3 :
    
    pathIN = rootPath + "\IN\\"
    pathOUT = rootPath + "\OUT"
    pathArchivesREFTRA = rootPath + "\Archives\REFTRA binaire"
    fichierREFTRA = pathIN + "GPS_REFTRA.csv"
    
    ### Création du fichier binaire GPS ###
    with open(pathArchivesREFTRA + "\\" + "GPSREFTRA.pickle", "wb") as f :
        reporting.appel("MAJGPS")
        REFTRA = GPS(fichierREFTRA)
        REFTRA = REFTRA.Acquisition()
        pickle.dump(REFTRA, f)
        reporting.appel("FinMAJGPS")
        reporting.appel("Fin")
        