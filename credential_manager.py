import os
import pickle
from models.user_model import User

PICKLE_FILE = "Project\creds.pkl"


class Database():

    def storeUser(self,newUser):
        try:
            if newUser.name == user.name:
                return "User already exists" 
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
            with open(PICKLE_FILE, 'wb') as f:
                for user in usersCopy:
                    pickle.dump(user, f)
    
    def deleteUser(self, name):
        users = self.getUsers()
        usersCopy = []        
        for user in users:
            if user.name == name:
                # Skip the user you want to delete                
                continue
            usersCopy.append(user)

        # Save the updated user list
        with open(PICKLE_FILE, 'wb') as f:
            for user in usersCopy:
                pickle.dump(user, f)

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



