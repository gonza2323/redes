
BANDERA = "7E"
ESCAPE = "7D"

content = ""
with open("tramas.log", "r") as file:
    content = file.read()

bytes = [content[i:i+2] for i in range(0, len(content)-1, 2)]

cant_sec_escape = 0

tramas = []

isEscaped = False
trama = []
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
        cant_sec_escape += 1
        continue

    if (byte == BANDERA):
        tramas.append(trama)
        trama = []
        continue

    trama.append(byte)

tramas.append(trama)


total_tramas = len(tramas)
long_incorrecta = 0
checksum_incorrecta = 0

for trama in tramas:
    fstByte = trama[0]
    sndByte = trama[1]

    longitud = int(fstByte + sndByte, 16)
    
    if (longitud != len(trama) - 3):
        long_incorrecta += 1
        continue
    
    checksum1 = int(trama[-1], 16)

    nums = [int(byte, 16) for byte in trama[2:-1]]
    suma = sum(nums)
    checksum2 = 0xFF - (suma & 0xFF)
    
    if (checksum1 != checksum2):
        checksum_incorrecta += 1


long_correcta = total_tramas - long_incorrecta
checksum_correcto = long_correcta - checksum_incorrecta

print("total_tramas = ", total_tramas)
print("long_incorrecta = ", long_incorrecta)
print("long_correcta = ", long_correcta)
print("checksum_incorrecta = ", checksum_incorrecta)
print("checksum_correcto = ", checksum_correcto)
print("cant_sec_escape = ", cant_sec_escape)
