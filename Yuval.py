import zlib
import hashlib


#extraemos las letras y posiciones a y e del texto
def extraer_letras(texto, n):
    letras = {}
    for i in range(len(texto)):
        if texto[i] == "A" or texto[i] == "a" or texto[i] == "E" or texto[i] == "e":
            letras[i] = texto[i]
    return dict(list(letras.items())[:n])



#Creamos un diccionario de 2^16 modificaciones con las letras a y e del mensaje legitimo en una funcion, y devolveremos una lista con los pares (mensaje, resumen)
def generador_mensajes_diccionario(texto, letras, funcion_resumen, ncomb):
    resultado = {}
    # Recorremos todas las combinaciones posibles de las letras a y e cambiadas por las letras a y e rusas
    for i in range(2**ncomb):
        mensaje = texto
        for j in range(ncomb):
            if i & (1 << j):
                mensaje = mensaje[:list(letras.keys())[j]] + diccionarioCambios[mensaje[list(letras.keys())[j]]] + mensaje[list(letras.keys())[j]+1:]
                resultado[funcion_resumen(mensaje)] = mensaje
    return resultado

def yuval(texto_legitimo, texto_ilegitimo, nbits, cambiosileg, resumen):
    cambiosleg = int(numeroDeBits/2)

    #Extraemos las letras a y e del texto legitimo
    letras_para_cambiar_legitimo = extraer_letras(texto_legitimo, cambiosleg)

    #Extraemos las letras a y e del texto ilegitimo
    letras_para_cambiar_ilegitimo = extraer_letras(texto_ilegitimo, cambiosileg)
    print(letras_para_cambiar_ilegitimo)

    # Recorremos todas las combinaciones posibles de las letras a y e cambiadas por las letras a y e rusas  
    combinaciones = generador_mensajes_diccionario(texto_legitimo,letras_para_cambiar_legitimo, resumen, cambiosleg)
    
    # Iteramos buscando colisiones con las combinaciones del texto legitimo preecreadas y las variaciones del texto ilegitimo
    for i in range(2**cambiosleg):
        mensaje = texto_ilegitimo
        for j in range(cambiosleg):
            if i & (1 << j):
                mensaje = mensaje[:list(letras_para_cambiar_ilegitimo.keys())[j]] + diccionarioCambios[mensaje[list(letras_para_cambiar_ilegitimo.keys())[j]]] + mensaje[list(letras_para_cambiar_ilegitimo.keys())[j]+1:]
                resumen_mensaje_ilegitimo = resumen(mensaje)
                if(resumen_mensaje_ilegitimo in combinaciones):
                    return combinaciones[resumen_mensaje_ilegitimo], mensaje, resumen_mensaje_ilegitimo
    
    return None


def yuval_conjunto_colisiones(texto_legitimo, texto_ilegitimo, nbits, cambiosileg, resumen, max_colisiones = 15):
 
    cambiosleg = int(numeroDeBits/2)

    lista_resultados = []

    #Extraemos las letras a y e del texto legitimo
    letras_para_cambiar_legitimo = extraer_letras(texto_legitimo, cambiosleg)

    #Extraemos las letras a y e del texto ilegitimo
    letras_para_cambiar_ilegitimo = extraer_letras(texto_ilegitimo, cambiosileg)
    
    # Recorremos todas las combinaciones posibles de las letras a y e cambiadas por las letras a y e rusas  
    combinaciones = generador_mensajes_diccionario(texto_legitimo,letras_para_cambiar_legitimo, resumen, cambiosleg)
    

    # Iteramos buscando colisiones con las combinaciones del texto legitimo preecreadas y las variaciones del texto ilegitimo
    for i in range(2**cambiosileg):
        mensaje = texto_ilegitimo
        for j in range(cambiosileg):
            if i & (1 << j):
                mensaje = mensaje[:list(letras_para_cambiar_ilegitimo.keys())[j]] + diccionarioCambios[mensaje[list(letras_para_cambiar_ilegitimo.keys())[j]]] + mensaje[list(letras_para_cambiar_ilegitimo.keys())[j]+1:]
                resumen_mensaje_ilegitimo = resumen(mensaje)
                if(resumen_mensaje_ilegitimo in combinaciones):
                    lista_resultados.append([combinaciones[resumen_mensaje_ilegitimo], mensaje, resumen_mensaje_ilegitimo])
                    if(len(lista_resultados) == max_colisiones):
                        return lista_resultados
    
    return lista_resultados

# main
if __name__ == "__main__":

    diccionarioCambios = {"a": "а", "e": "е", "A": "А", "E": "Е"}
    numeroDeBits = 32
    cambiosile = 24

    #Función lambda resumen CRC32 (32 bits)
    resumenCRC32 = lambda text: zlib.crc32(text.encode())

    #Función lambda resumen mda5 (128 bits) pero usando los n últimos bits
    resumenMD5 = lambda text: hashlib.md5(text.encode()).hexdigest()[-int(numeroDeBits/4):]

    #Función lambda resumen sha1 (160 bits) pero usando los n últimos bits
    resumenSHA1 = lambda text: hashlib.sha1(text.encode()).hexdigest()[-int(numeroDeBits/4):]

    #Función lambda resumen sha256 (256 bits) pero usando los n últimos bits
    resumenSHA256 = lambda text: hashlib.sha256(text.encode()).hexdigest()[-int(numeroDeBits/4):]

    #Abrimos el texto legitimo
    f = open("Texto Legitimo.txt", "r", encoding = "utf-8")
    texto_legitimo = f.read()
    f.close()

    #Abrimos el texto ilegitimo
    f = open("Texto Ilegitimo.txt", "r", encoding = "utf-8")
    texto_ilegitimo = f.read()
    f.close()
    
    # función resumen CRC32 (32 bits)
    resultado = yuval(texto_legitimo, texto_ilegitimo, numeroDeBits, cambiosile , resumenSHA256)

    #Escribir el resultado en un fichero de texto
    f = open("Texto Ilegitimo firmado.txt", "w", encoding = "utf-8")
    f.write(resultado[1])
    f.close()

    # resultado = yuval_conjunto_colisiones(texto_legitimo, texto_ilegitimo, numeroDeBits, cambiosile , resumenCRC32,10)
    # print(len(resultado))
