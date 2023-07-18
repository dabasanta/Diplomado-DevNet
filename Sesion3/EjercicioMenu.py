#!/usr/bin/env python3

def imprimir_menu():
    menu = '''
██████╗ ███████╗███████╗████████╗ █████╗ ██╗   ██╗██████╗  █████╗ ███╗   ██╗████████╗███████╗
██╔══██╗██╔════╝██╔════╝╚══██╔══╝██╔══██╗██║   ██║██╔══██╗██╔══██╗████╗  ██║╚══██╔══╝██╔════╝
██████╔╝█████╗  ███████╗   ██║   ███████║██║   ██║██████╔╝███████║██╔██╗ ██║   ██║   █████╗  
██╔══██╗██╔══╝  ╚════██║   ██║   ██╔══██║██║   ██║██╔══██╗██╔══██║██║╚██╗██║   ██║   ██╔══╝  
██║  ██║███████╗███████║   ██║   ██║  ██║╚██████╔╝██║  ██║██║  ██║██║ ╚████║   ██║   ███████╗
╚═╝  ╚═╝╚══════╝╚══════╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝   ╚═╝   ╚══════╝
   
   By: Danilo Alfonso Basanta Montero                                                                                          
'''
    print(menu)
    
imprimir_menu()


def mostrar_menu():
    print("MENU:")
    print("1. Corriente del día - 10k")
    print("2. Carne asada - 20k")
    print("3. Pollo guisado - 15k")
    print("4. Opción 1 - precio")
    print("5. Opción 2 - precio")
    print("6. Opción 3 - precio")
    print("7. Opción 4 - precio")
    print("0. Salir")

def seleccionar_opcion():
    opcion = input("Selecciona una opción del menú: ")
    return opcion

def ejecutar_opcion(opcion):
    if opcion == "1":
        print("Has seleccionado: Corriente del día")
        print("Precio: 10k")
    elif opcion == "2":
        print("Has seleccionado: Carne asada")
        print("Precio: 20k")
    elif opcion == "3":
        print("Has seleccionado: Pollo guisado")
        print("Precio: 15k")
    elif opcion == "4":
        print("Has seleccionado: Opción 1")
        print("Precio: precio")
    elif opcion == "5":
        print("Has seleccionado: Opción 2")
        print("Precio: precio")
    elif opcion == "6":
        print("Has seleccionado: Opción 3")
        print("Precio: precio")
    elif opcion == "7":
        print("Has seleccionado: Opción 4")
        print("Precio: precio")
    elif opcion == "0":
        print("Saliendo del programa...")
    else:
        print("Opción inválida. Por favor, selecciona una opción válida del menú.")

mostrar_menu()
opcion = seleccionar_opcion()
ejecutar_opcion(opcion)
