salir = ""

while salir != "a":
    n1 = input("Ingresa un número: ")
    numero = int(n1)
    
    if numero % 2 == 0:
        print("Es par")
    else:
        print("Es impar")
    
    salir = input("Presiona 'a' para salir o cualquier otra tecla para continuar: ")