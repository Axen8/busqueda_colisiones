import random
import zlib
import hashlib
import json
import time

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
recodi = lambda hash_str,index: funcion_decodificadora(hash_str, index)








# generador de contraseñas dentro de el espacio de claves
def contraseña_aleatoria(n,chset):
    return ''.join(random.choices(chset, k=n))

def funcion_decodificadora(resumen, n):
    resultado = []
    for i in range(tamaño_ctr):
        cadenaentera = int(resumen, 16)
        # Calcular el valor modificado en cada posición con un xor
        valor_modificado = cadenaentera ^ ((n+1) * tamaño_espacio_de_claves ** i)
        # Reducirlo al rango del conjunto de caracteres
        caracter = caracteresdisp[valor_modificado % tamaño_espacio_de_claves]
        # Agregar el carácter resultante a la lista
        resultado.append(caracter)
    # Unir todos los caracteres en una cadena
    return ''.join(resultado)

def guardar_tabla_json(tabla, nombre_fichero):
    with open(nombre_fichero, "w") as f:
        json.dump(tabla, f)

def cargar_tabla_json(nombre_fichero):
    with open(nombre_fichero, "r") as f:
        return json.load(f)


#Funcion que genera la tabla arcoiris
def tabla_arcoiris(t_claves, funcion_resumen, funcion_recodificadora, n_filas, n_columnas, chset):
    tabla = {}
    for i in range(n_filas):
        ctr_ini= contraseña_aleatoria(t_claves,chset)
        for j in range(n_columnas):
            if(j == 0) : contraseña = ctr_ini
            contraseña = funcion_recodificadora(funcion_resumen(contraseña), j)
        tabla[funcion_resumen(contraseña)] = ctr_ini
    guardar_tabla_json(tabla, "tabla_arcoiris.json")

def ataque_acoiris(tabla, funcion_resumen, funcion_recodificadora, n_columnas, hash_base):
    resumen = hash_base
    for j in range(n_columnas,0,-1):
        for k in range(j, n_columnas):
            if resumen in tabla.keys():
                pwd = tabla[resumen]
                resumen = hash_base
                i = 0
                # El while está dentro del for para que si se encuentra una colisión con un hash erroneo, se pueda seguir buscando
                while funcion_resumen(pwd) != resumen and i<n_columnas:
                    pwd = funcion_recodificadora(funcion_resumen(pwd), i)
                    i +=1 
                if funcion_resumen(pwd) == resumen:
                    return pwd
            resumen = funcion_resumen(funcion_recodificadora(resumen, k))
    return None

# main
if __name__ == "__main__":

    # Definición de espacio de claves: Conjunto de numérico de tamaño n
    caracteresdisp = 'abcdefghijklmnopqrstuvwxyz'
    tamaño_espacio_de_claves = len(caracteresdisp)
    tamaño_ctr = 5
    t = 50
    filas = 500000
    #contraseña_base = "abcde"  
    numeroDeBits = 40
    funcion_resumen_a_utilizar = resumenMD5
    
    # print("Contraseña real: ", contraseña_base)
    # print("Resumen de la contraseña real: ", funcion_resumen_a_utilizar(contraseña_base))
    # print("-----------")

    # hash_base = funcion_resumen_a_utilizar(contraseña_base)
    # print("generando tabla arcoiris")
    # print("-----------")
    # tiemp = time.time()
    # #tabla_arcoiris(tamaño_ctr, funcion_resumen_a_utilizar, recodi, filas, t, caracteresdisp)
    # print("-----------")
    # print("Tiempo de creación de la tabla: "+ str(time.time() - tiemp) + "s")
    # tabla = cargar_tabla_json("tabla_arcoiris.json") 
    # print("Tamaño de la tabla: ", end="")
    # print(len(tabla))

    
    # # Test 1
    # cont = 0
    # numContr = 20
    # contraseñas = [contraseña_aleatoria(tamaño_ctr, caracteresdisp) for i in range(numContr)]

    # tiempos = []
    # for ataque in contraseñas:
    #     print("Ataque con contraseña: " + ataque + " con resumen: " + funcion_resumen_a_utilizar(ataque))
    #     print("-----------")
    #     hash_base = funcion_resumen_a_utilizar(ataque)
    #     tiemp = time.time()
    #     contraseñafalsa = ataque_acoiris(tabla, funcion_resumen_a_utilizar, recodi, t, hash_base)
    #     if contraseñafalsa == None:
    #         print("Contraseña no encontrada")
    #     else:
    #         print("Contraseña encontrada: ", contraseñafalsa)
    #         cont += 1
    #     print("-----------")
    #     print("Tiempo del ataque "+ str(contraseñas.index(ataque)) + ": " + str(time.time() - tiemp) + " s")
    #     print()
    #     tiempos.append(time.time() - tiemp)

    # print("Contraseñas encontradas " + str(cont) + "/" + str(len(contraseñas)))
    # print("Tiempo medio de ataque: ", str(sum(tiempos)/len(tiempos)) + " s")

    # Test 2
    # Análisis del número de colisiones en funcion de la longitud del resumen
    numContr = 150
    t = 5
    filas = 100000
    contraseñas = [contraseña_aleatoria(tamaño_ctr, caracteresdisp) for i in range(numContr)]
    bits = [8, 12, 16, 20, 24, 28, 32]
    funcion_resumen = {"resumenSHA1":resumenSHA1, "resumenSHA256": resumenSHA256, "resumenMD5": resumenMD5, "resumenCRC32": resumenCRC32}
    bitsporAciertos = []
    aciertos = []
    func = []
    for nombrefun, fun in funcion_resumen.items():
        for nbits in bits:
            numeroDeBits = nbits
            funcion_resumen_a_utilizar = fun
            tabla_arcoiris(tamaño_ctr, funcion_resumen_a_utilizar, recodi, filas, t, caracteresdisp)
            tabla = cargar_tabla_json("tabla_arcoiris.json")
            cont = 0
            for ataque in contraseñas:
                hash_base = funcion_resumen_a_utilizar(ataque)
                contraseñafalsa = ataque_acoiris(tabla, funcion_resumen_a_utilizar, recodi, t, hash_base)
                if contraseñafalsa != None:
                    cont += 1
            func.append(nombrefun)
            bitsporAciertos.append(nbits)
            aciertos.append(cont)
    print(func)
    print(bitsporAciertos)
    print(aciertos)