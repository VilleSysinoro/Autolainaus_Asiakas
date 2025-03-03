"""A module to check the validity of Finnish Social Security Number (SSN). Contains methods to calculate age and determine the gender of person
"""
# LUOKKA HENKILÖTUNNUSTEN KÄSITTELYYN
# ===================================

# KIRJASTOT JA MOODUULIT
# ----------------------

# Kirjasto päivämäärälaskentaa varten
import datetime

# LUOKAT
# ------

# Henkilötunuksen käsittely


class NationalSSN:
    """Various methods to access and validate Finnish Social Security Number propersties
    """

    def __init__(self, ssn: str) -> None:
        """Generates a Finnish SSN object

        Args:
            ssn (str): 11 character SSN to process
        """
        self.ssn = ssn

        # Laskemalla selviävät ominaisuudet
        self.dateOfBirth = ''
        self.number = 0
        self.gender = ''
        self.correctLenght = False
        self.errorMessage = 'OK'

        # Sanakirjat vuosisatakoodeille ja varmisteille
        self.centuryCodes = {
            '+': '1800',
            '-': '1900',
            'A': '2000'
        }

        self.moduloSymbols = {
            0: '0',
            1: '1',
            2: '2',
            3: '3',
            4: '4',
            5: '5',
            6: '6',
            7: '7',
            8: '8',
            9: '9',
            10: 'A',
            11: 'B',
            12: 'C',
            13: 'D',
            14: 'E',
            15: 'F',
            16: 'H',
            17: 'J',
            18: 'K',
            19: 'L',
            20: 'M',
            21: 'N',
            22: 'P',
            23: 'R',
            24: 'S',
            25: 'T',
            26: 'U',
            27: 'V',
            28: 'W',
            29: 'X',
            30: 'Y'
        }
    # Luokan metodit eri osien laskentaan ja järkevyystarkistuksiin

    # Tarkistetaan, että HeTu:n pituus on 11 merkkiä
    def checkSsnLengthOk(self) -> bool:
        """Checks correct length of the SSN

        Returns:
            bool: True if 11 chr othervise False
        """
        ssnLength = len(self.ssn)
        if ssnLength != 11:

            # Generoidaan virhetilanne, jos liian lyhyt tai liian pitkä
            if ssnLength > 11:
                self.errorMessage = 'Henkilötunnuksessa ylimääräisiä merkkejä'
                raise ValueError(self.errorMessage)
            else:
                self.errorMessage = 'Henkilötunnuksesta puuttuu merkkejä'
                raise ValueError(self.errorMessage)
            
        else:
            return True

    # Pilkotaan henkilötunnus osiin
    def splitSsn(self) -> dict:
        """Splits the SSN to functional parts ie. birthdate, century, number and the checksum

        Returns:
            dict: parts as strings
        """
        # Tehdään pilkkominen vain jos pituus on oikein
        if self.checkSsnLengthOk():  # Jos True pilkotaan, huom. self.metodinNimi
            dayPart = self.ssn[0:2]
            monthPart = self.ssn[2:4]
            yearPart = self.ssn[4:6]
            centuryPart = self.ssn[6]
            birthNumberPart = self.ssn[7:10]
            checksumPart = self.ssn[10]
            return {'days': dayPart,
                    'months': monthPart,
                    'years': yearPart,
                    'century': centuryPart,
                    'number':  birthNumberPart,
                    'checksum': checksumPart
                    }
        # Else haaran tarkoitus on vain estää PyLance-virhe. Ei palauta oikeasti mitään, vaan antaa virheilmoituksen, jos HeTu väärän mittainen
        else:
            self.errorMessage = 'Virhe henkilötunnuksessa'
            return {'status': 'error'}

    

    # Selvitetään varmistussumman avulla onko HeTu syötetty oikein
    def isValidSsn(self) -> bool:
        """Recalculates the checksum of the SSN and verifies it is the same in the given SSN

        Returns:
            bool: True if SSN is valid, False otherwise
        """
        
        # Otetaan talteen mahdollinen virheilmoitus
        try:
            self.correctLenght = self.checkSsnLengthOk()
        except Exception as e:
            self.errorMessage = str(e)

        if self.correctLenght == True:
            parts = self.splitSsn()
            moduloString = parts['days'] + parts['months'] + \
                parts['years'] + parts['number']
            moduloNumeric = int(moduloString)
            checkSumCalculated = moduloNumeric % 31
            checkSumCalculatedSymbol = self.moduloSymbols[checkSumCalculated]
            if checkSumCalculatedSymbol == parts['checksum']:
                return True
            else:
                self.errorMessage = 'Syötetty henkilötunnus ei vastaa varmistussummaa'
                return False
        else:
            return False
   
    # Muutetaan synytmäaikaosa ja vuosisata päivämääräksi
    def getDateOfBirth(self) -> None:
        """Sets the value of dateOfBirth property for object
        """
        
        if self.isValidSsn():
            isoDate = '1799-12-31'
            parts = self.splitSsn()
            centurySymbol = parts['century']

            try:
                century = self.centuryCodes[centurySymbol]
            except:
                raise ValueError('Vuosisatamerkki virheellinen')
            
            isoDate = century[0:2] + parts['years'] + \
                '-' + parts['months'] + '-' + parts['days']
            self.dateOfBirth = isoDate

    # Lasketaan ikä nyt täysinä vuosina
    def calculateAge(self) -> int :
        """Calculates age in full years from SSN

        Returns:
            int: age in years
        """
        # Tarkistetaan ennen laskentaa, että henkilötunnus on oikein syötetty
        if self.isValidSsn():  # Tarkistaa onko hetu syötetty oikein
            self.getDateOfBirth()  # Kutsutaan metodia, joka asettaa dateOfBirth ominaisuuden arvon

            # Muutetaan olion syntymäaikaominaisuuteen tallennettu ISO-päivämäärä Pyhton-päivämääräksi
            pythonBirthDate = datetime.date.fromisoformat(self.dateOfBirth)

            # Haetaan nykyinen päivämäärä (ja kellonaika)
            pythonToday = datetime.datetime.now()

            # Lasketaan päivämäärien ero täysinä vuosina
            ageInYears = pythonToday.year - pythonBirthDate.year

            # Palautetaan ikä vuosina
            return ageInYears
        else:
            return 0
        
    # Metodi sukupuolen selvittämiseen sekä number- ja gender-ominaisuuden asettamiseen
    def getGender(self) -> None:
        """Sets the gender property of the object (in finnish)
        """
        # Tarkistetaan ensin, onko SSN oikein syötetty
        if self.isValidSsn():

            # Otetaan merkkijonosta järjestysnumero hyödyntämällä splitSSN-metodia
            parts = self.splitSsn()

            # Muutetaan luvuksi ja tallennetaan se ominaisuuden arvoksi
            number = int(parts['number'])
            self.number = number

            # Selvitetään onko parillinen (tyttö) vai pariton (poika)
            if number % 2 == 0:
                self.gender = 'Nainen'
            else:
                self.gender = 'Mies'

    
# MAIN KOKEILUJA VARTEN (Poista, kun ei enää tarvita)
# ===================================================


if __name__ == "__main__":
    try:
        hetu1 = NationalSSN('130728x478N')
        hetu1.checkSsnLengthOk()
        hetu1.getDateOfBirth()
        print('On oikean pituinen:', hetu1.checkSsnLengthOk())
        print('Henkilötunnus on oikein muodostettu', hetu1.isValidSsn())
        print('HeTun osat ovat: ', hetu1.splitSsn())
        print('Syntymäaikaosa ISO-muodossa on ', hetu1.dateOfBirth)
    except Exception as e:
        print('Tapahtui virhe:', e)
    

    
   