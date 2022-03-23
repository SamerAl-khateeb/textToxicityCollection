# getToxicityScores.py                 By: Samer Al-khateeb
# a script that can read text from a CSV file and 
# return the toxicity score of the text as calculated 
# by Google Perspective API (https://www.perspectiveapi.com)

# To be able to run the code using IDLE you have to do the following 
# (if you never did it before):
# For Mac users, open terminal and type:
#   python3 -m pip install --upgrade pip==19.0.3
#   python3 -m pip install google-auth-oauthlib
#   python3 -m pip install --upgrade google-api-python-client

# For Windows users, open CMD and type:
#   py -m pip install --upgrade pip==19.0.3
#   py -m pip install google-auth-oauthlib
#   py -m pip install --upgrade google-api-python-client


from googleapiclient import discovery
from datetime import datetime
import time  
import csv
import json


def write_output_to_CSV(biglist):
    # get the current date so we can 
    # append it to the CSV output file name
    now = datetime.now()
    dateAsString = now.strftime("%m-%d-%Y")
    # name of csv file
    filename = "outputWithToxicityScore{}.csv".format(dateAsString)

    # column names
    columnNames = ["ID", "Text", "ToxicityScore"]

    # data rows of csv file
    rows = biglist

    # creating a file to save the output
    with open(filename, 'w', newline='', encoding='utf-8') as csvOutputFile:
        #creating a csv writer object 
        csvwriter = csv.writer(csvOutputFile, delimiter=',', lineterminator='\n')
        #write the columns headers
        csvwriter.writerow(columnNames)
        csvwriter.writerows(rows)
    

def main():
    # paste your own API key below
    apiKey = 'pasteYourAPIKeyHere!'

    client = discovery.build(
        "commentanalyzer", 
        "v1alpha1", 
        developerKey = apiKey, 
        discoveryServiceUrl = "https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1", 
        )

    # an input file contain the text we want to calculate its toxicity score
    fileName = "input_file.csv"
    
    # list to hold all the info that will be written later to a file
    CSVOutputList = []

    # open the file
    with open(fileName, 'r', encoding='utf-8') as csvInputFile:
        # read the CSV file
        inputFileContents = csv.reader(csvInputFile)
        # skip first row, i.e., read the column headers first
        header = next(inputFileContents)

        # Iterate over each row after the header in the csv
        for row in inputFileContents:

            # the first column is the row ID
            rowID = row[0]

            # the second column is the text, change it if otherwise
            columnContainTheText = row[1]
            
            try:
                analyze_request = { 'comment': { 'text': columnContainTheText }, 'requestedAttributes': {'TOXICITY': {}}}
                response = client.comments().analyze(body=analyze_request).execute()
                
                summaryScore = response["attributeScores"]["TOXICITY"]["summaryScore"]["value"]

            # checking for errors returned from the API itself
            except OSError as excObj:
                if str(excObj) == "COMMENT_TOO_LONG":
                    print("text is too long")
                    summaryScore = 0
                elif str(excObj) == "COMMENT_EMPTY":
                    print("text is empty")
                    summaryScore = 0
                elif str(excObj) == "NO_REQUESTED_ATTRIBUTES":
                    print("the attribute requested is not there")
                    summaryScore = 0
                elif str(excObj) == "LANGUAGE_NOT_SUPPORTED_BY_ATTRIBUTE":
                    print("language is not supported")
                    summaryScore = 0
                elif str(excObj) == "LANGUAGE_DETECTION_FAILED":
                    print("failed to detect the language")
                    summaryScore = 0

            # any other error, we assign a value of Zero to the row
            except:
                print("skipping tweet number ", rowID)
                summaryScore = 0
                print("assigning tweet number ", rowID, " a score of Zero")
            
            # comment out the line below if you do not want to see output on the screen
            print(rowID, columnContainTheText, summaryScore)
            
            # creating a list of values (a row) 
            CSVOutputRow = [rowID, columnContainTheText, summaryScore]

            # adding the row to the output list
            CSVOutputList.append(CSVOutputRow)

            # making a request every one second 
            # to avoid hitting rate limit
            time.sleep(1)

    # send the list to the function to creat the CSV output file.
    write_output_to_CSV(CSVOutputList)
        
if __name__ == "__main__":
    main()
