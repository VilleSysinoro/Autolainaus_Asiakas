# MODUULI VIIVAKOODIEN TUOTTAMISEEN
# =================================

# KIRJASTOT
# ---------

# ASETUKSET
# ---------

# FUNKTIOT
# --------

def barCodeValue(character: str) -> int:
    """Calculates a value of character used in Code128B barcode generation

    Args:
        character (str): a single character to convert

    Returns:
        int: Code128B value for calcultaing the checksum
    """
    asciiValue = ord(character)
    code128BValue = asciiValue - 32
    return code128BValue

def calculateCode128BCheksum(text: str) -> int:
    """Calculates a checksum for a given string

    Args:
        text (str): text string to use in a barcode

    Returns:
        int: Modulo 103 checksum of weighted values
    """
    text = text.strip()
    numberOfLetters = len(text)
    weightedSum = 0
    for number in range(numberOfLetters):
        letter = text[number]
        code128BValue = barCodeValue(letter)
        weightedValue = code128BValue * (number + 1)
        weightedSum = weightedSum + weightedValue
    weightedSum = weightedSum + 104
    code128BChecksum = weightedSum % 103
    return code128BChecksum


def createCode128B(text: str) -> str:
    """Creates a complete code128B barcode to be printed using Libre Code128 font

    Args:
        text (str): The text for a barcode without checksum

    Returns:
        str: String containing start, barcode, checksum and stop symbols
    """
    code128BarcodeString = ''
    startChar = chr(204)
    stopChar = chr(206)
    checkSum = calculateCode128BCheksum(text)
    checkSumSymbol = chr(checkSum + 32)
    code128BarcodeString = startChar + text + checkSumSymbol + stopChar
    return code128BarcodeString

# LUOKKA VIIVAKOODEILLE
# =====================

class Code128B():
    """Generates Code128B barcodes. Supports variants common, uncommon and Barcodesoft"""
    def __init__(self, text: str, variant: str = 'Common') -> None:
        """Checks if text contains only valid characters for Code128B barcode

        Args:
            text (str): A text string to be converted into a barcode
            variant (str, optional): Variant of code128. Valid values: Common, Uncommon and BarcodeSoft. Defaults to 'Common'.
        """
        self.text = text
        self.variant = variant
        self.validRangeAll = range(33,126)
        self.validRangeCommon = range(195,202)
        self.validRangeUncommon = range(200,207)
        self.validRangeBarcodeSoft = range(240,247)
        self.commonSpecialChar = (32, 194, 207)
        self.uncommonSpecialChar = 212
        self.barcodeSoftSpecialChar = 252
        

    def checkValidityOfText(self) -> bool | None:
        textLength = len(self.text)
        isValid = False
        if self.variant == 'Common':
            for index in range(textLength):
                character = self.text[index]
                characterValue = ord(character)
                if characterValue in self.validRangeAll or characterValue in self.validRangeCommon or characterValue in self.commonSpecialChar:
                    isValid = True
                else:
                    errorMessage = 'Text string contains invalid characters ' + '(' + character + ')'
                    raise ValueError(errorMessage)
                    
        elif self.variant == 'Uncommon':
            for index in range(textLength):
                character = self.text[index]
                characterValue = ord(character)
                if characterValue in self.validRangeAll or characterValue in self.validRangeUncommon or characterValue == self.uncommonSpecialChar:
                    isValid = True
                else:
                    errorMessage = 'Text string contains invalid characters ' + '(' + character + ')'
                    raise ValueError(errorMessage)
                
        elif self.variant == 'BarcodeSoft':
            for index in range(textLength):
                character = self.text[index]
                characterValue = ord(character)
                if characterValue in self.validRangeAll or characterValue in self.validRangeBarcodeSoft or characterValue == self.barcodeSoftSpecialChar:
                    isValid = True
                else:
                    errorMessage = 'Text string contains invalid characters ' + '(' + character + ')'
                    raise ValueError(errorMessage)
                
        else:
            errorMessage = 'Invalid variant ' + '(' + self.variant + '): Common, Uncommon and BarcodeSoft supported'
            raise ValueError(errorMessage)
            
        return isValid
    
    # Metodi, joka tuottaa viivakoodin sisällön
    def buildBarcode(self) -> str:
        """Returns a string presentation of the barcode

        Returns:
            str: barcode with start symbol, text, checksum symbol and stop symbol
        """
        rawText = self.text
        variant = self.variant
        startValues = {'Common': 204, 'Uncommon': 209, 'BarcodeSoft': 249}
        stopValues = {'Common': 206, 'Uncommon': 211, 'BarcodeSoft': 251}
        subtractValues = {'Common': 100, 'Uncommon': 105, 'BarcodeSoft': 145}

        # Katsotaan onko tekstissä pelkästään sallittuja merkkejä
        if self.checkValidityOfText() == True:
            rawTextLenght = len(rawText)
            weightedSum = 0

            # Käydään merkkijono silmukassa läpi ja lasketaan varmistussuman arvot
            for index in range(rawTextLenght):
                character = rawText[index]
                characterValue = ord(character)

                # Normaalit merkit 32 - 126, alle 32 ei tarvitse enää huomioida
                if characterValue < 127:
                    value = characterValue -32 # Tätä arvoa käytetään varmistussumman laskennassa

                # Erikoismerkit, joiden arvo on 0    
                elif characterValue in (194, 207, 212, 252):
                    value = 0
                
                # Varianttien erikoismerkit, rajat tarkisettu jo aiemmin 
                else:
                    value = characterValue - subtractValues[variant]
                        
                
                # Kirjaimen painotetun arvon lisääminen, huom indeksi alkaa 0:sta kertoimet 1:stä       
                weightedSum =  weightedSum + (index +1)  * value
            
            # Alkumerkin sisältäva painotettu summa
            weightedSum = weightedSum + startValues[variant] - subtractValues[variant]

            # Lopullinen varmistussumma jakojäännös 103:lla jaettaessa
            checksum = weightedSum % 103

            # Generoidaan lopullinen viivakoodi alkumerkki + raakateksti + varmistussumma + loppumerkki
            startChar = chr(startValues[variant])
            stopChar = chr(stopValues[variant])
            checksumChar = chr(checksum + 32)
            barcode = startChar + rawText + checksumChar + stopChar
        
        return barcode
    

if __name__ == "__main__":
    testi = Code128B('AM-15')
    try:
        tulos = testi.checkValidityOfText()
        print(testi.text, 'on kelvollinen viivakoodiksi', tulos)
        viivakkoodi = testi.buildBarcode()
        print('Viivakoodin sisältö on', viivakkoodi)
    except Exception as e:
        print('Tapahtui virhe:', testi.text, e)
    