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

Please only use .png Images. I have only tested this with .png files, so I am unsure if it will work with other types of image files.

Also note that when using the Feistel Block Cipher these do take a while (5-10 minutes per image).


**********************
* Available Commands *
**********************
encrypt(inputLocation, outputLocation, mode, key, iv, cipherBlockType)
decrypt(inputLocation, outputLocation, mode, key, iv, cipherBlockType)

NOTE: All input arguments are strings
NOTE: There is no output. These commands will take find the image, parse the data, perform the specified mode of encryption/decryption, and save the new image in the defined output location
NOTE: These commands will both print to the Python Console. The output is in the form "[Completed Chunks] of [Total Chunks]". Prints every 100 chunks completed. There is no way to disable this in the published file.


*************
* Arguments *
*************
inputLocation (string): Location of the image being encrypted or decrypted.

outputLocation(string): Location where the encrypted or decrypted image will be saved. Image base save folder must already exist, this Suite will not create new folders to save in.

mode (string): AES mode of operation. Use the abreviation of the mode as the argument (i.e. 'ECB' for Electronic Code Book). It is not case sensitve, so an argument of 'ecb' will work.
	Available Modes:
	Electronic Code Book (ECB)
	Cipher Block Chaining (CBC)
	Output Feedback Mode (OFB)
	Counter Mode (CTR)

key (string): Key used for block cipher encryption/decryption

iv (string): Initialization Vector (or nonce in the case of CTR mode).

cipherBlockType (string): The cipher block type, either AES or Feistel. If no input then it'll use AES


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

To encrpyt use:
import jeffsAESSuite
jeffsAESSuite.encrypt('exampleImage.png', 'exampleOutput.png', 'ECB', 'exampleKey', 'exampleIV', 'aes')

To decrypt use: 
import jeffsAESSuite
jeffsAESSuite.decrypt('exampleImage.png', 'exampleOutput.png', 'ECB', 'exampleKey', 'exampleIV', 'aes')


***********
* Contact *
***********
Contact me if you need help
Email: jdiienno@udel.edu
Slack: Jeff DiIenno (Member ID: U01NB4R395J)
