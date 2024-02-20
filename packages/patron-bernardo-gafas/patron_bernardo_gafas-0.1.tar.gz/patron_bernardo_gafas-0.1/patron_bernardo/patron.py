import re
#La función bernardo_patron devuelve un patron con formato de gafas teniendo en cuenta un numero y un nombre
def bernardo_gafas():
    '''
    Está funcion crea un patron que pide n(numero tipo entero) y palab(un nombre tipo string),
    la cantidad de caracteres de palab, dependerá del valor de n y una expresion regular validará
    palab.Devuelve un conjunto de caracteres con formato de gafas cuadradas.
    '''
    while True:
        try:
            n = int(input("Introduce un número entre 3 y 9: "))
            if 3 <= n <= 9:
                break
            else:
                print("El número debe estar entre 3 y 9. Por favor, inténtalo de nuevo.")
        except ValueError:
            print("Por favor, introduce un número válido.")

    while True:
        palab = str(input('Introduce tu primer nombre: '))
        long_palabras = {3: 28, 4: 25, 5: 23, 6: 21, 7: 19, 8: 17, 9: 15}
        if len(palab) < 3:
            print("El nombre debe tener al menos 3 caracteres.")
            continue

        long_max = long_palabras[n]

        if len(palab) > long_max:
            print("El nombre ingresado excede la longitud máxima permitida. Por favor, inténtalo de nuevo.")
            continue

        expregPalab = r'^[A-Za-záéíóúÁÉÍÓÚñÑ]{3,' + str(long_max) + r'}(?: [A-Za-záéíóúÁÉÍÓÚñÑ]+)?$'
        
        if re.match(expregPalab, palab):
            break
        else:
            print("""El nombre ingresado no es válido(Solamente un espacio y entre palabras, 
                sin caracteres especiales).Por favor, inténtalo de nuevo.""") 
                

    i = 1
    linea =''
    nCharPal = len(palab)
    resta = 4
    lineaCent = 4*n + nCharPal
    listaNum = []

    if nCharPal % 2 == 0:
        palab = palab+'.'


    while i < n:
        if i < n-1:
            relleno = ((4*n + nCharPal) - 4*(n-2))-4
            esp = (lineaCent - relleno - resta)//2
            linea2 = str(i+1) + ' '
            linea += str(i) + ' '
            lineaC = '#'*esp+linea+linea2*(relleno//2)+str(i+1)+linea[::-1]+'#'*esp+' '+' '*nCharPal
            listaNum.append(lineaC)
        
        resta += 4
        if i == n-1:
            linea += str(i)+' '+str(i+1)+' '
            lineaC = linea+palab+linea[::-1]
            listaNum.append(lineaC)
        i += 1

    i = 1

    listaNumrev = listaNum[::-1]
    while i < len(listaNumrev):
        listaNum.append(listaNumrev[i])

        i += 1

    medioGui = (nCharPal+1)//2

    i = 0
    while i < len(listaNum):
        patron = listaNum[i]
        if i < n-2:
                print(patron+patron[::-1])
        if i == n-2:
            if nCharPal % 2 == 0:
                print(patron+'-'*medioGui+'.'+palab+'-'*medioGui+patron[::-1])
            else:
                print(patron+'-'*medioGui+palab+'.'+'-'*medioGui+patron[::-1])
        if i > n-2:
            print(patron+patron[::-1])
        i += 1

