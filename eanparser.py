class EanParser:
    def __init__(self, eanstring):
        if len(eanstring) != 13 and len(eanstring) != 24:
            raise ValueError('Length of EAN is not 13 or 23')
        if not eanstring.isdigit():
            raise ValueError('EAN is not a numeric string')
        self.ean = eanstring

    def isownproduct(self):
        if self.ean[:2] == '84' and len(self.ean) == 13:
            return True
        return False

    def isvariableweightproduct(self):
        if self.ean[:2] == '23' and len(self.ean) == 13:
            return True
        return False

    def isbulkproduct(self):
        if self.ean[:2] == '23' and len(self.ean) == 24:
            return True
        return False

    def getmcode(self):
        if self.isownproduct():
            return int(self.ean[7:12])
        elif self.isvariableweightproduct():
            return int(self.ean[2:7])
        elif self.isbulkproduct():
            return int(self.ean[3:8])
        else:
            raise ValueError('EAN does not belong to: own, variable weight, or bulk')

    def getprice(self):
        if self.isvariableweightproduct():
            return int(self.ean[7:12])/100
        elif self.isbulkproduct():
            return int(self.ean[18:23])/100
        else:
            raise ValueError('EAN does not belong to variable weight or bulk prod')

    def getpvp(self):
        if self.isbulkproduct():
            return int(self.ean[13:18])/100
        else:
            raise ValueError('EAN is not bulk prod')

    def getweight(self):
        if self.isbulkproduct():
            return int(self.ean[8:13])/100
        else:
            raise ValueError('EAN is not bulk prod')
