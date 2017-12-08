# Where Is Bill?

Bills don't turn laws in one day!

###### Project Overview: 
Bills do not turn laws in one day! Where is Bill? is a python program designed to track and find more information about the current status of a bill. The complex lawmaking process often makes it complicated for constituents to remain informed on latest proposed legislation. Has the bill been voted by Congress? Is it sitting in a Senate Committee? Did the President of the United States veto it? Using a simple keywords search, Where is Bill? will return the most recent bill information such as its identification number, where it currently stands on the hill and offer constituents some suggestions to voice their opinion. 

###### Program Interaction:
The user will start at a menu and have to press a key to continue. It will prompt him to enter one or more keywords to start the legislation search. The program will return a list of the most recent 20 matching bills. Then, the user will have the opportunity to enter the bill identification number to track its current location. Finally, a prompt will ask the user to provide his address to find contact information about his federal elected representatives. Our goal is to give them a voice in the legislation process. 

###### Algorithm:
To code this program we will need to import some libraries (json, requests, pandas, numpy) and code at least four functions. 

The first function we have to define is getrecentbill(keywords). It will connect to ProPublica Congress API and return matched bills in a data frame using pandas, Python Data Analysis Library. We will use lists, dictionaries and iteration to index and sort the json data to fit our needs. 

Then, the function track(bill_id) will connect back to the ProPublica Congress API to find more about the bill latest major action and deduce its current location. 

The third function will be getelectiverep(address). It will use SmartyStreets API to return data about the user district and work closely with legislators-current.csv to match their elected representative. This csv file was found online on the @unitedstates/congress-legislator Github and contains a lot of information about the current members of Congress. 

Finally, using the getcontact(state, district) function the user will be provided with his elected representative contact information. 
The main program will be used to generate the menu, the indefinite loop, the try and except, error handling and calls to functions. 
