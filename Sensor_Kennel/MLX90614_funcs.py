
def checkCRC(k, mask):  # mask (matching nibble) different in case
    inCrc = 0
    for inData in [k[0], k[1]]:
        data = inCrc ^ inData;
        data <<= 8 
        for i in range(8):
            if (( data & 0x8000 ) != 0 ):
                data = data ^ (0x1070 << 3)
            data = data << 1
        inCrc = data >> 8
    return (inCrc & mask) == (k[2]&mask)

def mlx90614temps(i2c):
    try:
        ka = i2c.readfrom_mem(0x5a, 0x06, 3)
        ki = i2c.readfrom_mem(0x5a, 0x07, 3)
        bcrcgood = (checkCRC(ka, 0x0F) and checkCRC(ki, 0xF0))
    except OSError:
        bcrcgood = False
    if bcrcgood:
        tempAmbient = (ka[0]+ka[1]*256)*0.02 - 273.15
        tempIR = (ki[0]+ki[1]*256)*0.02 - 273.15
        return tempAmbient, tempIR
    else:
        return None, None
    