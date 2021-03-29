# Import Stuff: ********************************************************************************************************
import hashlib
from PIL import Image
import random
from Crypto.Cipher import AES

# "Private" Functions: *************************************************************************************************
########################################################################################################################
# Convert number to binary: ********************************************************************************************
def _convertIntToBinary(numIn, totalBits=8):
    numIn = numIn % 2**totalBits
    bitStr = '#0' + str(totalBits + 2) + 'b'
    if 2**totalBits <= numIn:
        numIn = numIn % 2**totalBits
    return format(numIn, bitStr)

# Convert Binary to int: ***********************************************************************************************
def _convertBinaryToInt(binIn):
    return int(binIn, 2)

# Perfomr xor: *********************************************************************************************************
def _xor(bin1, bin2):
    # Expects binary strings in the form '0bxxxx'
    # Also assumes both binary strings are the same lenght. They gotta be or this won't work
    strOut = ['0', 'b']

    for i in range(2, len(bin1)):
        strOut.append(str(int(bin1[i] != bin2[i])))

    return strOut

# Do _superHash: *******************************************************************************************************
def _superHash(password, salt, numIts):
    # Returns a hash as a binary
    x = "0".encode('utf8')
    password = password.encode('utf8')
    salt = salt.encode('utf8')

    for i in range(numIts):
        x = hashlib.sha256(x + password + salt).digest()

    hashArray = bytearray(x)
    numList = []
    for byte in hashArray:
        numList.append(int(byte))

    hashOut = "0b"

    for i in numList:
        hashOut += _convertIntToBinary(i)[2::]

    return hashOut

# Feistel Encryption: **************************************************************************************************
def _feistelEncrpytion(valIn, K):

    # Convert value in to binary
    binIn = list(_convertIntToBinary(valIn, 512))

    # define number of iterations
    numIts = 5000

    # Split into left and right parts
    Rstring = '0b' + _listToString(binIn[258:514])
    Lstring = '0b' + _listToString(binIn[2:258])

    # Get F0
    F = _superHash(str(_convertBinaryToInt(Rstring)), K[0], numIts)

    # Get new L
    Lstring = _listToString(_xor(list(F), list(Lstring)))

    # Get New F
    F = _superHash(str(_convertBinaryToInt(Lstring)), K[1], numIts)

    # Get new R
    Rstring = _listToString(_xor(list(F), list(Rstring)))

    # Get new F
    F = _superHash(str(_convertBinaryToInt(Rstring)), K[2], numIts)

    # Get New L
    Lstring = _listToString(_xor(list(F), list(Lstring)))

    # Get Last F
    F = _superHash(str(_convertBinaryToInt(Lstring)), K[3], numIts)

    # Get Last R
    Rstring = _listToString(_xor(list(F), list(Rstring)))

    # Combine our strings and see what we get
    outStr = '0b' + _listToString(Rstring[2::]) + _listToString(Lstring[2::])

    return outStr

# Feistel Decryption: **************************************************************************************************
def _feistelDecrpytion(valIn, K):
    binIn = list(_convertIntToBinary(valIn, 512))

    # Split into left and right parts
    Lstring = '0b' + _listToString(binIn[258:514])
    Rstring = '0b' + _listToString(binIn[2:258])

    # Define Number of iterations
    numIts = 5000

    # Get F0
    F = _superHash(str(_convertBinaryToInt(Lstring)), K[3], numIts)

    # Get new L
    Rstring = _listToString(_xor(list(F), list(Rstring)))

    # Get New F
    F = _superHash(str(_convertBinaryToInt(Rstring)), K[2], numIts)

    # Get new R
    Lstring = _listToString(_xor(list(F), list(Lstring)))

    # Get new F
    F = _superHash(str(_convertBinaryToInt(Lstring)), K[1], numIts)

    # Get New L
    Rstring = _listToString(_xor(list(F), list(Rstring)))

    # Get Last F
    F = _superHash(str(_convertBinaryToInt(Rstring)), K[0], numIts)

    # Get Last R
    Lstring = _listToString(_xor(list(F), list(Lstring)))

    # Combine our strings and see what we get
    outStr = '0b' + _listToString(Lstring[2::]) + _listToString(Rstring[2::])
    return outStr

# Convert Image to binary chunks: **************************************************************************************
def _convertImageToBinaryChunks(imageLoc, chunkSize = 512, padIn=0):
    # Load the image
    tImage = Image.open(imageLoc)
    if tImage.mode != 'RGB':
        tImage.convert('RGB')
    pixelValues = list(tImage.getdata())
    imageSize = tImage.size

    # Convert non-tuples in the image pixel values to tuples
    for i in range(len(pixelValues)):
        if isinstance(pixelValues[i], int):
            pixelValues[i] = (pixelValues[i], pixelValues[i], pixelValues[i])
        elif len(pixelValues[i]) > 3:
            pixelValues[i] = (pixelValues[i][1], pixelValues[i][2], pixelValues[i][3])

    # Concatinate binary strings
    fullBinaryStr = '0b'
    for i in pixelValues:
        fullBinaryStr += _convertTupleToBinary(i)[2::]

    # Confirm we have the correct size
    # We are going to add full on bytes
    # We also assume chunk size is a multiple of 8 so this should always remove
    # IF we want chunk sizes that are not multiples of 8 we will have to revisit
    # It should also be a multiple of 3 since we are using RGB values, so include that as well
    if padIn != 0:
        randStrToAdd = padIn
    else:
        tLeftover = (chunkSize*3 - ((len(fullBinaryStr) - 2) % chunkSize*3)) // 8

        # Add randomized binary to the end. Doesn't actually matter what's here cuz we'll cut it off anyway
        # But we should still do it, because it feels more secure lol
        randBytes = random.SystemRandom().randbytes(tLeftover)
        randArray = bytearray(randBytes)
        randList = []
        for byte in randArray:
            randList.append(int(byte))
        randStrToAdd = ''
        for i in randList:
            randStrToAdd += _convertIntToBinary(i)[2::]

    # Now add it to the string
    fullBinaryStr += randStrToAdd

    # Now convert this to chunks
    tStr = fullBinaryStr[2::]
    plainChunks = [tStr[i:i + chunkSize] for i in range(0, len(tStr), chunkSize)]

    # Return what we want
    return plainChunks, imageSize

# Convert Bytes to RGB tuples: *****************************************************************************************
def _convertBytesToRgbTuples(b):
    # Convert to rgb values
    rgbList = []
    for c in b:
        rgbList.append(c)

    # Convert this list to tuple
    tupleList = []
    tupleGroups = [rgbList[i:i + 3] for i in range(0, len(rgbList), 3)]
    count = 0
    for i in tupleGroups:
        tTuple = (i[0], i[1], i[2])
        tupleList.append(tTuple)

    # Return the tuple list
    return tupleList

# Convert Binary chunks to image: **************************************************************************************
def _convertBinaryChunksToRgbTuples(binChunks):
    # Convert binary chunks to rgb values
    rgbList = []
    for chunk in binChunks:
        if len(chunk) != 512:
            print(len(chunk))
        subChunks = [chunk[i:i + 8] for i in range(0, len(chunk), 8)]
        for s in subChunks:
            rgbList.append(int(s, 2))

    # Convert this list to tuple
    tupleList = []
    tupleGroups = [rgbList[i:i + 3] for i in range(0, len(rgbList), 3)]
    count = 0
    for i in tupleGroups:
        tTuple = (i[0], i[1], i[2])
        tupleList.append(tTuple)

    # Return the tuple list
    return tupleList

# Convert List to String: **********************************************************************************************
def _listToString(s):
    # initialize an empty string
    str1 = ""

    # traverse in the string
    try:
        for ele in s:
            str1 += ele
    except:
        return 1

        # return string
    return str1

# Save Tuple list as image: ********************************************************************************************
def _saveTupleListAsImage(tupleList, imageSize, imagePath='testImage.png'):

    image = Image.new('RGB', imageSize)

    # Ensure our tuple list is the correct size
    tupleList = tupleList[0:imageSize[0]*imageSize[1]]


    image.putdata(tupleList)
    image.save(imagePath)

# Convert Binary to Tuple: *********************************************************************************************
def convertBinaryToTuple(binaryIn, numBits=8):
    # Initialze output
    tupleOut = tuple()

    # Convert binary to chunks


    return tupleOut

# Convert Tuple to Binary: *********************************************************************************************
def _convertTupleToBinary(tupleIn, numBits=8):
    # Initialize the output
    strOut = '0b'

    for i in tupleIn:
        strOut += _convertIntToBinary(i, numBits)[2::]

    return strOut

# Encrpytion Stuff (Still "Private:): **********************************************************************************
########################################################################################################################
# Electronic Code Book Encrpytion: *************************************************************************************
def _ecbEncryption(pText, key):
    # P text is given in the form of binary chunks
    # output cipher text is given also in binary chunks
    print('Performing ECB Encryption...')

    cText = []
    idx = 1
    for text in pText:
        if idx % 100 == 0:
            print(str(idx) + " of " + str(len(pText)))
        idx += 1
        cText.append(_feistelEncrpytion(int(text, 2), key)[2::])

    print('ECB Encryption Complete!')

    return cText

# Electronic Code Book Decryption: *************************************************************************************
def _ecbDecryption(cText, key):
    print('Performing ECB Decryption...')

    pText = []
    idx = 1
    for text in cText:
        if idx % 100 == 0:
            print(str(idx) + " of " + str(len(cText)))
        idx += 1
        pText.append(_feistelDecrpytion(int(text, 2), key)[2::])

    print('ECB Decryption Complete!')

    return pText

# Cipher Block Chaining Encryption: ************************************************************************************
def _cbcEncryption(pText, IV, key):
    print('Performing CBC Encryption...')

    cText = []
    idx = 1
    IV = _convertIntToBinary(IV, len(pText[0]))
    for text in pText:
        if idx % 100 == 0:
            print(str(idx) + " of " + str(len(pText)))
        idx += 1
        upPText = _listToString(_xor("0b"+text, IV))[2::]
        IV = _feistelEncrpytion(int(upPText, 2), key)
        cText.append(IV[2::])
    print('CBC Encryption Complete!')

    return cText

# Cipher Block Chaining Encryption: ************************************************************************************
def _cbcDecryption(cText, IV, key):
    print('Performing CBC Decryption...')

    pText = []
    idx = 1
    IV = _convertIntToBinary(IV, len(cText[0]))
    for text in cText:
        if idx % 100 == 0:
            print(str(idx) + " of " + str(len(cText)))
        idx += 1
        blockCipherDecrypt = _feistelDecrpytion(int(text, 2), key)
        pText.append(_listToString(_xor(IV, blockCipherDecrypt))[2::])
        IV = '0b' + text
    print('CBC Decryption Complete!')

    return pText

# OFB Mode Encryption: *************************************************************************************************
def _ofbEncryption(pText, IV, key):
    print('Performing OFB Encryption...')

    cText = []
    idx = 1
    IV = _convertIntToBinary(IV, len(pText[0]))

    for text in pText:
        if idx % 100 == 0:
            print(str(idx) + " of " + str(len(pText)))
        idx += 1

        bEncrypt = _feistelEncrpytion(int(IV, 2), key)

        cText.append(_listToString(_xor(bEncrypt, "0b" + text))[2::])
        IV = bEncrypt

    print("OFB Encryption Complete!")

    return cText

# OFB Mode Decryption: *************************************************************************************************
def _ofbDecryption(cText, IV, key):
    print('Performing OFB Decryption...')

    pText = []
    idx = 1
    IV = _convertIntToBinary(IV, len(cText[0]))

    for text in cText:
        if idx % 100 == 0:
            print(str(idx) + " of " + str(len(cText)))
        idx += 1

        bEncrypt = _feistelEncrpytion(int(IV, 2), key)

        pText.append(_listToString(_xor(bEncrypt, "0b" + text))[2::])
        IV = bEncrypt

    print("OFB Decryption Complete!")

    return pText

# CTR Mode Encryption: *************************************************************************************************
def _ctrEncryption(pText, nonce, key):
    print('Performing CTR Encryption...')

    cText = []
    idx = 1
    nonce = _convertIntToBinary(nonce, len(pText[0])//2)
    nonce = _convertBinaryToInt(nonce + _convertIntToBinary(0, len(pText[0])//2)[2::])
    for text in pText:
        if idx % 100 == 0:
            print(str(idx) + " of " + str(len(pText)))
        IV = nonce + idx - 1
        idx += 1

        bEncrypt = _feistelEncrpytion(IV, key)

        cText.append(_listToString(_xor(bEncrypt, "0b" + text))[2::])

    print('CTR Encryption Complete!')

    return cText

# CTR Mode Decryption: *************************************************************************************************
def _ctrDecryption(pText, nonce, key):
    print('Performing CTR Encryption...')

    cText = []
    idx = 1
    nonce = _convertIntToBinary(nonce, len(pText[0]) // 2)
    nonce = _convertBinaryToInt(nonce + _convertIntToBinary(0, len(pText[0]) // 2)[2::])
    for text in pText:
        if idx % 100 == 0:
            print(str(idx) + " of " + str(len(pText)))
        IV = nonce + idx - 1
        idx += 1

        bEncrypt = _feistelEncrpytion(IV, key)

        cText.append(_listToString(_xor(bEncrypt, "0b" + text))[2::])

    print('CTR Encryption Complete!')

    return cText

# Convert Key to 4 Keys: ***********************************************************************************************
def _convertKeyToFourKeys(key):
    fullK = hex(int(_superHash(key, '', 5000), 2))[2::]
    n = len(fullK) // 4
    K = [fullK[i:i + n] for i in range(0, len(fullK), n)]
    return K

# Convert Byte Message to plain text: **********************************************************************************
def _convertByteMessageToPlainText(msgBytes):
    msgAsStr = ''
    for i in msgBytes:
        msgAsStr += chr(i)

    return msgAsStr

# Public Functions: ****************************************************************************************************
########################################################################################################################
# Do Encryption: *******************************************************************************************************
def encrypt(imageLoc, saveLoc, aMode, key=-1, IV=-1, bcType='AES'):
    # Initialize an output
    padOut = -1
    # Lower the bcType
    bcType = bcType.lower()

    # Handle missing key
    if key == -1:
        key = str(random.SystemRandom().randint(0, 2**256-1))
    if bcType == 'feistel':
        key = str(key)
        keyToReturn = key

        # Convert key to 4 keys
        K = _convertKeyToFourKeys(key)

        # Convert original image to binary
        x = _convertImageToBinaryChunks(imageLoc)
        binChunks = x[0]
        imSize = x[1]

        # Handle missing IV
        if IV == -1 and aMode != 'ebc':
            IVint = random.SystemRandom().randint(0, 2**256-1)
        else:
            # Convert IV to integer
            IVint = int(''.join(str(ord(c)) for c in IV))

        # Do the decryption
        aMode = aMode.lower()
        if aMode == 'cbc':
            eText = _cbcEncryption(binChunks, IVint, K)
        elif aMode == 'ctr':
            eText = _ctrEncryption(binChunks, IVint, K)
        elif aMode == 'ecb':
            eText = _ecbEncryption(binChunks, K)
        elif aMode == 'ofb':
            eText = _ofbEncryption(binChunks, IVint, K)
        elif aMode == 'ofbbad':
            eText = _ofbEncryption(binChunks, IVint, [key] * 4)
        else:
            print('Invalid or Unsupported Encryption Mode Entered')
            return

        # Convert this to RGB tuples
        rgbTuples = _convertBinaryChunksToRgbTuples(eText)

        # Write our output
        _saveTupleListAsImage(rgbTuples, imSize, saveLoc)

    elif bcType == 'aes':
        print('Performing AES Encryption...')
        # Convert key and IV into something useable
        keyToReturn = key
        key = hashlib.sha256(key.encode('utf-8')).digest()
        if IV != -1:
            iv = hashlib.sha256(IV.encode('utf-8')).digest()[0:16]

        # Determine the decryption mode
        aMode = aMode.lower()
        if aMode == 'cbc':
            if IV == -1:
                cipher = AES.new(key, AES.MODE_CBC)
                iv = cipher.iv
            else:
                cipher = AES.new(key, AES.MODE_CBC, iv)
        elif aMode == 'ctr':
            if IV == -1:
                cipher = AES.new(key, AES.MODE_CTR)
                iv = cipher.nonce
            else:
                cipher = AES.new(key, AES.MODE_CTR, nonce=iv[0:8])
        elif aMode == 'ecb':
            cipher = AES.new(key, AES.MODE_ECB)
            iv = -1
        elif aMode == 'ofb':
            if IV == -1:
                cipher = AES.new(key, AES.MODE_OFB)
                iv = cipher.iv
            else:
                cipher = AES.new(key, AES.MODE_OFB, iv)
        elif aMode == 'gcm':
            if IV == -1:
                cipher = AES.new(key, AES.MODE_GCM)
                iv = cipher.nonce
            else:
                cipher = AES.new(key, AES.MODE_GCM, nonce=iv)
        else:
            print('Invalid Decryption Mode Entered')
            return

        # Convert iv and key to string
        # Encrypt the data
        im = Image.open(imageLoc)
        imSize = im.size
        tData = im.tobytes()

        # Add a pad if needed
        if aMode == 'cbc' or aMode == 'ecb':
            length = AES.block_size - (len(im.tobytes()) % AES.block_size)
            tData += bytes([length])*length
        imageBytesOut = cipher.encrypt(tData)

        # Store the encrypted pad data
        if aMode == 'cbc' or aMode == 'ecb':
            padOut = imageBytesOut[-length::]

        # Save the Data
        t = Image.frombytes(im.mode, imSize, imageBytesOut)
        t.save(saveLoc)

        print('AES Encryption Complete!')

    else:
        print('Invalid BC type entered (Feistel or AES)')
        return

    # Get original image hash
    im = Image.open(imageLoc)
    tHash = hashlib.sha256(im.tobytes()).hexdigest()

    # Return IV and key
    if isinstance(keyToReturn, bytes):
        keyToReturn = _convertByteMessageToPlainText(keyToReturn)
    if IV != -1:
        iv = IV

    if bcType.lower() == 'aes':
        return keyToReturn, iv, tHash, padOut, cipher
    else:
        IVstr = str(''.join(str(chr(int(c))) for c in list(str(IVint))))
        return keyToReturn, IVstr, tHash

# Do Decryption: *******************************************************************************************************
def decrypt(imageLoc, saveLoc, aMode, key, IV=-1, bcType='AES', imHash = -1, padIn = -1):
    if IV == -1 and aMode.lower() != 'ecb':
        print('Cannot perform decryption. No valid IV entered.')
        return

    bcType = bcType.lower()
    if bcType == 'feistel':
        # Convert key to 4 keys
        K = _convertKeyToFourKeys(key)

        # Convert original image to binary
        if padIn == -1:
            padIn = 0
        x = _convertImageToBinaryChunks(imageLoc, padIn=padIn)
        binChunks = x[0]
        imSize = x[1]

        # Convert IV to integer
        IVint = int(''.join(str(ord(c)) for c in IV))

        # Do the decryption
        aMode = aMode.lower()
        if aMode == 'cbc':
            eText = _cbcDecryption(binChunks, IVint, K)
        elif aMode == 'ctr':
            eText = _ctrDecryption(binChunks, IVint, K)
        elif aMode == 'ecb':
            eText = _ecbDecryption(binChunks, K)
        elif aMode == 'ofb':
            eText = _ofbDecryption(binChunks, IVint, K)
        elif aMode == 'ofbbad':
            eText = _ofbDecryption(binChunks, IVint, [key] * 4)
        else:
            print('Invalid or unsupported Decryption Mode Entered')
            return

        # Convert this to RGB tuples
        rgbTuples = _convertBinaryChunksToRgbTuples(eText)

        # Write our output
        _saveTupleListAsImage(rgbTuples, imSize, saveLoc)

    elif bcType == 'aes':
        print('Performing AES Decryption...')
        # Convert key and IV into something useable
        key = hashlib.sha256(key.encode('utf-8')).digest()
        if aMode.lower() != 'ecb' and isinstance(IV, str):
            iv = hashlib.sha256(IV.encode('utf-8')).digest()[0:16]
        else:
            iv = IV

        # Determine the decryption mode
        aMode = aMode.lower()
        if aMode == 'cbc':
            cipher = AES.new(key, AES.MODE_CBC, iv)
        elif aMode == 'ctr':
            cipher = AES.new(key, AES.MODE_CTR, nonce=iv[0:8])
        elif aMode == 'ecb':
            cipher = AES.new(key, AES.MODE_ECB)
        elif aMode == 'ofb':
            cipher = AES.new(key, AES.MODE_OFB, iv)
        elif aMode == 'gcm':
            cipher = AES.new(key, AES.MODE_GCM, nonce=iv)
        else:
            print('Invalid Decryption Mode Entered')
            return

        # Decrypt the data
        im = Image.open(imageLoc)
        imSize = im.size
        tData = im.tobytes()

        # Handle padding
        if padIn != -1:
            tData += padIn

        # Decrypt
        imageBytesOut = cipher.decrypt(tData)

        # Save the Data
        t = Image.frombytes(im.mode, imSize, imageBytesOut)
        t.save(saveLoc)

        print('AES Decryption Complete!')

    else:
        print('Invalid BC type entered (Feistel or AES)')
        return

    # Determine if the image is the same as the one that was sent
    if imHash != -1:
        im = Image.open(saveLoc)
        tHash = hashlib.sha256(im.tobytes()).hexdigest()
        if tHash == imHash:
            print('Image was correctly decrypted!')
        else:
            print('Image was not correctly decrypted =(')
