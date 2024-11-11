import random
import zlib
import hashlib
import json
import time
import alive_progress
#
# Funciones de resumen
#
#Función lambda resumen CRC32 (32 bits) // truncada a numeroDeBits y convertida a hexadecimal
resumenCRC32 = lambda text: zlib.crc32(text.encode()).to_bytes(4, byteorder='big').hex()[-int(numeroDeBits/4):]

#Función lambda resumen mda5 (128 bits) pero usando los n últimos bits // truncada a numeroDeBits y convertida a hexadecimal
resumenMD5 = lambda text: hashlib.md5(text.encode()).hexdigest()[-int(numeroDeBits/4):]

#Función lambda resumen sha1 (160 bits) pero usando los n últimos bits // truncada a numeroDeBits y convertida a hexadecimal
resumenSHA1 = lambda text: hashlib.sha1(text.encode()).hexdigest()[-int(numeroDeBits/4):]

#Función lambda resumen sha256 (256 bits) pero usando los n últimos bits // truncada a numeroDeBits y convertida a hexadecimal
resumenSHA256 = lambda text: hashlib.sha256(text.encode()).hexdigest()[-int(numeroDeBits/4):]

#Función recodificadora que devuelve los n últimos caracteres // truncada a numeroDeBits y convertida a hexadecimal
recodi = lambda hash_str: funcion_decodificadora(hash_str)








# Generador de contraseñas dentro de el espacio de claves
def contraseña_aleatoria(n,chset):
    return ''.join(random.choices(chset, k=n))


# Funcion recodificadora que recodifica el resumen de la contraseña
def funcion_decodificadora(resumen):
    resultado = []
    for i in range(tamaño_ctr):
        cadenaentera = int(resumen, 16)
        # Calcular el valor modificado en cada posición
        valor_modificado = cadenaentera ^ (i * tamaño_espacio_de_claves ** i)
        # Reducirlo al rango del conjunto de caracteres
        caracter = caracteresdisp[valor_modificado % tamaño_espacio_de_claves]
        # Agregar el carácter resultante a la lista
        resultado.append(caracter)
    return ''.join(resultado)



#Funcion que genera la tabla arcoiris Implementación 1
def tabla_arcoiris(t_claves, funcion_resumen, funcion_recodificadora, n_filas, n_columnas, chset):
    tabla = {}
    for i in range(n_filas):
        contraseña_inicial= contraseña_aleatoria(t_claves,chset)
        for j in range(n_columnas):
            if(j == 0) : contraseña = contraseña_inicial
            contraseña = funcion_recodificadora(funcion_resumen(contraseña))
        tabla[funcion_resumen(contraseña)] = contraseña_inicial
    return tabla

#Funcion que realiza el ataque a la tabla arcoiris
def ataque_acoiris(tabla, funcion_resumen, funcion_recodificadora, n_columnas, hash_base):
    resumen = hash_base
    flag = False
    for i in range(n_columnas):
        if resumen in tabla.keys():
            flag = True
            break
        resumen = funcion_resumen(funcion_recodificadora(resumen))

    if flag:
        pwd = tabla[resumen]
        resumen = hash_base
        i = 0
        while funcion_resumen(pwd) != resumen and i < n_columnas:
            pwd = funcion_recodificadora(funcion_resumen(pwd))
            i += 1
        if i < n_columnas:
            return pwd
    return None

# main
if __name__ == "__main__":

    # Definición de espacio de claves: Conjunto de numérico de tamaño n
    caracteresdisp = 'abcdefghijklmnopqrstuvwxyz'
    tamaño_espacio_de_claves = len(caracteresdisp)
    tamaño_ctr = 5
    t = 50
    filas = 100
    numeroDeBits = 16
    funcion_resumen_a_utilizar = resumenCRC32

    print("generando tabla arcoiris")
    print("-----------")
    tiemp = time.time()
    tabla = tabla_arcoiris(tamaño_ctr, funcion_resumen_a_utilizar, recodi, filas, t, caracteresdisp)
    print("-----------")
    print("Tiempo de creación de la tabla: "+ str(time.time() - tiemp) + "s")
    print("Tamaño de la tabla: ", end="")
    print(len(tabla))

    
    # Test 1
    cont = 0
    numContr = 20
    contraseñas = [contraseña_aleatoria(tamaño_ctr, caracteresdisp) for i in range(numContr)]

    tiempos = []
    for ataque in contraseñas:
        print("Ataque contraseña: " + ataque + " con resumen: " + funcion_resumen_a_utilizar(ataque))
        print("-----------")
        hash_base = funcion_resumen_a_utilizar(ataque)
        tiemp = time.time()
        contraseñafalsa = ataque_acoiris(tabla, funcion_resumen_a_utilizar, recodi, t, hash_base)
        if contraseñafalsa == None:
            print("Contraseña no encontrada")
        else:
            print("Contraseña encontrada: ", contraseñafalsa)
            cont += 1
        print("-----------")
        print("Tiempo del ataque "+ str(contraseñas.index(ataque)) + ": " + str(time.time() - tiemp) + " s")
        print()
        tiempos.append(time.time() - tiemp)

    print("Contraseñas encontradas " + str(cont) + "/" + str(len(contraseñas)))
    print("Tiempo medio de ataque: ", str(sum(tiempos)/len(tiempos)) + " s")