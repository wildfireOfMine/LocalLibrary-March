""" DIVIDEBIEN
Función que se llama DIVIDIR(a, b) = a/b
VOy a pasar 4 entre 0 
QUE NO SE CONTROLE DESDE DIVIDE
SINO DESDE UN DECORADOR LLAMADO DIVIDEBIEN 
CONDICIONAR LA EJECUCIÓN DE ESE DIVIDE POR SI EL B ES 0"""

def divideBien(func):
    def envolvente(a, b):
        if b == 0:
            print("NO DIVIDAS CON 0")
        else:
            print(func(a, b))
    return envolvente

@divideBien
def dividir(a, b):
    return a/b
""" 
dividir(15, 2)
dividir(15, 77)
dividir(15, 0) """

""" Función que sume y al pricipio de la función que saque un Empiezo la función y al Final un 
Que se sumen todos los números entre 0 y 10
Termino la función """
def sumaBien(func):
    def envolvente(*a):
        suma = 0
        for i in a:
            if i < 0 or i > 10:
                print("No suma")
            else:
                suma += i
        return suma
    return envolvente

@sumaBien
def suma(*a):
    suma = 0
    print(a)
    for i in a:
        suma += i
    return suma

print(suma(1, 2, 3, 3, 4, 8, 123))
