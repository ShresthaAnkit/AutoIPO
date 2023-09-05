# AutoIPO
This is a script that helps to automatically fill up all the Ordinary IPO shares in MeroShare. It goes through all the registered users stored locally in a pickle file and fills up the IPO based on all the 
information provided including the number of Kittas.

### Initial setup
You need to download the chromedriver for your browser and put it in a folder called "chromedriver" just outside the project directory.

### Registration
To register a new user currently, make a new file and call the functions given in the credential_manager class with the appropriate parameters and the user will be registered.

### Running
To run the script just run the scrap.py file and it will do the trick.

### Notes
1. This is not a foolproof script and there are many cases where the script gets stuck on something unexpected. But for the most part it does the job perfectly.
2. It only works for Ordinary share, IPO.
