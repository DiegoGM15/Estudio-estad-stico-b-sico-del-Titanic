import os
from os import system
system("cls")
import numpy as np
import mysql.connector

conexion1=mysql.connector.connect(host="localhost", user="root", passwd="", db="")
carpeta = "c:/nueva/"
fichero = "titanic.csv"

ruta = os.path.join(carpeta, fichero)
ruta = os.path.abspath(ruta)
titanic = np.loadtxt(carpeta + fichero, skiprows=1, dtype=str, delimiter=",") 

np.savetxt(carpeta + "copiatitanic.csv", titanic, delimiter=';', fmt=['%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s'])

cursor1 = conexion1.cursor()

cursor1.execute("create database if not exists titanicdatos character set latin1 collate latin1_spanish_ci;")
cursor1.execute("use titanicdatos;")
cursor1.execute("create table if not exists pasajeros (id_pasajero int primary key ,sobreviviente bool, clase varchar(1), nombre varchar(50), sexo varchar(10), edad int, sibsp int, parch int, ticket varchar(15), tarifa float, cabina varchar(15), embarcar varchar(1), mayorde_edad bool);")
#cursor1.execute("LOAD DATA INFILE 'c:/nueva/copiatitanic1.csv' INTO TABLE pasajeros FIELDS TERMINATED BY ';' LINES TERMINATED BY '\n';")
conexion1.commit()

cursor1.execute("select * from pasajeros;")

longitud = 0
tabla = list()

for fila in cursor1:

    ancho = len(fila)
    tabla.append(fila)
    longitud += 1

copia = np.array(tabla)

for i in range (copia.shape[0]): #Mayores y menores de edad 

    mayoredad = 0 
    edad = copia[i][5]

    if(int(copia[i][5]) < 18):

        mayoredad = 0

    else:

        mayoredad = 1

    cursor1.execute("update pasajeros set mayorde_edad = %s where edad = %s;",(mayoredad,str(edad)))

conexion1.commit()

totalpasajeros = 0
fallecidos = 0
sobrevivientes = 0
mujeres = 0
clase3 = 0 
clase2 = 0
clase1 = 0
c3sobrevivientes = 0
c2sobrevivientes = 0 
c1sobrevivientes = 0
c3mujeres = 0
mediac3 = 0 
c2mujeres = 0
mediac2 = 0
c1mujeres = 0
mediac1 = 0
mayoresc1 = 0
mayoresc2 = 0
mayoresc3 = 0
menoresc1 = 0
menoresc2 = 0
menoresc3 = 0

for i in range(copia.shape[0]):

    if(copia[i][1]):

        totalpasajeros = totalpasajeros + 1

        if(copia[i][1] == "0"):

            fallecidos = fallecidos + 1

        elif(copia[i][1] == "1"):

            sobrevivientes = sobrevivientes + 1

    if(copia[i][2] == "3"): #Clase 3
        
        clase3 = clase3 + 1
        if(copia[i][4] == "female"):

            c3mujeres = c3mujeres + 1
            mediac3 = mediac3 + int(copia[i][5])

        if(copia[i][1] == "1"):

            c3sobrevivientes = c3sobrevivientes + 1

            if(int(copia[i][5]) >= 18):

                mayoresc3 = mayoresc3 + 1

            elif(int(copia[i][5]) < 18):

                menoresc3 = menoresc3 + 1

    elif(copia[i][2] == "2"): #Clase2

        clase2 = clase2 + 1
        if(copia[i][4] == "female"):

            c2mujeres = c2mujeres + 1
            mediac2 = mediac2 + int(copia[i][5])

        if(copia[i][1] == "1"):

            c2sobrevivientes = c2sobrevivientes + 1

            if(int(copia[i][5]) >= 18):

                mayoresc2 = mayoresc2 + 1

            elif(int(copia[i][5]) < 18):

                menoresc2 = menoresc2 + 1
            
    elif(copia[i][2] == "1"): #Clase1

        clase1 = clase1 + 1

        if(copia[i][4] == "female"):

            c1mujeres = c1mujeres + 1
            mediac1 = mediac1 + int(copia[i][5])

        if(copia[i][1] == "1"):

            c1sobrevivientes = c1sobrevivientes + 1

            if(int(copia[i][5]) >= 18):

                mayoresc1 = mayoresc1 + 1

            elif(int(copia[i][5]) < 18):

                menoresc1 = menoresc1 + 1

porfallecidos = str(round(fallecidos/totalpasajeros * 100, 2)).replace(".", ",")
porsobrevivientes = str(round(sobrevivientes/totalpasajeros * 100, 2)).replace(".",",")

porclase3 = str(round(c3sobrevivientes/clase3 * 100, 2)).replace(".",",")
porclase2 = str(round(c2sobrevivientes/clase2 * 100, 2)).replace(".",",")
porclase1 = str(round(c1sobrevivientes/clase1 * 100, 2)).replace(".",",")

mujeresc1 = str(round(mediac1/c1mujeres , 2)).replace(".",",")
mujeresc2 = str(round(mediac2/c2mujeres , 2)).replace(".",",")
mujeresc3 = str(round(mediac3/c3mujeres , 2)).replace(".",",")

pormenoresc1 = str(round(menoresc1/c1sobrevivientes * 100, 2)).replace(".",",")
pormenoresc2 = str(round(menoresc2/c2sobrevivientes * 100, 2)).replace(".",",")
pormenoresc3 = str(round(menoresc3/c3sobrevivientes * 100, 2)).replace(".",",")

pormayoresc1 = str(round(mayoresc1/c1sobrevivientes * 100, 2)).replace(".",",")
pormayoresc2 = str(round(mayoresc2/c2sobrevivientes * 100, 2)).replace(".",",")
pormayoresc3 = str(round(mayoresc3/c3sobrevivientes * 100, 2)).replace(".",",")

psj148 = np.array(copia[147:148])

first10 = np.array(copia[:10])
last10 = np.array(copia[-10:])

for i in range(first10.shape[0]):

    first10[i][9] = str(first10[i][9]).replace(".",",")
    last10[i][9] = str(last10[i][9]).replace(".",",")

encabezado = np.array([["id pasajero(int)","sobreviviente(bool)","clase varchar(1)","nombre varchar(50)","sexo varchar(10)", "edad int", "sibsp int", "parch int", "ticket varchar(15)", "tarifa float", "cabina varchar(15)", "embarcar varchar(1)", "mayorde_edad bool"]])
salida1 = np.concatenate((encabezado,first10), axis=0)

filavacia = np.array([[" "," "," "," "," "," "," ", " "," "," ", " "," "," "]])

salida2 = np.concatenate((salida1,filavacia), axis=0)

salida3 = np.concatenate((salida2,last10), axis=0)

elementos = copia.size #Numero de datos que contiene
dimensiones = copia.ndim #Dimensiones de la tabla

salida0 = np.array([["Dimensiones de la tabla", dimensiones,"Numero de datos que contiene",elementos,"Porcentaje de personas que sobrevivieron",porsobrevivientes,"Porcentaje de personas que fallecieron", porfallecidos,"Porcentaje de personas que sobrevivieron en primera clase",porclase1,"Porcentaje de personas que sobrevivieron en segunda clase",porclase2," "]])

salida4 = np.concatenate((salida3,salida0), axis=0)

salida5 =np.array([["Porcentaje de personas que sobrevivieron en tercera clase",porclase3,"Edad media de las mujeres en primera clase",mujeresc1,"Edad media de las mujeres en segunda clase", mujeresc2,"Edad media de las mujeres en tercera clase", mujeresc3,"Porcentaje de menores que sobrevivieron en primera clase",pormenoresc1,"Porcentaje de menores que sobrevivieron en segunda clase",pormenoresc2," "]])

salida6 = np.concatenate((salida4,salida5), axis=0)

salida7 =np.array([["Porcentaje de menores que sobrevivieron en tercera clase",pormenoresc3,"Porcentaje de mayores que sobrevivieron en primera clase",pormayoresc1,"Porcentaje de mayores que sobrevivieron en segunda clase",pormayoresc2,"Porcentaje de mayores que sobrevivieron en tercera clase",pormayoresc3,"Datos del pasajero con ID 148:"," "," "," "," "]])

salida8 = np.concatenate((salida6,salida7), axis=0)

salida9 =np.concatenate((salida8,psj148), axis=0)

np.savetxt(carpeta + "salidatitanic.csv", salida9, delimiter=';', fmt=['%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s'])










    


    




