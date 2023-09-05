import os
import pickle
from models.user_model import User

PICKLE_FILE = "Project\creds.pkl"

class Database():

    def storeUser(self,newUser):
        try:
            with open(PICKLE_FILE,'ab') as f:
                pickle.dump(newUser,f)
        except Exception:
            print("Error while Storing")
    
    def registerUser(self,newUser): 
        users = self.getUsers()

        for user in users:
            if newUser.name == user.name:
                return "User already exists" 
            
        self.storeUser(newUser)
                   
        
        
    def updateUser(self,newUser):
        users = self.getUsers()
        usersCopy = []
        update = False
        for user in users:
            if newUser.name == user.name:
                usersCopy.append(newUser)
                update = True
            else: 
                usersCopy.append(user)           
        if update:
            for user in usersCopy:
                self.storeUser(user)
        

    def getUsers(self):                
        data = []     
        try:
            with open(PICKLE_FILE,"rb") as f:
                while True:
                    try:
                        data.append(pickle.load(f))
                    except EOFError:
                        break
                f.close()
        except Exception:
            print("Error while retrieving User")
        return data





