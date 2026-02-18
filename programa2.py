import time
import os 
import random
import msvcrt

def limpiar():
    os.system("cls")

def generar_datos(num):
    procesos = []
    lista_id = []
    for i in range(num):
        while True:
            id_programador = random.randint(0,1000)
            if id_programador in lista_id:
                print("ID repetido, intenta otro")         
            else:             
                lista_id.append(id_programador)             
                break    
        
        while True:
            tiempo_maximo = random.randint(6, 20)
            if tiempo_maximo < 6 or tiempo_maximo > 20:   # CORREGIDO
                print("Tiempo no valido")         
            else:                        
                break

        operaciones = ["+", "-", "*", "/", "%", "**"]
        operacion = random.choice(operaciones)
        
        a = random.randint(1,10)
        b = random.randint(1,10) 
        
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
        
        procesos.append([id_programador, tiempo_maximo, operacion, a, b, resultado])     
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
        
        print("==============================================")
        print(f"LOTE EN EJECUCION: {numero_de_lotes + 1}")
        for p in lote:
            print(f"ID: {p[0]} | Tiempo Maximo: {p[1]}")
        print("==============================================")

        for i in lote:             
            tiempo_estimado = 0                         

            while tiempo_estimado < i[1]:         
                
                limpiar()     
                
                if msvcrt.kbhit():
                    tecla = msvcrt.getch().decode().upper()

                    if tecla == "P":
                        print("\nPROGRAMA PAUSADO - Presione C para continuar")
                        while True:
                            if msvcrt.kbhit():
                                if msvcrt.getch().decode().upper() == "C":
                                    break

                    elif tecla == "I":
                        break

                    elif tecla == "E":
                        i[5] = "ERROR"
                        break

                pendientes = len(lotes) - numero_de_lotes - 1  

                print("------------------------------------------------")                 
                print(f"Lotes pendientes: {pendientes}")                 
                print(f"Lote actual: {numero_de_lotes + 1}")                 
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

                    terminados.extend([                         
                        "",                         
                        f"ID: {j[0]}",                         
                        f"Operacion: {j[2]}  Valores: {j[3]} y {j[4]}",  
                        f"Resultado: {resultado}"                      
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

                time.sleep(1.5)                 
                tiempo += 1                 
                tiempo_estimado += 1             

            procesados.append(i)                 

        numero_de_lotes += 1     

    print("-------------------------------")     
    print("PROCESOS COMPLETOS FINALES")     
    for i in procesados:         
        print("----------------------------------------------------------")                  
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
