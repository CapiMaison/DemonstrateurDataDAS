""" Created by Guillaume WELLER on 04/05/2021 """
""" Last modifications on 04/05/2021 by Guillaume WELLER """

######### ######### ######### ######### ####9#### ######### ######### ######### #########

##########################
### Modules à importer ###
##########################

import os
import csv
import pickle
from Classes import Debug
from Demonstrateur import Routes

rootPath = os.getcwd()
reporting = Debug()

data = Routes()
dataSillons = data.dataSillons

#archive = Archivage(rootPath)



##########################
### Variables globales ###
##########################

global balises
balises = ["POW", "GEO", "SPD", "CRV", "ALT", "FEA", "TSL", "SPDTSL"]



##########################
### Début du programme ###
##########################

### Emplacement des fichiers ###

#dataCirculationPath = rootPath + r"\Circulation" + r"\matoll_ctth_0408213054.dat"
testPath = rootPath + r"\Test"

### Création du fichier Route ###

for i in range(10) :
    with open(testPath + r"\Sillon " + str(i) + r".route ", 'w', newline='') as RouteFile:
        fichierRoute = csv.writer(RouteFile, delimiter=';', quotechar='|')

        ### Initialisation ###
        fichierRoute.writerow(["Sillon 7830"])
        for j in range(0) :
            if dataSillons[j] == "?" :
                fichierRoute.writerow(["Sillon 7830"])
            elif dataSillons[j] == "?" :
                fichierRoute.writerow(["Sillon 7830"])
            elif dataSillons[j] == "?" :
                fichierRoute.writerow(["Sillon 7830"])
            elif dataSillons[j] == "?" :
                fichierRoute.writerow(["Sillon 7830"])
            elif dataSillons[j] == "?" :
                fichierRoute.writerow(["Sillon 7830"])
            else :
                fichierRoute.writerow(["Sillon 7830"])

        ### Ecriture des données Route ###

        for n in range(len("route")) :
            fichierRoute.writerow(route[n])

