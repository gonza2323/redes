
BANDERA = int("7E", 16)
ESCAPE = int("7D", 16)

longitud_incorrecta = 0
checksum_incorrecta = 0
cant_secs_escape = 0


# leer archivo y separarlo en lista de bytes

with open("tramas.log", "r") as file:
    content = file.read()

bytes = [int(content[i:i+2], 16) for i in range(0, len(content)-1, 2)]


# generamos las tramas en base a la presencia de delimitadores

tramas = []
trama = []
isEscaped = False
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
        cant_secs_escape += 1
        continue

    if (byte == BANDERA):
        tramas.append(trama)
        trama = []
        continue

    trama.append(byte)
tramas.append(trama)

total_tramas = len(tramas)


# para cada trama, verificamos si la longitud y checksum son correctas

for trama in tramas:
    longitud = trama[0] * 256 + trama[1]
    
    if (longitud != len(trama) - 3):
        longitud_incorrecta += 1
        continue
    
    checksum1 = trama[-1]

    suma = sum(trama[2:-1])
    checksum2 = 0xFF - (suma & 0xFF)
    
    if (checksum1 != checksum2):
        checksum_incorrecta += 1


longitud_correcta = total_tramas - longitud_incorrecta
checksum_correcta = longitud_correcta - checksum_incorrecta


# imprimir resultados

print("Total de tramas = ", total_tramas)
print("Tramas con long. correcta = ", longitud_correcta)
print("Tramas con long. incorrecta = ", longitud_incorrecta)
print("Tramas con long. y checksum correctas = ", checksum_correcta)
print("Tramas con long correcta y checksum incorrecta = ", checksum_incorrecta)
print("Cantidad de secuencias de escape = ", cant_secs_escape)
