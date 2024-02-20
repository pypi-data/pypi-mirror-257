#Función para imprimir un patron con animación descendete/ascendente durante 11 s 
def patron_Robert():
    '''
    La función solicita al usuario un número que será el primer patrón a imprimir. Luego, la siguiente
    impresión se basará en si el número es mayor o menor que 5. La animación está dividida en tres etapas: descenso, ascenso
    y cambio de símbolos. Se elige descenso o ascenso en la animación dependiendo del número introducido. Si es mayor que 5,
    el patrón se imprimirá de forma descendente hasta llegar a 2, y a la inversa si el número es menor que 5.

    Al llegar al número mínimo o al número máximo, que son el 9 y el 2, el patrón cambiará de símbolos y comenzará con el
    último símbolo volviendo al número inicial introducido. La animación utiliza las bibliotecas os y time para borrar y
    calcular la duración total, siempre siendo 11 segundos para no cansar al usuario.
    '''
    import os
    import time
    
    while True:
        try:
            n = int(input("Introduce un numero de 1-9: "))
            if 1 <= n <= 9:
                break
            else:
                print("Te he pedido un número del 1 al 9.")
        except ValueError:
            print("Error: Debes introducir un número entero.")

    tiempo_inicial = time.time()
    duracion_deseada = 11
    ancho = n * 2 - 1
    vacio = "  " * n

    cont = 0
    i = 1
    NumFinal = n
    reverso = False
    end = n
    if n > 5:
        NumALlegar = 2
    else:
        NumFinal = 9
        reverso = True

    while (time.time() - tiempo_inicial) < duracion_deseada:
        simbolos = ["* ", "# ", "$ ", "Є ", "& "]
        spacio = 1
        patron = []
        NumDePAt = 1
        altura = n * 2 + 2
        os.system('cls' if os.name == 'nt' else 'clear')
        i = 1

        while i <= altura:
            j = 1
            linAImpr = ""
            NumIMPR = 1
            ancho = (2 * n - 1)

            if i == 1 or i == altura:
                linAImpr += simbolos[cont] * ancho
            else:
                if i <= n:
                    while j <= ancho:
                        relleno = (n + 2 - i) * 2 - 1
                        if j < spacio:
                            linAImpr += "  "
                        elif j < spacio + relleno:
                            if NumIMPR == 1:
                                linAImpr += simbolos[cont]
                                NumIMPR += 1
                            elif j < (n - i + 1) + spacio:
                                linAImpr += str(NumIMPR) + " "
                                NumIMPR += 1
                            else:
                                linAImpr += str(NumIMPR) + " "
                                NumIMPR -= 1
                        else:
                            linAImpr += "  "
                        j += 1
                    spacio += 1
                    patron.append(linAImpr)
                else:
                    if i <= (altura - n):
                        linAImpr += "  " * (spacio - 1) + simbolos[cont] + "  " * (spacio - 1)

            if i == 1 or i == altura:
                print(vacio + linAImpr + simbolos[cont] + linAImpr)
            else:
                if i <= (altura - n):
                    print(vacio + linAImpr + "  " + linAImpr)
                else:
                    print(vacio + patron[-NumDePAt] + "  " + patron[-NumDePAt])
                    NumDePAt += 1

            i += 1
        time.sleep(0.5)

        if n == NumFinal and reverso:
            if cont != 4:
                cont += 1
            else:
                NumALlegar = 2
                reverso = False
        elif reverso:
            if n != NumFinal:
                n += 1
        else:
            if n == NumALlegar:
                if cont != 4:
                    cont += 1
                else:
                    reverso = True
            else:
                n -= 1

    print("\n" + "Se ha acabado la animación. ")
