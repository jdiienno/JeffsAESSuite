****************
* Requirements *
****************
Python Version:
- Python 3.9.1

Python Packages:
- Pillow 8.1.0
- pycryptodome 3.10.1
- random (the one included with Python)
- hashlib (the one included with Python)

This "package" was developed and debugged using Pycharm Community Edition 2020.3.3, so I can only guarantee it will work in there, but it should work regardless of environment so long as the required Python version and packages are used.

**************
* How to Use *
**************
Download jeffsAESSuite.py and drop it into your project in a place where you can import it. I would suggest putting it in the root file, as that's the easiest method. 

In your script import jeffsAESSuite. Now you can use the AES Suite.

For University of Delaware class 21S-CPEG672-610 Assignment 2, the encrypted images are saved in the "AES Encrypted Images" and "Feistel Encrypted Images" folder at github.com/jdiienno/JeffsAESSuite. The passwords are saved in the file "passwords.txt" also at github.com/jdiienno/JeffsAESSuite. The Block Cipher type is in the main folder name (AES or Feistel). The Block Cipher mode is stated in the encrypted file name (i.e. ECB mode was used to create the encrypted image saved as 'ecbEncrypt.png')

Please only use .png Images. I have only tested this with .png files, so I am unsure if it will work with other types of image files. On this note, only .pngs of type 'L' and 'RGB' are supported for encryption, and only .pngs of type 'RGB' are supported for decryption.

Also note that when using the Feistel Block Cipher these do take a while (5-10 minutes per image).


**********************
* Available Commands *
**********************
encrypt(imageLoc, saveLoc, aMode, key, IV, bcType)
decrypt(imageLoc, saveLoc, aMode, key, IV, bcType, imHash)

NOTE: All input arguments are strings
NOTE: There is no output. These commands will take find the image, parse the data, perform the specified mode of encryption/decryption, and save the new image in the defined output location
NOTE: These commands will both print to the Python Console. The output is in the form "[Completed Chunks] of [Total Chunks]". Prints every 100 chunks completed. There is no way to disable this in the published file.


*************
* Arguments *
*************
inputLocation (string): Location of the image being encrypted or decrypted.

outputLocation(string): Location where the encrypted or decrypted image will be saved. Image base save folder must already exist, this Suite will not create new folders to save in.

aMode (string) (optional): AES mode of operation. Use the abreviation of the mode as the argument (i.e. 'ECB' for Electronic Code Book). It is not case sensitve, so an argument of 'ecb' will work. AES is selected by default
	Available Modes:
	Electronic Code Book (ECB)
	Cipher Block Chaining (CBC)
	Output Feedback Mode (OFB)
	Counter Mode (CTR)
	Galois Counter Mode (GCM) (Only supported with AES)

key (string) (optional for encryption): Key used for block cipher encryption/decryption. If no key is defined for encryption a key will be randomnly generated.

iv (string) (optional for encryption.: Initialization Vector (or nonce in the case of CTR mode). This will be converted to a byte string of length 16 in CBC, OFB, and GCM modes, and converted to a byte string of length 8 in the CTR mode. Also converted to a byte string of length 16 for EBC but it is not actually used. If no IV is defined for encryption an IV will be randomly generated.

bcType (string) (optional): The cipher block type, either AES or Feistel. If no input then it'll use AES

imHash (string of hex values) (optional) (Decryption only): A string hex that is the sha256 hash of the encrypted image. If defined the decryption method will check if the decrypted image matches the hash.

**********************
* Encryption Outputs *
**********************
key (string): The key used for the encryption

IV (string): The IV used for the encryption

imHash (string of hex values): sha256 hash of the original image

cipher (Crypto.Cipher.mode): The cipher object used to perform the encryption


**********************
* Decryption Outputs *
**********************
None.

Note: If an imHash is used as an input then the decryption method will check the decrypted image hash with the the imHash input and print a message saying if they are the same or not


***********
* Example *
***********
NOTE: The mechanics are the same for encryption or decryption, the only difference will be the function used

Input file Location: exampleImage.png (located in the root)
Output file location: exampleOutput.png (located in the root)
Mode: ECB
key: exampleKey
iv: exampleIV
cipherBlockType = AES
imHash = 2cd645b618f89db964d4927c546c25b55622eeb7d1332ca79f8960e628ba9d60 

To encrpyt use:
import jeffsAESSuite
jeffsAESSuite.encrypt('exampleImage.png', 'exampleOutput.png', 'ECB', 'exampleKey', 'exampleIV', 'aes')

To decrypt use: 
import jeffsAESSuite
jeffsAESSuite.decrypt('exampleImage.png', 'exampleOutput.png', 'ECB', 'exampleKey', 'exampleIV', 'aes', '2cd645b618f89db964d4927c546c25b55622eeb7d1332ca79f8960e628ba9d60')


***********
* Contact *
***********
Contact me if you need help
Email: jdiienno@udel.edu
Slack: Jeff DiIenno (Member ID: U01NB4R395J)
