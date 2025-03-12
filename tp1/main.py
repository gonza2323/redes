
# constantes

BANDERA = int("7E", 16)
ESCAPE = int("7D", 16)


# aux

def tramaToString(trama):
    tramaStr = " ".join(format(byte, "02X") for byte in trama)
    return tramaStr


# leer archivo y separarlo en lista de bytes

with open("tramas.log", "r") as file:
    content = file.read()

bytes = [int(content[i:i+2], 16) for i in range(0, len(content)-1, 2)]


# generamos las tramas en base a la presencia de delimitadores

tramas = []
trama = []
isEscaped = False
wasEscaped = False
cant_secs_escape = 0
for i in range(1, len(bytes)):
    byte = bytes[i]

    if (isEscaped):
        if (byte == ESCAPE or byte == BANDERA):
            trama.append(byte)
            continue
        else:
            isEscaped = False

    if (byte == ESCAPE):
        isEscaped = True
        wasEscaped = True;
        cant_secs_escape += 1
        continue
    
    if (byte == BANDERA or i == len(bytes) - 1):
        if (i == len(bytes) - 1):
            tramas.append(trama)
        
        if (wasEscaped):
            print(f"La línea Nro. {len(tramas)} tiene una secuencia de escape. La línea es:")
            print(tramaToString(trama))
        
        tramas.append(trama)
        wasEscaped = False;
        trama = []
        continue

    trama.append(byte)

    if (i == len(bytes) - 1):
        tramas.append(trama)


total_tramas = len(tramas)


# para cada trama, verificamos si la longitud y checksum son correctas

print()
longitud_incorrecta = 0
checksum_incorrecta = 0
for i, trama in enumerate(tramas):
    longitud = trama[0] * 256 + trama[1]
    
    if (longitud != len(trama) - 3):
        longitud_incorrecta += 1
        print(f"La línea Nro. {i} tiene la longitud incorrecta. La línea es:")
        print(tramaToString(trama))
        continue
    
    checksum1 = trama[-1]

    suma = sum(trama[2:-1])
    checksum2 = 0xFF - (suma & 0xFF)
    
    if (checksum1 != checksum2):
        print(f"La línea Nro. {i} tiene una checksum incorrecta. La línea es:")
        print(tramaToString(trama))
        checksum_incorrecta += 1


longitud_correcta = total_tramas - longitud_incorrecta
checksum_correcta = longitud_correcta - checksum_incorrecta


# imprimir resultados

print()
print("Total de tramas = ", total_tramas)
print("Tramas con long. correcta = ", longitud_correcta)
print("Tramas con long. incorrecta = ", longitud_incorrecta)
print("Tramas con long. y checksum correctas = ", checksum_correcta)
print("Tramas con long correcta y checksum incorrecta = ", checksum_incorrecta)
print("Cantidad de secuencias de escape = ", cant_secs_escape)
