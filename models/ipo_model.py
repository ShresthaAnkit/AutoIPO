class IPO():
    def __init__(self,name,subGroup,shareType,shareGroup):
        self.name = name
        self.subGroup = subGroup
        self.shareType = shareType
        self.shareGroup = shareGroup
        
    def __str__(self):
        return "Name: "+self.name+ "\nSubGroup: "+self.subGroup+"\nShareType: "+self.shareType+"\nShareGroup: "+self.shareGroup