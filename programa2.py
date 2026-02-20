import time
import os 
import random
import msvcrt

def limpiar():
    os.system("cls")

def generar_datos(num):
    procesos = [] #guardo los procesos que se crean
    lista_id = [] #se gusradan las id, para buscar id repetido

    for i in range(num):

        while True:
            id_programador = random.randint(0,1000)
            if id_programador in lista_id:
                print("ID repetido, se creara otro")         
            else:             
                lista_id.append(id_programador)             
                break    

        tiempo_maximo = random.randint(6, 20)

        operaciones = ["+", "-", "*", "/", "%", "**"]
        operacion = random.choice(operaciones)

        a = random.randint(1,10)
        b = random.randint(1,10)
        
        while True:
            if operacion == "/" or operacion == "%":
                if b==0:
                    a = random.randint(1,10)
                    b = random.randint(1,10)
                else:
                    break
            else:
                break

        if operacion == "+":
            resultado =  a+b
        elif operacion == "-":
            resultado =  a-b
        elif operacion == "*":
            resultado =  a*b
        elif operacion == "/":
            resultado =  a/b
        elif operacion == "%":
            resultado =  a%b
        elif operacion == "**":
            resultado =  a**b

        procesos.append([id_programador, tiempo_maximo, operacion, a, b, resultado, 0])     

    return procesos


def crear_lotes(procesos):
    lotes = []     
    for i in range(0, len(procesos), 5):   
        lotes.append(procesos[i:i+5])     
    return lotes  


def mostrar(lotes):

    procesados = []     
    tiempo = 0     
    numero_de_lotes = 0       

    while numero_de_lotes < len(lotes):
        lote = lotes[numero_de_lotes]   

        print("----------------------------------------------")
        print(f"LOTE EN EJECUCION: {numero_de_lotes + 1}")
        for p in lote:
            print(f"ID: {p[0]} | Tiempo Maximo: {p[1]}")
        print("----------------------------------------------")
        n= 0
        while n < len(lote):
            i = lote[n]
            if i in procesados:
                n+=1
                continue

            tiempo_estimado = i[6] #es el tiempo avanzado
            interrumpido = False 

            while tiempo_estimado < i[1]:

                if msvcrt.kbhit():
                    tecla = msvcrt.getch().decode().upper()

                    if tecla == "P":
                        print("\nPROGRAMA PAUSADO - Presione C para continuar")
                        while True:
                            if msvcrt.kbhit():
                                if msvcrt.getch().decode().upper() == "C": #caracter/ convierte/mayuscula 
                                    break

                    elif tecla == "I":
                        i[6] = tiempo_estimado
                        lote.append(lote.pop(n))
                        interrumpido = True
                        break

                    elif tecla == "E":
                        i[5] = "ERROR"
                        break

                limpiar()

                pendientes = len(lotes) - numero_de_lotes - 1  

                print("------------------------------------------------")                 
                print(f"Lotes pendientes: {pendientes}")                 
                print(f"Lote actual: {numero_de_lotes + 1}")                 
                print("------------------------------------------------")     

                print("------------------------------------------------")                 
                print(f"PROCESOS DEL LOTE: {numero_de_lotes+1}")                 
                for ejecucion in lote:
                    if ejecucion not in procesados and ejecucion != i:
                        print(f"ID: {ejecucion[0]}")
                print("------------------------------------------------")

                actual = [                                        
                    f"Operacion: {i[2]}  Valores: {i[3]} y {i[4]}",                     
                    f"Tiempo Maximo: {i[1]}",                     
                    f"ID: {i[0]}",
                    f"Tiempo avanzado: {tiempo_estimado}",                     
                    f"Tiempo restante: {i[1]-tiempo_estimado}"                 
                ]                  

                terminados = []   

                for j in procesados:

                    if isinstance(j[5], str):
                        resultado = j[5]
                    else:
                        resultado = f"{j[5]:.2f}"

                    separador = "-------------------------------------------------------"

                    terminados.extend([
                        separador,
                        f"LOTE: {j[7]}",
                        f"ID: {j[0]} / Operacion: {j[2]} / Valores: {j[3]} y {j[4]} / Resultado: {resultado}",
                        separador
                    ])

                from itertools import zip_longest                 
                ancho = 45                 

                print(f"{'PROCESO ACTUAL':^{ancho}}|{'PROCESOS TERMINADOS':^{ancho}}")                 
                print("------------------------------------------------")                 

                for izq, der in zip_longest(actual, terminados, fillvalue=""):                     
                    print(f"{str(izq):<{ancho}}|{str(der):<{ancho}}")                                  

                print()                  
                print(f"Tiempo global: {tiempo+1}")                 
                print()                   

                time.sleep(1)                 

                tiempo += 1                 
                tiempo_estimado += 1             
                i[6] = tiempo_estimado

            if interrumpido:
                continue
            
            i.append(numero_de_lotes + 1)
            procesados.append(i)
            n+=1                 

        numero_de_lotes += 1     

    print("-------------------------------")     
    print("PROCESOS COMPLETOS FINALES")     

    for i in procesados:

        print("----------------------------------------------------------")                  
        print (f"Lote: {i[7]}")
        print (f"ID: {i[0]}")         

        if isinstance(i[5], str):
            print (f"Operacion: {i[2]} Valores: {i[3]} y {i[4]} Resultado: {i[5]}")
        else:
            print (f"Operacion: {i[2]} Valores: {i[3]} y {i[4]} Resultado: {float(i[5]):.2f}")

    input("\nPresione ENTER para finalizar...")  


num = int(input("Ingrese el numero de procesos que desea ingresar: "))

procesos = generar_datos(num)
lotes = crear_lotes(procesos)
mostrar(lotes)