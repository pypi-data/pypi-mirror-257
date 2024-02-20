''' Teniendo en cuenta que el numero introducido es 7, la palabra introducida es juanpedro y que su edad es 76, se imprimiria el siguiente patron:

                                                 J - 1 - 
                                                 U - 2 - 22 - 
                                                 A - 3 - 33 - 333 - 
                                                 N - 4 - 44 - 444 - 4444 - 
                                                 P - 5 - 55 - 555 - 5555 - 55555 - 
                                                 E - 6 - 66 - 666 - 6666 - 66666 - 666666 - 
                                                 D - 7 - 77 - 777 - 7777 - 77777 - 777777 - 7777777 - 
7-6-5-4-3-2-1-#-##-###-####-#####-######-#######-R - 8 - 88 - 888 - 8888 - 88888 - 888888 - 8888888 - 88888888 - 
7-6-5-4-3-2-1-#-##-###-####-#####-######-#######-O - 9 - 99 - 999 - 9999 - 99999 - 999999 - 9999999 - 99999999 - 999999999 - 
                                                 Hola, Tengo 76 Años y mi nombre es:                                         >+-juanpedro-+
7-6-5-4-3-2-1-#-##-###-####-#####-######-#######-O - 9 - 99 - 999 - 9999 - 99999 - 999999 - 9999999 - 99999999 - 999999999 - 
7-6-5-4-3-2-1-#-##-###-####-#####-######-#######-R - 8 - 88 - 888 - 8888 - 88888 - 888888 - 8888888 - 88888888 - 
                                                 D - 7 - 77 - 777 - 7777 - 77777 - 777777 - 7777777 - 
                                                 E - 6 - 66 - 666 - 6666 - 66666 - 666666 - 
                                                 P - 5 - 55 - 555 - 5555 - 55555 - 
                                                 N - 4 - 44 - 444 - 4444 - 
                                                 A - 3 - 33 - 333 - 
                                                 U - 2 - 22 - 
                                                 J - 1 - 
'''

import os
import time

def cargando_animacion():
    '''Esta funcion realiza una animacion de cargando antes de ejecutar el codigo principal. Utiliza como parametros n un int que 
    mide la longitud de la animacion, y reps un int que mide el numero de veces que se repite el patron'''
    n = 12
    reps = 2
    iReps = 0
    while iReps < reps:
        i = 1
        while i <= n:
            os.system('clear' if os.name == 'posix' else 'cls')
            iA = 1
            linea = ''
            while iA <= i:
                linea += ("#" * iA) + '-'
                iA += 1
            print('\n' * 6)
            print('Cargando   ', end='')
            print(linea[:-1])
            time.sleep(0.15)
            i += 1
        iReps += 1
    os.system('clear' if os.name == 'posix' else 'cls')

def print_con_delay(line, delay=0.25):
    '''Esta funcion hace que las imprsiones se realicen con cierto retraso entre ellas'''
    for x in line:
        if x == '\n':
            print(x, end='')
            time.sleep(delay)
        else:
            print(x, end='')

def generar_patron():
    '''Esta funcion genera un patron utilizando 3 parametros de entrada: n, edad y plbr, la n representa la longitud de la flecha, plbr 
    representa el tamaño de la punta y el nombre del usuario, y edad representa la edad del usuario'''
    try:
        n = int(input('Introduce un número entre el 1 y el 9: '))
        print('---------------------------')
        plbr = input('Introduce un nombre que tenga entre 3 y 9 caracteres: ')
        print('---------------------------')
        edad = int(input('Introduce tu edad: '))
        print('---------------------------')

        lineaNum = ''
        ptrGui = ' - '
        Frase = 'Hola, Tengo xx Años y mi nombre es:'
        i = 1

        print()
        while i <= len(plbr):
            if i <= len(plbr) - 2:
                lineaEsp = (' ' * (n * 2)) + (' ' * (int((n * (n + 1)) / 2) + n))
                iAscend = 1
                while iAscend <= i:
                    if iAscend == 1:
                        lineaNum += plbr[i - 1].upper() + ' - ' + str(i) + ' - '
                    else:
                        lineaNum += str(i) * iAscend + ptrGui
                    iAscend += 1
                print_con_delay(lineaEsp)
                print_con_delay(lineaNum + '\n')
                lineaNum = ''
            else:
                Inum = n
                while Inum > 0:
                    print_con_delay(str(Inum) + "-", delay=0.25)
                    Inum -= 1
                iAlmo = 1
                while iAlmo <= n:
                    print_con_delay("#" * iAlmo + "-", delay=0.25)
                    iAlmo += 1
                iAscend = 1
                while iAscend <= i:
                    if iAscend == 1:
                        lineaNum += plbr[i - 1].upper() + ' - ' + str(i) + ' - '
                    else:
                        lineaNum += str(i) * iAscend + ptrGui
                    iAscend += 1
                if i == len(plbr):
                    lineaLenPlbr = lineaNum
                    lineaArriba = (n * 2) + (int((n * (n + 1)) / 2) + n) + len(lineaLenPlbr)
                    lineaFrase = (n * 2) + (int((n * (n + 1)) / 2) + n) + len(Frase)
                    numesp = ' ' * (lineaArriba - lineaFrase)
                print_con_delay(lineaNum + '\n')
                lineaNum = ''

            i += 1
        if len(str(edad)) == 2:
            print(f'{lineaEsp}Hola, Tengo {edad} Años y mi nombre es:{numesp}>+-{plbr}-+')
        else:
            print(f'{lineaEsp}Hola, Tengo {edad} Años y mi nombre es:{numesp} >+-{plbr}-+')
        i = len(plbr)
        while i >= 1:
            if i <= len(plbr) - 2:
                lineaEsp = (' ' * (n * 2)) + (' ' * (int((n * (n + 1)) / 2) + n))
                iAscend = 1
                while iAscend <= i:
                    if iAscend == 1:
                        lineaNum += plbr[i - 1].upper() + ' - ' + str(i) + ' - '
                    else:
                        lineaNum += str(i) * iAscend + ptrGui
                    iAscend += 1
                print_con_delay(lineaEsp)
                print_con_delay(lineaNum + '\n')
                lineaNum = ''
            else:
                Inum = n
                while Inum > 0:
                    print_con_delay(str(Inum) + "-", delay=0.25)
                    Inum -= 1
                iAlmo = 1
                while iAlmo <= n:
                    print_con_delay("#" * iAlmo + "-", delay=0.25)
                    iAlmo += 1
                iAscend = 1
                while iAscend <= i:
                    if iAscend == 1:
                        lineaNum += plbr[i - 1].upper() + ' - ' + str(i) + ' - '
                    else:
                        lineaNum += str(i) * iAscend + ptrGui
                    iAscend += 1
                if i == len(plbr):
                    lineaLenPlbr = lineaNum
                print_con_delay(lineaNum + '\n')
                lineaNum = ''
            i -= 1
        print()

    except ValueError:
        print('No has introducido el tipo de dato esperado')
        generar_patron()

def Nizar_patron():
    '''Esta funcion realiza una animacion de cargando antes de ejecutar el codigo principal. 
    seguidamente, genera un patron utilizando 3 parametros de entrada: n, edad y plbr, la n representa la longitud de la flecha, plbr 
    representa el tamaño de la punta y el nombre del usuario, y edad representa la edad del usuario'''
    cargando_animacion()
    generar_patron()


Nizar_patron()