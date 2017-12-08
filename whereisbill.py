# Definition of functions
#S.G

def getrecentbill(query): #Call to ProPublica API for bill information
    url = "https://api.propublica.org/congress/v1/bills/search.json"
    headers={ "X-API-Key": "OL9rTNU3pOCB5FkqOWJH7hMAdmCZLS3GJU5NpLuV" }
    params = {'query' : query}
    response = requests.get(url, headers=headers, params=params)
    bill = response.json()
    bill_data = []
    for i in bill['results'][0]['bills']:
        bills = {}
        bill_data.append(bills)
        bills['bill_id'] = i["bill_id"]
        bills['bill_title'] = i['title']        
    
    return bill_data

def getbillstatus(bill_id):  #call to ProPublica API for detailled information about selected bill  
    congress = bill_id.split("-",1)[1]
    bill_id = bill_id[0:4]
    url = "https://api.propublica.org/congress/v1/" + congress + "/bills/" + bill_id + ".json"
    headers={ "X-API-Key": "OL9rTNU3pOCB5FkqOWJH7hMAdmCZLS3GJU5NpLuV" }
    response = requests.get(url, headers=headers)
    bill_tracking_response = response.json()
    bill_data_tracking = []
    for i in bill_tracking_response['results']:
        bill_tracking = {}
        bill_data_tracking.append(bill_tracking)
        bill_tracking['bill'] = i["bill"]
        bill_tracking['bill_title'] = i['title'] 
        bill_tracking['short_title'] = i['short_title']
        bill_tracking['active'] = i['active']
        bill_tracking["last_vote"] = i['last_vote']
        bill_tracking["house_passage"] = i['house_passage']
        bill_tracking["senate_passage"] = i['senate_passage']
        bill_tracking['enacted'] = i['enacted']
        bill_tracking['vetoed'] = i['vetoed']
        bill_tracking['introduced_date'] = i['introduced_date']
        bill_tracking['latest_major_action'] = i['latest_major_action'] 
        bill_tracking['latest_major_action_date'] = i['latest_major_action_date']
        
    return bill_data_tracking

def getuseraddress(): #Create dictionnary with user address
    address = {}
    address['street'] = input("Please enter your street address (ex: 900 South Crouse Ave): ").replace(" ", "%20") + "&"
    address['city'] = input("Please enter your city (ex: Syracuse): ").replace(" ", "%20") + "&"
    address['state'] = input("Please enter your state code (ex: NY for New York): ").replace(" ","%20") + "&"
    address['zipcode'] = input("Please enter your zipcode (ex: 13244): ") + "&"

    return address

def getstateanddistrict(address): #Call to SmartyStreets API to return Congressional district                                                                                                                       
    url = "https://us-street.api.smartystreets.com/street-address?auth-id=a9ccb89b-f8d2-fbf7-a9e3-4151ad050599&auth-token=oZ762CRxtxJ6vPKfvOgt&candidates=10&street=" + address['street'] + "&city=" + address['city'] + "&state=" + address['state'] + "&zipcode=" + address['zipcode'] 
    response = requests.get(url)
    state_district_response = response.json()
    address_data = {}
    address_data['state_abbreviation'] = state_district_response[0]["components"]["state_abbreviation"]
    address_data['congressional_district'] = state_district_response[0]["metadata"]["congressional_district"]
    
    return address_data

def gethrrep(address_data): #Input state and congressional district to return elected HR representative
    legislator_hr = pd.read_csv('legislators-current.csv')
    legislator_hr_df = pd.DataFrame({ 'First Name' : legislator_hr['first_name'], 
                                 'Last Name' : legislator_hr['last_name'],
                                 'State': legislator_hr['state'],
                                 'District' : legislator_hr['district'],
                                 'Party': legislator_hr['party'],
                                 'Phone': legislator_hr['phone']
                               })
    legislator_hr_df = legislator_hr_df[['Last Name', 'First Name', 'State', 'District', 'Party', 'Phone']]
    legislator_hr_df = legislator_hr_df[(legislator_hr['state'] == address_data["state_abbreviation"]) & (legislator_hr['district'] == int(address_data["congressional_district"]))]
    legislator_hr_df = legislator_hr_df.reset_index()
    
    return legislator_hr_df

def getssenaterep(address): #Input state to return elected Senate representatives
    legislator_senate = pd.read_csv('legislators-current.csv')
    legislator_senate_df = pd.DataFrame({ 'First Name' : legislator_senate['first_name'], 
                                 'Last Name' : legislator_senate['last_name'],
                                 'State': legislator_senate['state'],
                                 'Party': legislator_senate['party'],
                                 'Phone': legislator_senate['phone']
                               })
    legislator_senate_df = legislator_senate_df[['Last Name', 'First Name', 'State', 'Party', 'Phone']]
    legislator_senate_df = legislator_senate_df[(legislator_senate['state'] == address["state"][:-1]) & (legislator_senate['type'] == 'sen')]
    legislator_senate_df = legislator_senate_df.reset_index()
    
    return legislator_senate_df

logo = '''
                                           .╓▄▄#▒▓▓▓▓▓▓▓▄▄.
                                 ,▄▄▒▓▓▀▀╙└           ╙▀▀▓▄
                         .╓▄▄▒▓▀▀╙╙                      └█Γ
                   ,▄▄▓▓▀▀╙└                              ╫▒
              .▄▒▓▀╜╙                 .╓▄▄▄,              ║▌
             ╢█╙                    ╓▒██▒▒╠╙▀▓            ╙█
           ╓▓▀         .▄▄#⌐             └╙▀▓▒            └█⌐
          #█`         ▒▀╙▄▒▓▀`               `             █Γ
        ╓▓▀      ╓▒▓▒▒▒#▀╙                                 █M
       ╔█╙   ╓#▓▀█░(█▀▀█⌐           ╓▄▓▓▓▄,                ╫▌
      ▒█▒▓▓▓██` .▓Ñ║█ ╔█∩          ║▀    └▀M               ║▌
     `▀▀╙.#▓╙   ╙╙ ╙ÿ▓▀║▓ ╔▓▓▀▀▓▄ (█⌐ ╓,  │█               ║▌
        ╓▓▀          #▓▀└╫▌   ,╓║█▓▀▀▓██▓╓▓▀               ║▌
       #█"         .╫▌   ║▌  ║███╙    ██▀╜                 ║▌
     .▓▀         ╔▓▀╙     ▀▓▄╓║█∩     ▀∩  ,                ║▌
    ╓▓Ñ        ╓▓▀█▄        └╙╙█▄       ┌▓Ñ                ╫▌
   ╓█╙        #█` └█▄       .   ▀▀▀▀    ╫▌                 ▓M
   ▓▌          ▀▓▄ └█▄      ╙▀▓▄,       ╫▌                (█∩
   └▀▓,          ▀▓▄╙█M        └▀M      ║█▓▄              ▐█
     └▀▓▄          ╙▓▓▓         │█     ╓▓∩ ╙╙ .╓▄▄▄▄▄▄▄▄╓,╫▌
        ▀▓▄,         ╙█M       ╓▓▀▀▓▄#▓▀  .▄▓▓█▒▒▒▒▒▒▒▒▒▒▀█▓▄,
          ╙▀▓▄        ╙█,     ╙╜        ╓▒▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒█▓▄
             ▀▓▄,      ║▌             .▒█▒▒▒▒▒▒▒▒▒▒▒▓▓▓▓▓▓▓▓▀▀▀▀▓
               ╙▀▓▄     █▄    .,▄▄▒▓▓▓██▓▓▓▀▀▀▀            ▄▄   └█
                  ╙▓▒,  └▀▄▄▓▓▓▒▒▒▒▒▒█▀   ▄▄▄▄▄  ▓▓ ║█     ██    └█
                    └▀▓▒▓▓▒▒▒▒▒▒▓▓▓▀█▌    █▌  █   █ ▐█▌    ██     ║▌
                       █▓▒▒▓▓▀╜└..╓▄╫▌    ██▓▓█   █▌ ██    ║█     ▐▌
                      (██▀╙╓▄#▓▓▀▀▀Ñ║▌    ██  ▐█▌ █▌ ██▓▒▓▓▐██▓█▀ ║▌
                      ▐█▄▓▓▀ÑÑÑ╠╠ÑÑ▒▒█M    █▓▀▀▀  ▀▀    ▄▄▄▄▄▄▄  ▒█
                      ╫█ÑÑÑ▒▒▓▓▀▀╙╙└`╙▓⌂.╓▄▄▄_▓▓▓▓▀▀▀▀▀▀▀║ÑÑÑÑÑÑ║▓▀
                     (█▓▓▀╙└          └██▒ÑÑÑÑ╠╠╠╠╠╠╠╠╠╠╠╠ÑÑÑ╠Ñ▒█▀
                     ║█                 ╙▓▒╡╠Ñ╠Ñ╠╠╠╠╠╠╠╠╠╠╠╠║▒▓▀▒▓,
                    ╔█∩                   └▀▓▓▒ÑÑÑ╠╠╠╠╠Ñ▒▒▓██ÑÑ╠Ñ║█▄
                   .█Ñ                        └╙▀█▓▓▓▓█▀└   ▀▒╠ÑÑ╠║█▄
                   ╫▌                           │█▒▒▒╢▒▓     █▒╠╠╠╠╠█▓,
                  #█        .,╓▄▄▄##▓▓▓▓▓▓▓▓▀▀▀▓▓█▒▒▒▒╢█▒    └█▒╠╠╠ÑÑ║▓▒,
                 ╓█∩ .▄▄▓▓▀▀╙╙└     ▐█   ╓█    ║Ñ║█▒▒▒▒╢█▒    `█▒╠╠╠╠╠Ñ║▀▓▄
                 ╫▌#▓▀└            (▓∩   ║▌    ║▓▓█▒▒▒▒▒╢█▄▒▓▓▄▄█▒ÑÑ╠Ñ╠╠╠Ñ▀▓▓▄
                 └▀▓▄▄▄▄╓▄▄▄▄▄▄▄#▒▓█Ñ    ╫▌    ║▌ ║█▒▒▒▒▒▒█▀  └╙▀▀▀▓▓▓▓▓▓▓▓▀▀▀"
                     └╙╙╙╙╙╙└'    ╫▌     █Γ    ║▌  █▓▒▒▒▒█▀
                                 (█`    (█⌐    ║▌  └█▒▒▒█╙
                                 ║▌     ⌠█     ╫Ñ   ╚█▓█C
                                (█∩     ║▌     ▓Γ    ╚▀`
                           .,▄▄▄▓▀      ║▌   .▄█▓▄▄▄╓,
                   .╓▄▄▓▓▀▀▀╙╙`         ▓Ñ #▀╜╙   `└╙╙▀▀▓▒▄,
               ,▄▓▓▀╙└                  █∩                ╙▀▓▒▄
            ╓▒▓▀└                      (█                     ▀▓▄
           (█Ñ                  ..,╓▄▄#▓█▓▓▄▄▄▄╓,,..        .,▄▓Ñ
            ╙▀▓▄▄▄╓╓╓▄▄▄▄▄▒▓▓▓▀▀▀╙╙╙└        '└╙╙╙╙▀▀▀▀▀▀▀▀▀▀╙╙    
'''
       
# Main program
#S.G

import json
import requests
import pandas as pd
import numpy as np
import os
from pprint import pprint
import textwrap

# this turns off warning messages
import warnings
warnings.filterwarnings('ignore')

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'


print(logo) #print logo
print('''   
                            #####Where is Bill?#####\n
                        Bills do not turn laws in one day! 
''')
exit = True #exit conditions 1
exit2 = False #exit condition 2
while exit:
    user_input = input("Type 'enter' to continue or type 'quit' to exit the program: ")
    if user_input == "quit":
        break 
    elif user_input == "enter":
        query = input('What subjects are you interested in: ') #user selects keywords for bills search
        bills = getrecentbill(query) #function call
        print("")
        for i in bills:
            print("*****************************")
            print(color.BOLD + "Bill ID:" + color.END, i['bill_id']) #print bill_id
            print(color.BOLD + "Bill Title:" + color.END, i['bill_title']) #print bill_title
            print("*****************************\n")
        while exit: #check for exit condition 1
            user_continue = input('Would you like to learn more information about a law? [Y/N]')
            if user_continue == "N":
                print("No wories. See you later!")
                exit = False #exit program 
                break
            elif user_continue == "Y":
                bill_id = input("Please enter the bill id [ex: hr4909-114]: ")
                bill_tracking = getbillstatus(bill_id) #get more info based on bill_id
                print("")
                for i in bill_tracking:
                    print("*****************************")
                    print(color.BOLD + "Bill: " + color.END, i['bill'])
                    print(color.BOLD + "Bill Title:" + color.END, i['bill_title'])
                    print(color.BOLD + "Bill Short Title:" + color.END, i['short_title'])
                    print(color.BOLD + "Introduced Date:" + color.END, i['introduced_date'])
                    print(color.BOLD + "Active:" + color.END, i['active'])
                    print(color.BOLD + "Bill Latest Major Action:" + color.END, i['latest_major_action'])
                    print(color.BOLD + "Bill Latest Major Action Date:" + color.END, i['latest_major_action_date'])
                    print('')
                    print(color.BOLD + "Bill Last Vote:" + color.END, i['last_vote'])
                    print(color.BOLD + "Bill House Passage:" + color.END, i['house_passage'])
                    print(color.BOLD + "Bill Senate Passage:" + color.END, i['senate_passage'])
                    print(color.BOLD + "Enacted:" + color.END, i['enacted'])
                    print(color.BOLD + "Vetoed:" + color.END, i['vetoed'])
                    print("*****************************\n")
                    exit2 = True #exit condition 2
            else: 
                print("I didn't understand your choice, please try again.\n")                
            while exit2: #exit condition 2
                user_continue2 = input('Would you like to get your federal elected representative contact information? [Y/N]')
                if user_continue2 == "N":
                    print("No worries. See you later!")
                    exit = False
                    break
                elif user_continue2 == "Y":
                    address = getuseraddress() #call to function
                    state_and_district = getstateanddistrict(address) #call to function
                    hr_data = gethrrep(state_and_district) #call to function
                    senate_data = getssenaterep(address) #call to function
                    print("")
                    print("Member of the House of Representative for %s %s district" % (state_and_district['state_abbreviation'], int(state_and_district['congressional_district'])))
                    print("")
                    print("*****************************")
                    print(hr_data)
                    print("*****************************")
                    print("")
                    print("Senators for", state_and_district['state_abbreviation'])
                    print("")
                    print("*****************************")
                    print(senate_data)
                    print("*****************************")
                    exit = False #prevent automatic reset
                    exit2 = False #prevent automatic reset
                else:
                    print("I didn't understand your choice, please try again.\n")
