""" Created by Guillaume WELLER : 03/12/2020 """

######### ######### ######### ######### ####9#### ######### ######### ######### #########

import datetime
import time
import os
import shutil
import csv

class Debug:
    """ Classe permettant d'afficher des informations lors de l'utilisation d'un algorithme """

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
        #print("Created by Guillaume WELLER on 09/01/2020 \nLast modifications on 23/12/2020 by Guillaume WELLER\n")
        #print(self.appel_header(), "Début du programme...")
        
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

class Fonctions:
    """  """

    def __init__(self):
        self.rootPath = "rootPath"

    

    ### Fonctions de nettoyage - TTH Reader ###

    def concatenation(self,row):
            string = ""
            for i in range(len(row)) :
                if row[i] == "":
                    string = string + " "
                else :
                    string = string + row[i]
            return string

    def clean(self,listeA):
        listeTemp = []
        for i in range(len(listeA)) :
            temp = ""
            for j in range(len(listeA[i])) :
                if listeA[i][j] != " " :
                    temp = temp + listeA[i][j]
            listeTemp.append(temp)
        return listeTemp

    def cleanString(self,string) :
        stringTemp = ""
        for i in range(len(string)) :
            if string[i] != " " :
                stringTemp = stringTemp + string[i]
        return stringTemp

    def cleaned7H(self) :
        self.dataSillon7H_cleaned = []
        del self.dataSillon7H[0]
        for i in range(len(self.dataSillon7H)) :
            self.dataSillon7H_cleaned.append([self.dataSillon7H[i][0], self.dataSillon7H[i][1], []])
            temp = self.dataSillon7H[i][2]
            for j in range(int(len(temp)/2)) :
                if temp[2*j][6] == "1" :
                    temp[2*j][6] = "Ascending"
                else :
                    temp[2*j][6] = "Descending"
                self.dataSillon7H_cleaned[i][2].append([temp[2*j][7], temp[2*j][3], temp[2*j][2], temp[2*j][5], temp[2*j][4], temp[2*j][1], temp[2*j+1][1], temp[2*j][6]])
        return self.dataSillon7H_cleaned

    def parcours(self,liste):
        temp = []
        for i in range(len(liste)) :
            temp.append()
        return temp

    def parcoursSillon(self,liste):
        temp = []
        for i in range(len(liste)) :
            temp.append(liste[i][3])
        return temp

    def correspondance(self, parcours, parcoursSignaux) :
        numeroSignal = []

        for i in range(len(parcoursSignaux)) :
            flag = 0
            for k in range(len(parcoursSignaux[i])) :
                try :
                    #print("a",parcoursSignaux[i][k])
                    if parcours[k] == parcoursSignaux[i][k] :
                        #print("b",parcours[k])
                        flag = flag + 1
                except :
                    pass
            if flag >= 2 :
                numeroSignal.append(i)
        return numeroSignal
        
    def test(self, A7H, vitesses) :
        pkDebut = int(A7H[5])
        pkFin = int(A7H[6])
        sens = A7H[7]
        sectionDebut = -1
        sectionFin = -1
        suiteVitesses = []
        #print("Longueur vitesse", len(vitesses))
        
        for l in range(len(vitesses)) :
            #print("a :",float(vitesses[l][0])*1000)
            #print("b :",pkDebut)
            #print("c :",float(vitesses[l][1])*1000)
            if round(float(vitesses[l][0])*1000) <= pkDebut <= round(float(vitesses[l][1])*1000) :
                sectionDebut = l
            #else :
                #print("Début non trouvé")
            #print("Fin de section :",float(vitesses[l][1])*1000)
            if round(float(vitesses[l][0])*1000) <= pkFin <= round(float(vitesses[l][1])*1000+1) :
                sectionFin = l
            #else :
                #print("Fin non trouvé")
        return [sectionDebut, sectionFin]


    def triVitesses(self, A7H, vitesses) :
        pkDebut = int(A7H[5])
        pkFin = int(A7H[6])
        sens = A7H[7]
        #print("debug :", pkDebut, pkFin)
        sectionDebut = -1
        sectionFin = -1
        suiteVitesses = []
        #print(vitesses)
        for l in range(len(vitesses)) :
            if round(float(vitesses[l][0])*1000) <= pkDebut <= round(float(vitesses[l][1])*1000) :
                sectionDebut = l
            #else :
                #print("Début non trouvé")
            #print("Fin de section :",int(float(vitesses[l][1])*1000))

            #print(format(float(vitesses[l][1])*1000, '.2f'))

            if round(float(vitesses[l][0])*1000) <= pkFin <= round(float(vitesses[l][1])*1000) :
                sectionFin = l
            #else :
                #print("Fin non trouvé")
        #print("debug 1:",sectionDebut, sectionFin)
        #print("debug 2 :", vitesses)
        if sectionDebut == sectionFin :
            print("Sections :", sectionDebut, sectionFin)
            print("Pks :", pkDebut, pkFin)
            suiteVitesses.append([pkDebut, vitesses[sectionDebut][3], pkFin, sens])
        
        
        else :
            
            #print("HAHAHAHA",sectionDebut, sectionFin)
            if sens == "Ascending" :
                for n in range(sectionDebut, sectionFin + 1) :
                    #print("AAA",n)
                    #print(sens)

                    ### Sens ascendant ###
                    if n == sectionDebut and sens == "Ascending" :
                        suiteVitesses.append([pkDebut, vitesses[n][3] ,float(vitesses[n][1])*1000, "Ascending"])
                    elif n == sectionFin and sens == "Ascending" :
                        suiteVitesses.append([float(vitesses[n][0])*1000, vitesses[n][3], pkFin, "Ascending"])
                    elif n != sectionDebut and n != sectionFin and sens == "Ascending" :
                        suiteVitesses.append([float(vitesses[n][0])*1000, vitesses[n][3], float(vitesses[n][1])*1000, "Ascending"])

                ###Sens descendant ###
            else :
                #print("aaaaa")
                for n in range(sectionDebut, sectionFin - 1,-1) :
                    #print("Ceci est n :",n)
                    inverse = len(vitesses)
                    m = n
                    #print("m :",n)

                    #print("BBB", inverse, k)
                    if m == sectionDebut :
                        suiteVitesses.append([pkDebut, vitesses[m][3], float(vitesses[m][0])*1000, "Descending"])
                    elif m == sectionFin :
                        suiteVitesses.append([float(vitesses[m][1])*1000, vitesses[m][3], pkFin, "Descending"])
                    elif m != sectionDebut and m != sectionFin :
                        suiteVitesses.append([float(vitesses[m][1])*1000, vitesses[m][3], float(vitesses[m][0])*1000, "Descending"])

        ### Supprimer les doublons de vitesses dus aux changement de SRV ###
        listeTemp = []
        memoireVitesse = ""    
        for i in range(len(suiteVitesses)) :
        
            if suiteVitesses[i][1] != memoireVitesse :
                listeTemp.append(i)
            memoireVitesse = suiteVitesses[i][1]
        #print(listeTemp)
        #print("a",suiteVitesses)
        return suiteVitesses

    def testTrajet(self, parcoursSillon, parcoursSignal) :
        longueur = 0
        flag = "False"
        for j in range(len(parcoursSillon)) :
            if parcoursSignal[0] == parcoursSillon[j] :
                try :
                    if parcoursSignal[1] == parcoursSillon[j+1] :
                        flag = "True"
                        longueur = 1
                        try :
                            if parcoursSignal[2] == parcoursSillon[j+2] :
                                longueur = 2
                                try :
                                    if parcoursSignal[3] == parcoursSillon[j+3] :
                                        longueur = 3
                                        try :
                                            if parcoursSignal[4] == parcoursSillon[j+4] :
                                                longueur = 4
                                        except :
                                            pass
                                except :
                                    pass
                        except :
                            pass
                except :
                    pass
        return [flag, longueur]

    def selectionSignaux (self, trajet, signaux, k) :
        #print('\n', "Couple ligne / voie n° :", k + 1)
        signauxConcernes = []
        #print("Numéro de voie :", k)
        #print("Trajet à comparer" ,trajet)
        #print(trajet[k])
        #print(trajet[k][5])
        #for i in range(len(signaux)) :
            #print(signaux[i])
            #print(len(signaux[i]))
        
        parcours = self.parcoursSillon(trajet)
        j = 0
        for signal in signaux :
            j = j + 1
            for n in range(len(signal)//3) :
                #print("a",signal[3*n+2])
                if len(signal[3*n+2]) == 1 :#and signal[3*n+2][0] == parcours[k] :
                    #print("Signal sur une seule voie", signal[3*n], signal[3*n+1], signal[3*n+2])
                    #print("aaa",k)
                    #print("Trajetttt", trajet[k][5], k)
                    pkd = trajet[k][5]
                    pkf = trajet[k][6]
                    sens = trajet[k][7]
                    #print("A", sens)
                    if sens == "Ascending" :
                        #print("Debug A :")
                        #print(int(pkf), int(float(signal[3*n+2][1])*1000), int(pkd))
                        if int(pkd) <= int(float(signal[3*n+2][0][1])*1000) <= int(pkf) :
                            signauxConcernes.append([signal, n, 0])
                    else :
                        #print("Debug D :")
                        #print(signal[3*n+2])
                        if int(pkf) <= int(float(signal[3*n+2][0][1])*1000) <= int(pkd) :
                            signauxConcernes.append([signal, n, 0])
                else :
                    parcoursSignal = []
                    for m in range(len(signal[3*n+2])) :
                        parcoursSignal.append(signal[3*n+2][m][0])
                    if self.testTrajet(parcours, parcoursSignal)[0] == "True" :
                        signauxConcernes.append([signal,n,self.testTrajet(parcours, parcoursSignal)[1]])
        return signauxConcernes


            #for j in range(int(len(signaux[i])/3)) :
                #if len(signaux[i][3*j+2]) == 1 :
                    #print("Signal sur une seule voie", signaux[i][3*j], signaux[i][3*j+1], signaux[i][3*j+2])


    def diminutionVitesseSignaux (self, dataVitesses, signal, parcours):
        """
        Entrées : listes de listes + numéro du SRV
        """

        #chgmtVoiesSillon = self.parcoursSillon(trajet)
        #print('\n', "Couple ligne / voie n° :", k)
        #print(parcours)
        for typeSignal in signal :
            indice = typeSignal[-2]
            longueur = typeSignal[-1]
            print("\n")#"Indice :", indice)
            print("Type :", typeSignal)
            SRV = []
            vitesse = []
            pkDebutReseau = []
            pkFinReseau = []
            for i in range(longueur+1) :

                SRV.append(typeSignal[0][3*indice+2][i][0])
                vitesse.append(typeSignal[0][3*indice])
                pkDebutReseau.append(float(typeSignal[0][3*indice+2][i][1])*1000)
                pkFinReseau.append(float(typeSignal[0][3*indice+2][i][2])*1000)
                if float(typeSignal[0][3*indice+2][i][2])*1000 - float(typeSignal[0][3*indice+2][i][1])*1000 > 0 :
                    sens = "Ascending"
                else :
                    sens = "Descending"
            print("SRV et pks :", SRV, vitesse, pkDebutReseau, pkFinReseau)
            numeroSection = -1
            for i in range(len(parcours)) :
                if SRV[0] == parcours[i] :
                    numeroSection = i
                    break
            print(numeroSection)
            print("Section à modifier :",dataVitesses[numeroSection])
            sectionDebut = -1
            sectionFin = -1
            if len(SRV) == 1 and numeroSection != -1 :
                for i in range(len(dataVitesses[numeroSection])) :
                    if sens == "Ascending" :
                        if dataVitesses[numeroSection][i][0] <= int(pkDebutReseau[0]) <= dataVitesses[numeroSection][i][2] :
                            sectionDebut = i
                        if dataVitesses[numeroSection][i][0] <= int(pkFinReseau[0]) <= dataVitesses[numeroSection][i][2] :
                            sectionFin = i
                    else :
                        if dataVitesses[numeroSection][i][2] <= int(pkDebutReseau[0]) <= dataVitesses[numeroSection][i][0] :
                            sectionDebut = i
                        if dataVitesses[numeroSection][i][2] <= int(pkFinReseau[0]) <= dataVitesses[numeroSection][i][0] :
                            sectionFin = i
                
                
                print("A modifier :",sectionDebut, sectionFin)
                #print(dataVitesses[numeroSection][i][0], int(pkDebutReseau[0]))
                #print(dataVitesses[numeroSection][i][0] <= int(pkDebutReseau[0]))
                temp = []

                if sectionDebut == sectionFin :
                    for j in range(len(dataVitesses[numeroSection])) :
                        if j == sectionDebut :
                            temp.append([dataVitesses[numeroSection][j][0], dataVitesses[numeroSection][j][1], int(pkDebutReseau[0]), sens])
                            temp.append([int(pkDebutReseau[0]), vitesse[0], int(pkFinReseau[0]), sens])
                            temp.append([int(pkFinReseau[0]), dataVitesses[numeroSection][j][1], dataVitesses[numeroSection][j][2], sens])
                        else :
                            temp.append(dataVitesses[numeroSection][j])
                #elif sectionDebut ==
                else :
                    if sens == "Ascending" :
                        if sectionFin == -1 :
                            for n in range(sectionDebut + 1) : #len(dataVitesses[numeroSection])) :#sectionDebut, sectionFin + 1) :
                                if n != sectionDebut :
                                    temp.append(dataVitesses[numeroSection][n])
                                if n == sectionDebut :
                                    temp.append([dataVitesses[numeroSection][n][0],dataVitesses[numeroSection][n][1], int(pkDebutReseau[0]), sens])
                                    temp.append([int(pkDebutReseau[0]),vitesse[0], dataVitesses[numeroSection][n][2], sens])
                        #temp.append([int(pkDebutReseau[0]), vitesse[0], int(pkFinReseau[0]), sens])
                        else :
                            for n in range(sectionDebut + 1) : #len(dataVitesses[numeroSection])) :#sectionDebut, sectionFin + 1) :
                                if n != sectionDebut :
                                    temp.append(dataVitesses[numeroSection][n])
                            ### Sens ascendant ###
                                if n == sectionDebut :
                                    temp.append([dataVitesses[numeroSection][n][0], dataVitesses[numeroSection][n][1], int(pkDebutReseau[0]), sens])
                            temp.append([int(pkDebutReseau[0]), vitesse[0], int(pkFinReseau[0]), sens])
                            for n in range(sectionFin, len(dataVitesses[numeroSection])) :
                                #print("n = ", n)
                                if n == sectionFin :
                                    if int(pkFinReseau[0]) >= dataVitesses[numeroSection][n][2] :
                                        pass #temp.append([int(pkFinReseau[0]), dataVitesses[numeroSection][n][1], dataVitesses[numeroSection][n][2], sens])
                                    else :
                                        temp.append([int(pkFinReseau[0]), dataVitesses[numeroSection][n][1], dataVitesses[numeroSection][n][2], sens])
                                #elif 
                                else :
                                    temp.append(dataVitesses[numeroSection][n])
                    else :
                        if sectionFin == -1 :
                            for n in range(sectionDebut + 1) : #len(dataVitesses[numeroSection])) :#sectionDebut, sectionFin + 1) :
                                if n != sectionDebut :
                                    temp.append(dataVitesses[numeroSection][n])
                                if n == sectionDebut :
                                    temp.append([dataVitesses[numeroSection][n][0],dataVitesses[numeroSection][n][1], int(pkDebutReseau[0]), sens])
                                    temp.append([int(pkDebutReseau[0]),vitesse[0], dataVitesses[numeroSection][n][2], sens])
                        else :
                            for n in range(sectionDebut + 1) : #len(dataVitesses[numeroSection])) :#sectionDebut, sectionFin + 1) :
                                if n != sectionDebut :
                                    temp.append(dataVitesses[numeroSection][n])
                            ### Sens descendant ###
                                if n == sectionDebut :
                                    temp.append([dataVitesses[numeroSection][n][0],dataVitesses[numeroSection][n][1], int(pkDebutReseau[0]), sens])
                            temp.append([int(pkDebutReseau[0]), vitesse[0], int(pkFinReseau[0]), sens])
                            for n in range(sectionFin, len(dataVitesses[numeroSection])) :
                                if n == sectionFin :
                                    temp.append([int(pkFinReseau[0]), dataVitesses[numeroSection][n][1], dataVitesses[numeroSection][n][2], sens])
                            ### Sens descendant ###
                                else :
                                    temp.append(dataVitesses[numeroSection][n])
                #print("Ceci est le temp :",temp)
                dataVitesses[numeroSection] = temp
                print("Section modifiée :",dataVitesses[numeroSection])

        return dataVitesses

    def diminutionVitesseSignaux1 (self, dataVitesses, signal, parcours):
        """
        Entrées : listes de listes + numéro du SRV
        """

        #chgmtVoiesSillon = self.parcoursSillon(trajet)
        #print('\n', "Couple ligne / voie n° :", k)
        #print(parcours)
        for typeSignal in signal :
            indice = typeSignal[-2]
            longueur = typeSignal[-1]
            print("\n")#"Indice :", indice)
            print("Type :", typeSignal)
            SRV = []
            vitesse = []
            pkDebutReseau = []
            pkFinReseau = []
            for i in range(longueur+1) :

                SRV.append(typeSignal[0][3*indice+2][i][0])
                vitesse.append(typeSignal[0][3*indice])
                pkDebutReseau.append(float(typeSignal[0][3*indice+2][i][1])*1000)
                pkFinReseau.append(float(typeSignal[0][3*indice+2][i][2])*1000)
                if float(typeSignal[0][3*indice+2][i][2])*1000 - float(typeSignal[0][3*indice+2][i][1])*1000 > 0 :
                    sens = "Ascending"
                else :
                    sens = "Descending"
            print("SRV et pks :", SRV, vitesse, pkDebutReseau, pkFinReseau)
            numeroSection = -1
            for i in range(len(parcours)) :
                if SRV[0] == parcours[i] :
                    numeroSection = i
                    break
            print(numeroSection)
            print("Section à modifier :",dataVitesses[numeroSection])
            sectionDebut = -1
            sectionFin = -1
            if len(SRV) == 1 and numeroSection != -1 :
                pass
            elif numeroSection != -1 :
                #if 
                pass
            for d in range(len(SRV)) :
                for i in range(len(dataVitesses[numeroSection+d])) :
                    if sens == "Ascending" :
                        if dataVitesses[numeroSection][i][0] <= int(pkDebutReseau[0]) <= dataVitesses[numeroSection][i][2] :
                            sectionDebut = i
                        if dataVitesses[numeroSection][i][0] <= int(pkFinReseau[0]) <= dataVitesses[numeroSection][i][2] :
                            sectionFin = i
                    else :
                        if dataVitesses[numeroSection][i][2] <= int(pkDebutReseau[0]) <= dataVitesses[numeroSection][i][0] :
                            sectionDebut = i
                        if dataVitesses[numeroSection][i][2] <= int(pkFinReseau[0]) <= dataVitesses[numeroSection][i][0] :
                            sectionFin = i
                
                
                print("A modifier :",sectionDebut, sectionFin)
                print(dataVitesses[numeroSection][i][0], int(pkDebutReseau[0]))
                print(dataVitesses[numeroSection][i][0] <= int(pkDebutReseau[0]))
                temp = []

                if sectionDebut == sectionFin :
                    for j in range(len(dataVitesses[numeroSection])) :
                        if j == sectionDebut :
                            temp.append([dataVitesses[numeroSection][j][0], dataVitesses[numeroSection][j][1], int(pkDebutReseau[0]), sens])
                            temp.append([int(pkDebutReseau[0]), vitesse[0], int(pkFinReseau[0]), sens])
                            temp.append([int(pkFinReseau[0]), dataVitesses[numeroSection][j][1], dataVitesses[numeroSection][j][2], sens])
                        else :
                            temp.append(dataVitesses[numeroSection][j])
                else :
                    if sens == "Ascending" :
                        for n in range(sectionDebut + 1) : #len(dataVitesses[numeroSection])) :#sectionDebut, sectionFin + 1) :
                            if n != sectionDebut :
                                temp.append(dataVitesses[numeroSection][n])
                        ### Sens ascendant ###
                            if n == sectionDebut :
                                temp.append([dataVitesses[numeroSection][n][0],dataVitesses[numeroSection][n][1],  int(pkDebutReseau[0]), sens])
                        temp.append([int(pkDebutReseau[0]), vitesse[0], int(pkFinReseau[0]), sens])
                        for n in range(sectionFin, len(dataVitesses[numeroSection])) :
                            if n == sectionFin :
                                temp.append([int(pkFinReseau[0]), dataVitesses[numeroSection][n][1], dataVitesses[numeroSection][n][2], sens])
                            else :
                                temp.append(dataVitesses[numeroSection][n])
                    else :
                        for n in range(sectionDebut + 1) : #len(dataVitesses[numeroSection])) :#sectionDebut, sectionFin + 1) :
                            if n != sectionDebut :
                                temp.append(dataVitesses[numeroSection][n])
                        ### Sens ascendant ###
                            if n == sectionDebut :
                                temp.append([dataVitesses[numeroSection][n][0],dataVitesses[numeroSection][n][1],  int(pkDebutReseau[0]), sens])
                        temp.append([int(pkDebutReseau[0]), vitesse[0], int(pkFinReseau[0]), sens])
                        for n in range(sectionFin, len(dataVitesses[numeroSection])) :
                            if n == sectionFin :
                                temp.append([int(pkFinReseau[0]), dataVitesses[numeroSection][n][1], dataVitesses[numeroSection][n][2], sens])
                        ### Sens ascendant ###
                            else :
                                temp.append(dataVitesses[numeroSection][n])
                #print("Ceci est le temp :",temp)
                dataVitesses[numeroSection] = temp
                print("Section modifiée :",dataVitesses[numeroSection])

        return dataVitesses
            
            
    def triGradient(self, A7H, gradients) :
        pkDebut = int(A7H[5])
        pkFin = int(A7H[6])
        sectionDebut = -1
        sectionFin = -1
        suiteGradients = []
        sens = A7H[7]
        #print("gradients",gradients)
        for l in range(len(gradients)) :
            #print("comparaison",gradients[l])
            if float(gradients[l][0])*1000 <= pkDebut <= float(gradients[l][1])*1000 :
                sectionDebut = l
            #else :
                #print("Début non trouvé")
            if float(gradients[l][0])*1000 <= pkFin <= float(gradients[l][1])*1000 :
                sectionFin = l
            #else :
                #print("Fin non trouvé")
        #Si aucun gradient n'est trouvé
        if sectionDebut == sectionFin and sectionFin == -1:
            return []
        ### Sens Ascendant ###
        elif sens == "Ascending" :
            if sectionDebut == sectionFin :
                suiteGradients.append([pkDebut, "{0:f}".format(float(gradients[sectionDebut][2])*(pkFin-pkDebut)/1000), pkFin])
            #Si on ne trouve pas la fin des gradients car liste incomplète
            elif sectionFin==-1 :
                suiteGradients.append([pkDebut, "{0:f}".format(float(gradients[sectionDebut][2])*(float(gradients[sectionDebut][1])*1000-pkDebut)/1000) ,int(float(gradients[sectionDebut][1])*1000)])
                suiteGradients.append([int(float(gradients[sectionDebut][1])*1000), 0 ,pkFin])
            #Si on ne trouve pas le début des gradients car liste incomplète
            elif sectionDebut==-1 :
                suiteGradients.append([pkDebut, 0 ,int(float(gradients[sectionFin][0])*1000)])
                suiteGradients.append([int(float(gradients[sectionFin][0])*1000), "{0:f}".format(float(gradients[sectionFin][2])*(pkFin-float(gradients[sectionFin][0])*1000)/1000) ,pkFin])
            else :
                for n in range(sectionDebut, sectionFin + 1) :
                    if n == sectionDebut :
                        suiteGradients.append([pkDebut, "{0:f}".format(float(gradients[n][2])*(float(gradients[n][1])*1000-pkDebut)/1000) ,int(float(gradients[n][1])*1000)])
                    elif n == sectionFin :
                        suiteGradients.append([int(float(gradients[n][0])*1000), "{0:f}".format(float(gradients[n][2])*(pkFin-float(gradients[n][0])*1000)/1000), pkFin])
                    elif n != sectionDebut and n != sectionFin :
                        suiteGradients.append([int(float(gradients[n][0])*1000), "{0:f}".format(float(gradients[n][2])*(float(gradients[n][1])*1000-float(gradients[n][0])*1000)/1000), int(float(gradients[n][1])*1000)])
        
        ### Sens Descendant ###
        else :
            if sectionDebut == sectionFin :
                suiteGradients.append([pkDebut, "{0:f}".format(float(gradients[sectionDebut][2])*(pkFin-pkDebut)/1000), pkFin])
            elif sectionFin==-1 :
                suiteGradients.append([pkDebut, "{0:f}".format(float(gradients[sectionDebut][2])*(float(gradients[sectionDebut][0])*1000-pkDebut)/1000) ,int(float(gradients[sectionDebut][0])*1000)])
                suiteGradients.append([int(float(gradients[sectionDebut][0])*1000), 0 ,pkFin])
            elif sectionDebut==-1 :
                suiteGradients.append([pkDebut, 0 ,int(float(gradients[sectionFin][1])*1000)])
                suiteGradients.append([int(float(gradients[sectionFin][1])*1000), "{0:f}".format(float(gradients[sectionDebut][2])*(pkFin-float(gradients[sectionFin][1])*1000)/1000) ,pkFin])
            else :
                for n in range(sectionDebut, sectionFin + 1,-1) :
                    if n == sectionDebut :
                        suiteGradients.append([pkDebut, "{0:f}".format(float(gradients[n][2])*(float(gradients[n][0])*1000-pkDebut)/1000) ,int(float(gradients[n][0])*1000)])
                    elif n == sectionFin :
                        suiteGradients.append([int(float(gradients[n][1])*1000), "{0:f}".format(float(gradients[n][2])*(float(gradients[n][1])*1000-pkFin)/1000),pkFin])
                    elif n != sectionDebut and n != sectionFin :
                        suiteGradients.append([int(float(gradients[n][1])*1000), "{0:f}".format(float(gradients[n][2])*(float(gradients[n][0])*1000-float(gradients[n][1])*1000)/1000), int(float(gradients[n][0])*1000)])


        return suiteGradients
        

    def triRadiuses(self, A7H, radiuses) :
        pkDebut = int(A7H[5])
        pkFin = int(A7H[6])
        sectionDebut = -1
        sectionFin = -1
        suiteRadiuses = []
        sens = A7H[7]
        for l in range(len(radiuses)) :
            if float(radiuses[l][0])*1000 <= pkDebut <= float(radiuses[l][1])*1000 :
                sectionDebut = l
            #else :
                #print("Début non trouvé")
            if float(radiuses[l][0])*1000 <= pkFin <= float(radiuses[l][1])*1000 :
                sectionFin = l
            #else :
                #print("Fin non trouvé")
        #Si aucun radius n'est trouvé
        if sectionDebut == sectionFin and sectionFin == -1:
            return []
        ### Sens Ascendant ###
        elif sens == "Ascending":
            if sectionDebut == sectionFin :
                if int(radiuses[sectionDebut][2]) == 0 :
                    suiteRadiuses.append([pkDebut, 0, pkFin])
                else :
                    suiteRadiuses.append([pkDebut, 1/int(radiuses[sectionDebut][2]), pkFin])
            #Si on ne trouve pas la fin des radius car liste incomplète
            elif sectionFin==-1 :
                if int(radiuses[sectionDebut][2])==0:
                    valradius=0
                else:
                    valradius="{0:f}".format(1/int(radiuses[sectionDebut][2]))
                    suiteRadiuses.append([pkDebut, valradius ,int(float(radiuses[sectionDebut][1])*1000)])
                suiteRadiuses.append([int(float(radiuses[sectionDebut][1])*1000), 0 ,pkFin])
            #Si on ne trouve pas le début des radius car liste incomplète
            elif sectionDebut==-1 :
                suiteRadiuses.append([pkDebut, 0 ,int(float(radiuses[sectionFin][0])*1000)])
                if int(radiuses[sectionFin][2])==0:
                    valradius=0
                else:
                    valradius="{0:f}".format(1/int(radiuses[sectionFin][2]))
                    suiteRadiuses.append([int(float(radiuses[sectionFin][0])*1000), valradius ,pkFin])
            else :
                for n in range(sectionDebut, sectionFin + 1) :
                    if n == sectionDebut :
                        if int(radiuses[n][2])==0:
                            valradius=0
                        else:
                            valradius="{0:f}".format(1/int(radiuses[n][2]))
                        suiteRadiuses.append([pkDebut, valradius ,int(float(radiuses[n][1])*1000)])
                    elif n == sectionFin :
                        if int(radiuses[n][2])==0:
                            valradius=0
                        else:
                            valradius="{0:f}".format(1/int(radiuses[n][2]))
                        suiteRadiuses.append([int(float(radiuses[n][0])*1000), valradius, pkFin])
                    elif n != sectionDebut and n != sectionFin :
                        if int(radiuses[n][2])==0:
                            valradius=0
                        else:
                            valradius="{0:f}".format(1/int(radiuses[n][2]))
                        suiteRadiuses.append([int(float(radiuses[n][0])*1000), valradius, int(float(radiuses[n][1])*1000)])

        ### Sens Descendant ###
        else :
            if sectionDebut == sectionFin :
                if int(radiuses[sectionDebut][2]) == 0 :
                    suiteRadiuses.append([pkDebut, 0, pkFin])
                else :
                    suiteRadiuses.append([pkDebut, 1/int(radiuses[sectionDebut][2]), pkFin])
            elif sectionFin==-1 :
                if int(radiuses[sectionDebut][2])==0:
                    valradius=0
                else:
                    valradius="{0:f}".format(1/int(radiuses[sectionDebut][2]))
                    suiteRadiuses.append([pkDebut, valradius ,int(float(radiuses[sectionDebut][0])*1000)])
                suiteRadiuses.append([int(float(radiuses[sectionDebut][0])*1000), 0 ,pkFin])
            elif sectionDebut==-1 :
                suiteRadiuses.append([pkDebut, 0 ,int(float(radiuses[sectionFin][1])*1000)])
                if int(radiuses[sectionFin][2])==0:
                    valradius=0
                else:
                    valradius="{0:f}".format(1/int(radiuses[sectionFin][2]))
                    suiteRadiuses.append([int(float(radiuses[sectionFin][1])*1000), valradius ,pkFin])
            else :
                for n in range(sectionDebut, sectionFin + 1,-1) :
                    if n == sectionDebut :
                        if int(radiuses[n][2])==0:
                            valradius=0
                        else:
                            valradius="{0:f}".format(1/int(radiuses[n][2]))
                        suiteRadiuses.append([pkDebut, valradius ,int(float(radiuses[n][0])*1000)])
                    elif n == sectionFin :
                        if int(radiuses[n][2])==0:
                            valradius=0
                        else:
                            valradius="{0:f}".format(1/int(radiuses[n][2]))
                        suiteRadiuses.append([int(float(radiuses[n][1])*1000), valradius, pkFin])
                    elif n != sectionDebut and n != sectionFin :
                        if int(radiuses[n][2])==0:
                            valradius=0
                        else:
                            valradius="{0:f}".format(1/int(radiuses[n][2])) 
                        suiteRadiuses.append([int(float(radiuses[n][1])*1000), valradius, int(float(radiuses[n][0])*1000)])


        return suiteRadiuses

    def doublons(self, liste):
        tri=[]
        try :
            tri.append(liste[0])
            for n in range (1,len(liste)):
                if liste[n][1]!=tri[-1][1]:
                    tri.append(liste[n])
            return tri
        except :
            return liste

            