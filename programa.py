from datetime import date
import sqlite3
import hashlib
import os

conexion = sqlite3.connect("db.sqlite3")
cursor = conexion.cursor()
usuario = os.getlogin()

print('''Bienvenido al Gestor de Votaciones
1.- Crear usuario
2.- Responder encuestas
3.- Salir
''')
decision = int(input())

while decision != 3:
    if decision == 1:
        dni = input("Introduzca DNI del sujeto al cual se le va a crear una contraseña: ")
        fite = open(f"lectores.txt", "r")
        print(os.getlogin())
        print(fite)
        dniEncontrado = False
        fin = False
        while not dniEncontrado and not fin:
            i = fite.readline();
            try: 
                if dni in i:
                    print(i)
                    print("¡Se ha encontrado!")
                    dniEncontrado = True
                elif i == '':
                    fin = True
            except:
                fin = True
        if not dniEncontrado:
            print("No se ha encontrado el DNI, ¿seguro que lo has escrito bien?")
        elif dniEncontrado:
            contrasena = input(f"Introduzca contraseña del usuario {dni}: ")
            codificador = hashlib.md5(contrasena.encode())
            contrasenaEncriptada = codificador.hexdigest()
            acto = cursor.execute(f"UPDATE catalog_lector SET clave=? WHERE DNI=?", (contrasenaEncriptada, dni) )
            conexion.commit()
            print("¡Hecho!")
        fite.close()

        
    if decision == 2:
        dni = input("Inserte DNI del usuario: ")
        fite = open("lectores.txt", "r")
        control = open("control.txt", "r+")
        dniEncontrado = False
        fin = False
        while not dniEncontrado and not fin:
            i = fite.readline();
            try: 
                if dni in i:
                    print(i)
                    print("¡Se ha encontrado!")
                    dniEncontrado = True
                elif i == '':
                    fin = True
            except:
                fin = True
        if not dniEncontrado:
            print("No se ha encontrado el DNI, ¿seguro que lo has escrito bien?")
        elif dniEncontrado:
            contrasena = input("Inserte contraseña del usuario: ")
            codificador = hashlib.md5(contrasena.encode())
            contrasenaEncriptada = codificador.hexdigest()
            usuario = cursor.execute("SELECT * FROM catalog_lector WHERE DNI=?", (dni,) )
            usuario = usuario.fetchone()
            if usuario[6] != contrasenaEncriptada:
                print("LAS CONTRASEÑAS NO COINCIDEN")
            else:
                encuestas = cursor.execute("SELECT * FROM catalog_encuesta")
                print(f'''Bienvenido al gestor de votaciones, {usuario[2]}
Número de encuestas disponibles:''')
                encuestas = encuestas.fetchall()
                for i in encuestas:
                    print(f"{i[0]} - {i[5]}")
                decisionEncuesta = int(input("Elige número de la encuesta entre los disponibles: "))
                control.seek(69)
                controlEncuestas =  control.readlines()
                verificador = f"{usuario[0]}, {encuestas[decisionEncuesta-1][0]}"
                controlDefensa = False
                for i in controlEncuestas:
                    if i[:4] == verificador:
                        print("Ya has votado. ¿Para qué tanto votar?")
                        controlDefensa = True
                        break
                if not controlDefensa: 
                    print("Elige tu respuesta entre las disponibles: ")
                    respuestasEncuesta = cursor.execute("SELECT * FROM catalog_respuesta WHERE pregunta_id=?", (decisionEncuesta, ))
                    respuestasEncuesta = respuestasEncuesta.fetchall()
                    contador = 1
                    for i in respuestasEncuesta:
                        print(f" {contador} - {i[1]}")
                        contador+=1
                    decisionNumero = int(input())
                    votacion = cursor.execute("UPDATE catalog_respuesta SET votos=? WHERE id=?", 
                                            ((respuestasEncuesta[decisionNumero-1][2])+1, respuestasEncuesta[decisionNumero-1][0]))
                    conexion.commit()
                    control.read()
                    fechaActual = date.today()
                    control.write(f"\n{usuario[0]}, {encuestas[decisionEncuesta-1][0]}, {fechaActual}")
                    print("Votación hecha")

        control.close()
        fite.close()

    print('''\n-----------
Bienvenido al Gestor de Votaciones
1.- Crear usuario
2.- Responder encuestas
3.- Salir
''')
    decision = int(input())



fite.close()
conexion.close()
