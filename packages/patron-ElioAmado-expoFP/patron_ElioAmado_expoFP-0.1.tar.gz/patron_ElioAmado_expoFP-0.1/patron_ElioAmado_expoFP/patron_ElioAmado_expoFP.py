import time
import os
"""
Idea patron: alt, forma.
alt = 7, forma = Abajo, nombre = Loco, rell = º
|\ ººººººººººººº /|
| \ ººººººººººº / |
|  \ ººººººººº /  |
|   \ ººººººº /   |
|    \ ººººº /    |
|     \ ººº /     |
| Loco \ º / Loco | O 


alt = 2, forma = Abajo, nombre = Tonto, rell = º

| Tonto / º \ Tonto |
|      / ººº \      |
|     / ººººº \     |
|    / ººººººº \    |
|   / ººººººººº \   |
|  / ººººººººººº \  |
| / ººººººººººººº \ |
|/ ººººººººººººººº \|

alt = 8, forma = Mezcla, nombre = Azote, rell = º, Si es impar pide mid = "X"
|\ ººººººººººººº /| 
| \ ººººººººººº / |
|  \ ººººººººº /  |
| A \ ººººººº / A |
| z  \ ººººº /  z |
| o   X XXX X   o |
| t  / ººººº \  t |
| e / ººººººº \ e |
|  / ººººººººº \  |
| / ººººººººººº \ |
|/ ººººººººººººº \|

|\ ººººººººººººº /|
| \ ººººººººººº / |
|  \ ººººººººº /  |
| A \ ººººººº / A |
| z  \ ººººº /  z |
| t  / ººººº \  t |
| e / ººººººº \ e |
|  / ººººººººº \  |
| / ººººººººººº \ |
|/ ººººººººººººº \|

    Mezclado

1 - El comienzo de la primera iteraccion es i = alt
2 - En la primera iteraccion empieza sin espacios entre el "|" y el "\\"
3 - En cada iteraccion se imprime un "|" al principio y al final
4 - Despues de el primer | habran espacios que sera nSpc, despues habra "\\"
5 - Una vez se imprime el lado izquierdo toca el centro que es " "+Rell*iRell+" "
6 - Con el centro impreso el lado izquierdo empieza con un "/",
    un numero de espacios que es nSpc y con un "|"
7 - Todos los indices que son: nSpc, iRell y i se suman por inc que es -1
8 - A partir de la mitad el incremento sera 1 y todos los indices empiezan a sumar
9 - y se empezara a imprimir la letra del nombre cuando se cumpla la condicion (alt//2-lon//2 == i)
    y acabara cuando no queden mas letras en el nombre:
        El lado izquierdo sera "|"+" "+nom[iNom]+" "*nSpc+"\\"
        El lado derecho sera "/"+" "*nSpc+nom[iNom]+" "+"|"
10 - Si nom es impar se pedia otro simbolo que se almacena en la variable mid
11 - si nom es impar se imprimira en la mitad del patron:
     "|"+" "+nom[iNom]+" "*nSpc+mid+" "+mid*irell+" "+mid+" "*nSpc+nom[iNom]+" "+"|"

    Arriba

1 - en cada iteraccion se imprime un "|"
2 - En la primera linia se imprime minimo un espacio y despues se imprime el nombre
3 - En la primera linia se imprime despues del nombre un "/"+Rell*iRell+"\\"
4 - Al final de la iteraccion se imprime un "|"
5 - En cada iteraccion despues del primer "|" habra un numero de espacios que es " "*nSpc
6 - Despues se imprime un "/" y despues se imprime un espacio
7 - Despues del primer "/ " se imprime rell*irell
8 - Una vez imprimido el "\\" se vuelve a imprimir el numero de espacios " "*Spc
9 - Al final de cada iterraccion se imprime un "|"
10 - En cada iterracion hay, menos espacios y mas caracteres de relleno "Rell"
11 - Minimo alt sera la longitud de la palabra

    Abajo

Es lo mismo que arriba pero a la inversa y "inc" que es el incremento de las pasa a ser -1

"""

#Esta funcion imprime un patron segun los parametros
def elio_Patron() -> None:
    """
    Esta funcion crea un patron segun los parametros de entrada.
    Son 4 parametros de entrada, el primero que es "alt",
    especifica la altura que tendra el patron y tiene que ser un entero,
    el segundo es "frm" que hay 3 posibilidades (Arriba, Abajo, Mezclado),
    segun la forma que se especifique el patron tendra una forma o otra,
    el tercer parametro es "rell" que indica el que caracter de relleno,
    habra en medio del patron y solo puede ser un caracter,
    el cuarto parametro es "nom" que es una palabra o frase,
    que se imprime en el patron, al forma en que se imprime depende de "frm".
    No devuelve nada.
    """
    #Este funcion devuelve una linia del patron
    def ptrferiaLine(irell:int, lon:int, nSpc:int,frmTrin:list[str], rell:str, nom:str) -> str:
        """
        Esta funcion crea la variable line que es la linia del patron segun los
        parametros, de parametros de entrada tiene irell que es un entero que 
        significa la cantidad de caracteres de relleno que hay en el patron,
        lon es la longitud en enteros de nom que el parametro es de la funcion padre,
        nSpc es un entero que significa el numero de espacios,
        frmTrin es una lista que contiene un \ y un /, que se utiliza para dar
        forma al patron
        """
        line = ""
        if irell == 1 and nom:
            if ((nSpc-lon)//2) % 2:
                nSpcN = (nSpc-lon)//2
            else:
                nSpcN = (nSpc-lon)//2
            line += "| "+(" "*(nSpcN))
            line += nom+" "*(nSpcN)
            line += frmTrin[0]+" "+rell*irell+" "+frmTrin[1]
            line += " "*(nSpcN)+nom
            line += " "*(nSpcN)+" |"
        else:
            line += "|"+(" "*(nSpc))+frmTrin[0]+" "
            line += rell*irell+" "
            line += frmTrin[1]+" "*(nSpc)+"|"
        return line
    
    #Esta funcion imprime por pantalla el patron con la forma Arriba o Abajo
    def ptrferiaimpr(inc:int, irell:int, i:int, frmTrin:list[str], alt:int, rell:str, nom:str) -> None:
        """
        Esta funcion imprime el patron segun los parametros.
        De parametros de entrada esta inc que es el incrementos,
        el incremento puede ser 1 o -1, irell que es un entero que 
        significa la cantidad de caracteres de relleno que hay en el patron,
        i es un indice para el patron, frmTrin es una lista que contiene
        un \ y un /, que se utiliza para da forma al patron
        """
        lon = len(nom)
        nSpc = alt-i+1
        
        while i <= alt and i != 1:
            line = ptrferiaLine(irell,lon,nSpc,frmTrin,rell,nom)
            print(line)

            nSpc -= inc
            irell += inc*2
            i += inc
    #Esta funcion imprime por pantalla el patron con la forma mezclado
    def ptrferiaimprMez(inc:int, irell:int, i:int, frmTrin:list[str], alt:int, rell:str, nom:str) -> None:
        """
        Esta funcion imprime el patron con forma mezclada
        """
        #Esta funion imprime la linia del patron con el nombre en vertical
        def ptrferiaLineNom(nSpc:int,iNom:int):
            """
            """
            line = ""
            line += "|"+(" "+nom[iNom])+(" "*(nSpc-2))+frmTrin[0]+" "
            line += rell*irell+" "
            line += frmTrin[1]+(" "*(nSpc-2))+(nom[iNom]+" ")+"|"
            return line
        
        lon = len(nom)
        nSpc = alt-i
        Nbool = False
        iNom = -1

        while i <= alt and i != 1:
            line = ""
            if i == alt//2-1:
                inc *= -1

                frmTrin = frmTrin[::-1]
            else:
                if lon % 2:
                    lon -= 1
                rstNom = alt//2-lon//2
                if Nbool or (rstNom == i-lon+1 and i > 2):
                    iNom += 1
                    line += ptrferiaLineNom(nSpc,iNom)
                else:
                    line += ptrferiaLine(irell,lon,nSpc,frmTrin,rell,nom)

                if rstNom == i-lon+1:
                    Nbool = not Nbool
            if line:
                print(line)

            nSpc -= inc
            irell += inc*2
            i += inc

    frm = input("Indica la forma que puede ser Abajo, Arriba o Mezclado: ")
    rell = input("Indica un caracter que sera el relleno para el patron: ")
    
    nom = input("Indica un nombre que tenga menos de 19 caracteres: ")
    print()
    alt = input("indica la altura que tiene que ser un numero entre "+str(len(nom)+9)+" y 29")

    while True:
        alt = str(alt)
        if not alt or not alt.isdecimal():
            alt = input("La altura tiene que ser un numero: ")
            continue
        else:
            alt = int(alt)
            if alt > 0 and not alt <= 28:
                alt = input("indica la altura que tiene que ser un numero entre "+str(len(nom)+9)+" y 29")
                continue
        if not frm in ["Abajo", "Arriba", "Mezclado"]:
            frm = input("indica la forma que puede ser Abajo, Arriba o Mezclado: ")
            continue

        if len(rell) != 1:
            rell = input("indica un caracter que sera el relleno para el patron: ")
            continue
            
        if not nom or len(nom) > 19:
            nom = input("indica un nombre que tenga menos de 19 caracteres: ")
            continue

        if len(nom)+4 > alt:
            if len(nom) % 2:
                alt = len(nom)+10
            else:
                alt = len(nom)+8
        break
    
    if frm == "Mezclado":
        while alt > 5:
            i = int(alt)
            irell = int(alt)*2-3
            frmTrin = ["\\","/"]
            ptrferiaimprMez(-1,irell,i,frmTrin,alt,rell,nom)
            nom = nom[1:]
            time.sleep(0.5)
            os.system('cls')
            alt -= 2
    else:
        nom = " " + nom
        while alt > 0:
            if frm == "Abajo":
                frm = "Arriba"
            else:
                frm = "Abajo"
            nom = nom[1:]
            frmTrin = ["/","\\"]
            os.system('cls')
            if frm == "Arriba":
                ptrferiaimpr(1,1,2,frmTrin,alt,rell,nom)

            else:

                i = int(alt)
                irell = int(alt)*2-3
                frmTrin = frmTrin[::-1]
                ptrferiaimpr(-1,irell,i,frmTrin,alt,rell,nom)
            time.sleep(0.5)
            alt -= 1