#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Class in Python 2.7 for simultaneous reading of RFID tags through two modules
RFID-RC522 using the SPI interface of Raspberry Pi through the MFRC522 driver.

Credits and License: Created by Mario Gómez, adapted by Erivando Sena(2016)

 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License.
"""

import signal
from module.MFRC522 import MFRC522
from module.pinos import PinoControle
import time

##from MFRC522 import MFRC522
##from pinos import PinoControle

__author__ = "Erivando Sena Ramos (Adaptations)"
__copyright__ = "Mario Gómez"
__email__ = "erivandoramos@bol.com.br"
__status__ = "Prototype"

class Nfc522(object):
    
    pc = PinoControle()
    MIFAREReader = None
    RST1 = 22 #GPIO
    RST2 = 22 #GPIO
    SPI_DEV0 = '/dev/spidev0.0'
    SPI_DEV1 = '/dev/spidev0.1'
    
    def obtem_nfc_rfid(self, autenticacao=False):
        try:
            self.MIFAREReader = MFRC522(self.RST1, self.SPI_DEV0)
##            while True:
            (status, TagType) = self.MIFAREReader.MFRC522_Request(self.MIFAREReader.PICC_REQIDL)
            (status, uid) = self.MIFAREReader.MFRC522_Anticoll()
            
            if status == self.MIFAREReader.MI_OK:
##                print "Ganesh 1"
                gid1 =  self.obtem_tag(self.MIFAREReader, status, uid, autenticacao)
##                    return gg
##                print "GID1:" + str(gg)
            else:
                self.pc.atualiza(self.RST1, self.pc.baixo())
##                print "GID1: No"

                gid1 = 0
            
        except Exception as e:
            print e
            
        try:    
            self.MIFAREReader = MFRC522(self.RST2, self.SPI_DEV1)
            
            
            #while True:
            (status, TagType) = self.MIFAREReader.MFRC522_Request(self.MIFAREReader.PICC_REQIDL)
            (status, uid) = self.MIFAREReader.MFRC522_Anticoll()
                
            if status == self.MIFAREReader.MI_OK:
                
                gid2= self.obtem_tag(self.MIFAREReader, status, uid, autenticacao)
##                print "GID2:" + str(ggg)
            else:
                self.pc.atualiza(self.RST2, self.pc.baixo())
##                print "GID2: No"
                gid2=0
##                    return None
            

        except Exception as e:
            print e
        #finally:
            #self.MIFAREReader.fecha_spi()

        return gid1,gid2
			
    def obtem_tag(self, MIFAREReader, status, uid, autenticacao):
        try:
			if autenticacao:
				# Chave padrão para a autenticação
				key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
				MIFAREReader.MFRC522_SelectTag(uid)
				status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 8, key, uid)
				if status == MIFAREReader.MI_OK:
					MIFAREReader.MFRC522_Read(8)
					MIFAREReader.MFRC522_StopCrypto1()
				else:
					print "Erro na autenticação!"
					return None
			tag_hexa = ''.join([str(hex(x)[2:4]).zfill(2) for x in uid[:-1][::-1]]) #Returns in hexadecimal
			return int(tag_hexa.upper(), 16) #Returns in decimal
        except Exception as e:
            print e
			
# Capture SIGINT for cleanup when the script is aborted
def end_read(signal,frame):
    global continue_reading
    print "Ctrl+C captured, ending read."
    continue_reading = False
##    GPIO.cleanup()

# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

nfc = Nfc522()

continue_reading = True
print "\nWaiting for Tag\n---------------"

while continue_reading:
    print_opt = 0
    
    gid1,gid2 = nfc.obtem_nfc_rfid()
    ##print "G Read TAG Number: " +str(id)

    if not gid1==0:
        print "ID of first Tag is:" + str(gid1)
        print_opt = 1
    if not gid2==0:
        print "ID of SecondTag is:" + str(gid2)
        print_opt = 1

    if print_opt==1:
        print "\nWaiting for Tag\n---------------"
    time.sleep(1)


