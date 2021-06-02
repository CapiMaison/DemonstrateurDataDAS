""" Created by Guillaume WELLER on 09/01/2020 """
""" Last modifications on 23/12/2020 by Guillaume WELLER """

######### ######### ######### ######### ####9#### ######### ######### ######### #########

##########################
### Modules à importer ###
##########################

import os
import datetime
import csv
import pickle
from Classes import Debug, Fonctions
from TTHReader import Sillon#, HOUAT
from InfrastructureAcquisition import Infrastructure


rootPath = os.getcwd()

debug = Debug()
infrastructure = Infrastructure()
f = Fonctions()
#sillon = Sillon()



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

        self.sillonsTests1 = ["2836", "96721 non" ,"9211" ,"86092" ,"19905" ,"SOUS70" ,"PILE72" 
        ,"147158" ,"122300" ,"153704 non" ,"118499" 
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
                        print(self.sillonsHOUAT[-1].numeroSillon)
                        flag = 0
                        for i in range(len(self.sillonsTests)):
                            
                            if self.sillonsHOUAT[-1].numeroSillon == self.sillonsTests[i] :
                                flag = flag + 1
                        if flag == 0 :
                            self.sillonsHOUAT.pop()
                            print("Sillon enlevé")
                        #print(temp)
                        temp = []
                        temp.append(row)
                    else :
                        temp.append(row)
                        n =+ 1
        with open(self.dossierBinaire + "\CirculationTotale1.pickle", "wb") as binaryFile :
            pickle.dump(self.sillonsHOUAT, binaryFile)

    def chargementSillons(self) :
        with open(self.dossierBinaire + "\CirculationTotale.pickle", "rb") as binaryFile :
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
        with open(self.dossierBinaire + "\CirculationTotale1.pickle", "rb") as binaryFile :
            #print(len(pickle.load(binaryFile)))
            #print(len(pickle.load(binaryFile)))
            return pickle.load(binaryFile)


houat = HOUAT()
#houat.acquisitionSillons()

#for i in range(len(houat.sillonsHOUAT)):
#    print(houat.sillonsHOUAT[i].numeroSillon)

#for i in range(len(houat.sillonsHOUAT)) :
 #   numeroSillon = houat.sillonsHOUAT[i].dataSillon50[3]
    #print(i, numeroSillon)


##########################
### Variables globales ###
##########################

global ddSA 
ddSA = "2020-12-13"
global dfSA 
dfSA = "2021-12-10"



##########################
### Début du programme ###
##########################


### Récupération des données sillons du TTH ###

class Routes:
    """ Classe permettant de recueillir les informations -Route- des sillons"""

    def __init__(self):#sillons):
        
        
        #print(self.dataHoraire[1])
        vitessesVoies = infrastructure.chargementVitesses()
        radiusesVoies = infrastructure.chargementRadiuses()
        signauxVoies = infrastructure.chargementSignauxSpeedIndicators()
        gradientsVoies = infrastructure.chargementGradients()
        hierarchieIndiceCompo = infrastructure.chargementHierarchieIndiceCompo()
        #print(hierarchieIndiceCompo["E14P"])
        #print(signauxVoies["1525" , "Ascending"])
        #print("Signal :",signauxVoies["2" , "Ascending"])
        print("SRV 689 :",vitessesVoies["689" , "Descending"])
        print("SRV 687 :",vitessesVoies["687" , "Descending"])
        print("SRV 6006 :",vitessesVoies["6006" , "Descending"])
        print("SRV 5897 :",vitessesVoies["5897" , "Descending"])
        #print("SRV 9898 :",vitessesVoies["9898" , "Descending"])
        #print("SRV 11750 :",vitessesVoies["11750" , "Descending"])
        sillons = houat.chargementSillonsTests()
        #print(self.trajetsSillons)
        #print(vitessesVoies)
        
        self.nomsFichiers = []
        memoireNumeroSillon = ""
        variante = 0
        self.dataRoute = []

        


        for i in range(338,339):#len(sillons)) :#houat.sillonsHOUAT)) :
            self.trajetsSillons = sillons[i].cleaned7H() #houat.sillonsHOUAT[i].cleaned7H()
            #for j in range(len(self.trajetsSillons)) :
                #print(self.trajetsSillons[j])
            self.dataHoraire = sillons[i].dataSillon52 #houat.sillonsHOUAT[i].dataSillon52

            #print(houat.sillonsHOUAT[i].dataSillon50)
            numeroSillon = sillons[i].dataSillon50[3] #houat.sillonsHOUAT[i].dataSillon50[3]
            indiceCompo = sillons[i].dataSillon50[8] #houat.sillonsHOUAT[i].dataSillon50[8]
            print(numeroSillon)
            print(indiceCompo)
            #print("SRV 6006 :",vitessesVoies["6006" , "Descending"])

            if numeroSillon == memoireNumeroSillon :
                variante = variante + 1

            self.nomsFichiers.append(str(numeroSillon) + "_" + str(variante) + str(i) + ".route")
            

            ### Partie vitesses ###
            dataVitesses = []
            m = []
            m2 = []
            #print(self.trajetsSillons)
            for j in range(len(self.trajetsSillons)) :#[i][2])) :
                vitessesAssemblees = []
                print("Trajet : ", self.trajetsSillons[j])

                #for i in range(len(self.trajetsSillons)) :
                    #try :
                        #print(signauxVoies[self.trajetsSillons[i][3], self.trajetsSillons[i][-1]])
                    #except :
                        #pass


                vitessesSection = vitessesVoies[self.trajetsSillons[j][3], self.trajetsSillons[j][-1]]
                
                temp = []
                temp2 = []
                temp3 = []
                temp4 = []
                indiceAUtiliser = ""


                #for n in range(len(vitessesSection)) :
                #    if vitessesSection[n][2] == "T14C" :
                #        temp.append(vitessesSection[n])
                #f.test(self.trajetsSillons[j],temp)[0]

                try :
                    for indice in hierarchieIndiceCompo[indiceCompo] :
                        flag = "False"
                        temp = []
                        print("indice :",indice)
                        #while flag != "True" :
                        for n in range(len(vitessesSection)) :
                            if vitessesSection[n][2] == indice :
                                temp.append(vitessesSection[n])
                            #temp.append(vitessesSection[n])
                        #print("Test :", f.test(self.trajetsSillons[j],temp))
                        try :
                            if f.test(self.trajetsSillons[j],temp)[0] == -1 or f.test(self.trajetsSillons[j],temp)[1] == -1 :
                                pass
                            else :
                                flag = "True"
                                indiceAUtiliser = indice
                                break
                        except :
                            pass
                except :
                    indiceAUtiliser = ""
                #print("indice :",indiceAUtiliser)
                print("Indice à utiliser :", round(float(419.675)*1000))
                if indiceAUtiliser == "" :
                    for n in range(len(vitessesSection)) :
                        if vitessesSection[n][2] == "All" :
                            temp.append(vitessesSection[n])
                    #print("Utilisation du All")
                print("Temporaire :", temp)
                
                    #print("Section nulle")
                #print(self.trajetsSillons[j], temp)
                #if self.trajetsSillons[j][3] == "9898" :
                #print("Temporaire :" ,temp)
                #print(temp)
                #try :
                vitessesAssemblees = f.triVitesses(self.trajetsSillons[j], temp)
                #except :
                    #vitessesAssemblees = [[int(self.trajetsSillons[j][5]), "0", int(self.trajetsSillons[j][6]), self.trajetsSillons[j][-1]]]

                #print("Infrastructure : ", temp)
                m.append(temp)
                m2.append(temp2)

                dataVitesses.append(vitessesAssemblees)

                #print("Vitesses assemblées : ", dataVitesses)
            
            ### Création données propres Route (vitesses) ###
            
            vitessesSillon = []
            
            print("Datavitesse : ", dataVitesses)
            #print("\n")
            #for k in range(len(vitessesSillon)) :
            #print("SPD : ", vitessesSillon[k])


                #print(sectionDebut, sectionFin)

            

            #print("\n","\n")
                
            ###########################for k in range(len(m)) :
                ################################print("Infrastructure : ", m[k])
            #for k in range(len(m2)) :
                #print("Infrastructure 2 : ", m2[k])

            utilisationSignaux = []
            clefs = []
            for k in range(len(self.trajetsSillons)) :
                #print(k)
                try :
                    signaux = signauxVoies[self.trajetsSillons[k][3], self.trajetsSillons[k][-1]]
                    clefs.append([self.trajetsSillons[k][3], self.trajetsSillons[k][-1]])
                    #print("Clé dictionnaire signaux :", self.trajetsSillons[k][3], self.trajetsSillons[k][-1])
                    applicationSignaux = f.selectionSignaux(self.trajetsSillons, signaux, k)
                    #print("Signaux :", applicationSignaux)
                    utilisationSignaux.append(applicationSignaux)
                except :
                    pass

                
                #print(vitesseSignaux)
            #print("Signaux :", utilisationSignaux)
            #utilisationSignaux = list(set(utilisationSignaux))
            new_list = [] 
            SPD = []
            parcours = f.parcoursSillon(self.trajetsSillons)
            #print(parcours)
            for list1 in utilisationSignaux : 
                if list1 not in new_list : 
                    if list1 != [] : 
                        new_list.append(list1) 
            for b in range(len(new_list)):
                print("\n")
                print("#########################################")
                print("Signal :", new_list[b])
                dataVitesses = f.diminutionVitesseSignaux(dataVitesses, new_list[b], parcours)
                #print("Vitesses après signal :", SPD)
            #print("Longueur :", len(new_list))
            for j in range(len(dataVitesses)) :
                for n in range(len(dataVitesses[j])) :
                    if dataVitesses[j][n][3] == "Ascending" :
                        if j == 0 and n == 0 :
                            
                            distance = dataVitesses[j][n][2] - dataVitesses[j][n][0]
                            vitessesSillon.append([0, dataVitesses[j][n][1], dataVitesses[j][n][0]])

                        ### Cas particulier de la LGV ###
                        #elif indiceCompo == "E32C" and n == 0 and dataVitesses[j-1][n][1] != dataVitesses[j][n][1] :# len(dataVitesses)[j] :
                            #pkSignal = 1 #rechercheSignal(voie précédente , sens de circulation, pk fin)
                            #AKM = vitessesSillon[-1][0] + distance
                            #vitessesSillon[-1] = ([AKM, dataVitesses[j][n][1]])
                            #distance = dataVitesses[j][n][2] - dataVitesses[j][n][0]
                        
                        elif j == len(dataVitesses) and n == len(dataVitesses)[j] :
                            vitessesSillon.append([0, dataVitesses[j][n][1], dataVitesses[j][n][0]])
                        
                        else :
                            #print(vitessesSillon)
                            AKM = vitessesSillon[-1][0] + distance
                            vitessesSillon.append([AKM, dataVitesses[j][n][1], dataVitesses[j][n][0]])
                            distance = dataVitesses[j][n][2] - dataVitesses[j][n][0]

                    elif dataVitesses[j][n][3] == "Descending" :
                        #print(dataVitesses)
                        if j == 0 and n == 0 :
                            
                            distance = dataVitesses[j][n][0] - dataVitesses[j][n][2]
                            vitessesSillon.append([0, dataVitesses[j][n][1], dataVitesses[j][n][0]])

                        ### Cas particulier de la LGV ###
                        #elif indiceCompo == "E32C" and n == 0 and dataVitesses[j-1][n][1] != dataVitesses[j][n][1] :# len(dataVitesses)[j] :
                            #pkSignal = 1 #rechercheSignal(voie précédente , sens de circulation, pk fin)
                            #AKM = vitessesSillon[-1][0] + distance
                            #vitessesSillon[-1] = ([AKM, dataVitesses[j][n][1]])
                            #distance = dataVitesses[j][n][2] - dataVitesses[j][n][0]
                        
                        elif j == len(dataVitesses) and n == len(dataVitesses)[j] :
                            vitessesSillon.append([0, dataVitesses[j][n][1], dataVitesses[j][n][0]])
                        
                        else :
                            #print(vitessesSillon)
                            AKM = vitessesSillon[-1][0] + distance
                            vitessesSillon.append([AKM, dataVitesses[j][n][1], dataVitesses[j][n][0]])
                            distance = dataVitesses[j][n][0] - dataVitesses[j][n][2]

                    else :
                        pass


            #with open(rootPath + r"\Sillons\ " + str(i) + r".route ", 'w', newline='') as RouteFile:
                #fichierRoute = csv.writer(RouteFile, delimiter=';', quotechar='|')
                #fichierRoute.writerow(["Trajet"])
                #for b in range(len(self.trajetsSillons)) :
                    #fichierRoute.writerow(self.trajetsSillons[b])
                #fichierRoute.writerow(["SPD"])
                #for b in range(len(vitessesSillon)) :
                    #fichierRoute.writerow(vitessesSillon[b])
                #fichierRoute.writerow(["Infrastructure"])
                #for b in range(len(m)) :
                    #fichierRoute.writerow(m[b])
                #print(rootPath + r"\Sillons\ " + str(i) + r".route ")
            



            ### Partie gradients ###

            dataGradients = []
            m = []
            m2 = []

            for j in range(len(self.trajetsSillons)) :
                gradientsAssemblees = []
                #print("Trajet : ", self.trajetsSillons[i][2][j])
                try :
                    gradientsSection = gradientsVoies[self.trajetsSillons[j][3]]
                except :
                    gradientsSection = [[self.trajetsSillons[j][5],self.trajetsSillons[j][6],0]]
                
                temp = []
                #print(temp)

                for n in range(len(gradientsSection)) :
                    temp.append(gradientsSection[n])

                gradientsAssemblees = f.triGradient(self.trajetsSillons[j], temp)

                dataGradients.append(gradientsAssemblees)
            #print("data gradients",dataGradients)

            ### Création données propres routes (altitude) ###

            gradientsSillon = []
            #print("\n", dataGradients)
            for j in range(len(dataGradients)) :
                for n in range(len(dataGradients[j])) :
                    if gradientsSillon==[] and n == 0 :
                        valeur_gradient=float(dataGradients[j][n][1])
                        gradientsSillon.append([0, valeur_gradient, dataGradients[j][n][0]])
                        distance = abs(dataGradients[j][n][2] - dataGradients[j][n][0])
                        
                    
                    else :
                        valeur_gradient+=float(dataGradients[j][n][1])
                        gradientsSillon.append([distance, "{0:.1f}".format(valeur_gradient), dataGradients[j][n][0]])
                        distance += abs(dataGradients[j][n][2] - dataGradients[j][n][0])
            #print("Sillon Gradients :", gradientsSillon)


            ### Partie courbures ###
            
            dataRadiuses = []
            m = []
            m2 = []

            for j in range(len(self.trajetsSillons)) :
                radiusesAssemblees = []
                #print("Trajet : ", self.trajetsSillons[i][2][j])
                try :
                    radiusesSection = radiusesVoies[self.trajetsSillons[j][3]]
                    #print("Radiuses section ",radiusesSection)
                    #print("Radius : ", radiusesSection)
                except :
                    if self.trajetsSillons[j][-1] == "Ascending" :
                        radiusesSection = [[self.trajetsSillons[j][5], self.trajetsSillons[j][6], "0"]]
                    else :
                        radiusesSection = [[self.trajetsSillons[j][6], self.trajetsSillons[j][5], "0"]]
                    #print("Pas de radius sur la section : ", self.trajetsSillons[j])
                
                temp = []
                #print(temp)

                for n in range(len(radiusesSection)) :
                    temp.append(radiusesSection[n])

                radiusesAssemblees = f.triRadiuses(self.trajetsSillons[j], temp)
                dataRadiuses.append(radiusesAssemblees)
            #print("Dataradiuses :", dataRadiuses)
            try :
                dataRadiuses.remove([])
            except :
                pass
            #print("Radiuses :", dataRadiuses)

            ### Création données propres routes (courbure) ###

            radiusesSillon = []
            #print("\n", dataRadiuses)
            for j in range(len(dataRadiuses)) :
                for n in range(len(dataRadiuses[j])) :

                    if j == 0 and n == 0 :
                        radiusesSillon.append([0, dataRadiuses[j][n][1], dataRadiuses[j][n][0]])
                        distance = abs(dataRadiuses[j][n][2] - dataRadiuses[j][n][0])
                    
                    else :
                        radiusesSillon.append([distance, dataRadiuses[j][n][1], dataRadiuses[j][n][0]])
                        distance += abs(dataRadiuses[j][n][2] - dataRadiuses[j][n][0])
            #print("Sillon Radiuses :", radiusesSillon)


            ### Partie électrification ###


            ### Partie coordonnées GPS ###


            ### Assemblage VMax ###


            ### Partie balise trajet ###

            trajetSillon=[]
            for j in range (len(self.trajetsSillons)):
                ligne,voie=self.trajetsSillons[j][2],self.trajetsSillons[j][4]
                trajetSillon.append([float(self.trajetsSillons[j][0]),"j",str(ligne),str(voie),self.trajetsSillons[j][5]])
            #print("liste fea",trajetSillon)


            ### Assemblage du fichier Route ###
            def ROUTE (ALT, POW, CRV, SPD, FEA, GEO=[]):
                ROUTE=[]
                nom_balise=["ALT","POW","CRV","SPD","FEA","GEO"]
                liste_conca=[ALT,POW,CRV,SPD,FEA,GEO]
                while liste_conca!=[[],[],[],[],[],[]]:
                    if not ALT and "ALT" in nom_balise:
                        nom_balise.remove("ALT")
                    if not POW and "POW" in nom_balise :
                        nom_balise.remove("POW")
                    if not CRV and "CRV" in nom_balise :
                        nom_balise.remove("CRV")
                    if not SPD and "SPD" in nom_balise:
                        nom_balise.remove("SPD")
                    if not FEA and "FEA" in nom_balise:
                        nom_balise.remove("FEA")
                    if not GEO and "GEO" in nom_balise :
                        nom_balise.remove("GEO")
                    liste=[]
                    for i in liste_conca:
                        if i!=[]:
                            liste.append(i[0])
                    balise,ind = min(liste,key=lambda item:item[0]),liste.index(min(liste,key=lambda item:item[0]))
                    balise.insert(0,nom_balise[ind])
                    #print(balise)
                    if ROUTE!=[] and ROUTE[-1][1]==balise[1] :
                        fea=ROUTE[-1]
                        ROUTE[-1]=balise
                        ROUTE.append(fea)
                    else :
                        ROUTE.append(balise[:-1])
                        ROUTE.append(["FEA",balise[1],"KP",balise[-1]])
                    if nom_balise[ind]=="ALT":
                        del ALT[0]
                    elif nom_balise[ind]=="POW":
                        del POW[0]
                    elif nom_balise[ind]=="CRV":
                        del CRV[0]
                    elif nom_balise[ind]=="SPD":
                        del SPD[0]
                    elif nom_balise[ind]=="FEA":
                        del FEA[0]
                    else :
                        del GEO[0]
                    liste_conca=[ALT,POW,CRV,SPD,FEA,GEO]
                return ROUTE

            initialisationROUTE = [gradientsSillon[0],radiusesSillon[0],vitessesSillon[0]]
            terminerROUTE = [gradientsSillon[-1],radiusesSillon[-1],vitessesSillon[-1],self.trajetsSillons[-1]]
            listeROUTE = ROUTE(f.doublons(gradientsSillon),[],f.doublons(radiusesSillon),f.doublons(vitessesSillon),trajetSillon)
            #print("ROUTE",listeROUTE[2])
            #print("ROUTE",listeROUTE)
            #rootPath = os.getcwd()

            testPath= rootPath + r"\Sillons"
            longueur = "-400"
            with open(testPath + r"\Sillon_" + numeroSillon + "_" + str(i) + r".route", 'w', newline='') as RouteFile:
                fichierRoute = csv.writer(RouteFile, delimiter='\t', quotechar='|')
                fichierRoute.writerow(["CRV",longueur,initialisationROUTE[1][2]])
                fichierRoute.writerow(["ALT",longueur ,initialisationROUTE[0][2]])
                fichierRoute.writerow(["SPD",longueur ,initialisationROUTE[2][2]])
                fichierRoute.writerow(["FEA",0,"SILLON#",numeroSillon])
                for j in range(len(listeROUTE)) :
                    listeROUTE[j][1]="{0:.3f}".format(float(listeROUTE[j][1])/1000)
                    if len(listeROUTE[j])==4 and listeROUTE[j][0] != "FEA" :
                        listeROUTE[j]=listeROUTE[j][:3]
                    elif len(listeROUTE[j])==6:
                        listeROUTE[j]=listeROUTE[j][:5]
                    fichierRoute.writerow(listeROUTE[j])
                pkfin="{0:.3f}".format((float(terminerROUTE[-1][0])+float(terminerROUTE[-1][6])-float(terminerROUTE[-1][5]))/1000)
                fichierRoute.writerow(["CRV",pkfin,terminerROUTE[1][2]])
                fichierRoute.writerow(["ALT",pkfin ,terminerROUTE[0][2]])
                fichierRoute.writerow(["SPD",pkfin ,terminerROUTE[2][2]])


                #self.dataRoute.append([])



                #memoireNumeroSillon = sillons.dataSillon50[1]

                
                    #for b in range(len(radiusesSillon)) :
                        #fichierRoute.writerow(radiusesSillon[b])



route = Routes()