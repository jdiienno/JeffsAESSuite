****************
* Requirements *
****************
Python 3.9.1
Pillow 8.1.0

**************
* How to Use *
**************
Download jeffsAESSuite.py and drop it into your project in a place where you can import it. I would suggest putting it in the root file, as that's the easiest method. 

In your script import jeffsAESSuite. Now you can use the AES Suite.

Please only use .png Images. I have only tested this with .png files, so I am unsure if it will work with other types of image files.

Also note that these do take a while (5-10 minutes per image). 


**********************
* Available Commands *
**********************
encrypt(inputLocation, outputLocation, mode, key, iv)
decrypt(inputLocation, outputLocation, mode, key, iv)

NOTE: All input arguments are strings
NOTE: There is no output. These commands will take find the image, parse the data, perform the specified mode of encryption/decryption, and save the new image in the defined output location
NOTE: These commands will both print to the Python Console. The output is in the form "[Completed Chunks] of [Total Chunks]". Prints every 100 chunks completed. There is no way to disable this in the published file.


*************
* Arguments *
*************
inputLocation (string): Location of the image being encrypted or decrypted

outputLocation(string): Location where the encrypted or decrypted image will be saved

mode (string): AES mode of operation. Use the abreviation of the mode as the argument (i.e. 'ECB' for Electronic Code Book)
	Available Modes:
	Electronic Code Book (ECB)
	Cipher Block Chaining (CBC)
	Output Feedback Mode (OFB)
	Counter Mode (CTR)

key (string): Key used for block cipher encryption/decryption

iv (string): Initialization Vector (or nonce in the case of CTR mode).


***********
* Example *
***********
NOTE: The mechanics are the same for encryption or decryption, the only difference will be the function used

Input file Location: exampleImage.png
Output file location: exampleOutput.png
Mode: ECB
key: exampleKey
iv: exampleIV

To encrpyt 'exampleImage.png' and save the encrypted image as 'exampleOutput.png' use:
Import jeffsAESSuite
jeffsAESSuite.encrypt('exampleImage.png', 'exampleOutput.png', 'ECB', 'exampleKey', 'exampleIV')

To decrypt'exampleImage.png' and save the decrypted image as 'exampleOutput.png' use: 
jeffsAESSuite.decrypt('exampleImage.png', 'exampleOutput.png', 'ECB', 'exampleKey', 'exampleIV')


***********
* Contact *
***********
Contact me if you need help
Email: jdiienno@udel.edu
Slack: Jeff DiIenno (Member ID: U01NB4R395J)
