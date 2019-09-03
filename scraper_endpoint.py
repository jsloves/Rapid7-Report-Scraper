# Text file scraper for use of scraping numbers from InsightVM report
# Might hang for a few seconds after running.

# ********************************
# Credit to Pablo Macias on Quora for providing helpful code
# https://www.quora.com/How-do-I-parse-a-text-file-in-Python-and-get-the-sum-of-the-numbers-present-in-the-file
# ********************************
import re
import os
import sys

def previousFileInput():
    previousFile = input("Enter the previous endpoint report's file name (case sensitive with file extension): \n")
    #previousFile = '.txt' # manual input
    return previousFile

def currentFileInput():
    currentFile = input("Enter the current endpoint report's file name (case sensitive with file extension): \n")
    #currentFile = '.txt' # manual input
    return currentFile

def processPreviousFile(): # scrape file for relevant values
    try:
        previousFile = previousFileInput()
        f = open(previousFile)
        fdata = f.read()
        print("Scraping file 1...")

        # regular expression to find relevant sentences 
        obj = re.compile('(performed on \d+,?\d*,?\d*)|(There were \d+,?\d*,?\d* vulnerabilities)|(Of these, \n? ? ?\d+,?\d*,?\d*)|(\d*,?\d*,?\d* ?\n? ? ?vulnerabilities were \n? ? ?severe)|(There were \n? ? ?\d*,?\d*,?\d* moderate)|(exist on \d*,?\d*,?\d*)|(\d*,?\d*,?\d* systems were found)|(were found on \d*,?\d*,?\d* systems)|(on the remaining \d*,?\d*,?\d* systems)')
        sentences = obj.findall(fdata)
        # regular expression to find values within sentences
        obj2 = re.compile('\d+,?\d*,?\d*')
        num = obj2.findall(str(sentences))
 
        f.close()
        return num
    
    except FileNotFoundError:
        print('File does not exist.')
        main()

def processCurrentFile(): # scrape file for relevant values
    try:
        currentFile = currentFileInput()
        f = open(currentFile)
        fdata = f.read()
        print("Scraping file 2...")

        # regular expression to find relevant sentences 
        obj = re.compile('(performed on \d+,?\d*,?\d*)|(There were \d+,?\d*,?\d* vulnerabilities)|(Of these, \n? ? ?\d+,?\d*,?\d*)|(\d*,?\d*,?\d* ?\n? ? ?vulnerabilities were \n? ? ?severe)|(There were \n? ? ?\d*,?\d*,?\d* moderate)|(exist on \d*,?\d*,?\d*)|(\d*,?\d*,?\d* systems were found)|(were found on \d*,?\d*,?\d* systems)|(on the remaining \d*,?\d*,?\d* systems)')
        sentences = obj.findall(fdata)
        # regular expression to find values within sentences
        obj2 = re.compile('\d+,?\d*,?\d*')
        num = obj2.findall(str(sentences))
 
        f.close()
        return num
    
    except FileNotFoundError:
        print('File does not exist.')
        main()
        
def get_change(current, previous):
    if current == previous:
        return 100
    try:
        return (abs(current - previous) / previous) * 100.0
    except ZeroDivisionError:
        return 0
    
def main():
    numPrevious = processPreviousFile() # get previous report's numbers
    numCurrent = processCurrentFile() # get current report's numbers

    if (len(numPrevious) == 8): # case if no systems have vulnerabilities
        numPrevious.append("0")

    # purpose is to store int versions of numPrevious and numCurrent
    numPreviousTemp = (numPrevious)
    numCurrentTemp = (numCurrent)
    
    temp = [] 
    temp2 = []
    difference = []
    pct = []
    
    length = len(numPreviousTemp)
    for i in range(length): # change from list to array
        temp.append(numPreviousTemp[i])

    for i in range(length): # change from list to array
        temp2.append(numCurrentTemp[i])

    for i in range(length): # remove commas from ints
        temp[i] = int(temp[i].replace(',', ''))
        
    for i in range(length): # remove commas from ints
        temp2[i] = int(temp2[i].replace(',', ''))
        
    for i in range(length): # populate array that contains the differences
        difference.append(int(temp2[i])- int(temp[i]))

    for i in range(length):
        pct.append(float(round(get_change(temp[i], temp2[i]),1)))
        
    numPrevious[0] = "Total Assets\t" + numPrevious[0]
    numPrevious[1] = "Total Vuln\t" + numPrevious[1]
    numPrevious[2] = "Critical Vuln.\t" + numPrevious[2]
    numPrevious[3] = "Severe Vuln.\t" + numPrevious[3]
    numPrevious[4] = "Moderate Vuln\t" + numPrevious[4]
    numPrevious[5] = "Systems with critical\t" + numPrevious[5]
    numPrevious[6] = "Systems with severe\t" + numPrevious[6]
    numPrevious[7] = "Systems with moderate\t" + numPrevious[7]
    numPrevious[8] = "Systems with none\t" + numPrevious[8]

    numCurrent[0] = "Total Assets\t" + numCurrent[0]
    numCurrent[1] = "Total Vuln\t" + numCurrent[1]
    numCurrent[2] = "Critical Vuln.\t" + numCurrent[2]
    numCurrent[3] = "Severe Vuln.\t" + numCurrent[3]
    numCurrent[4] = "Moderate Vuln\t" + numCurrent[4]
    numCurrent[5] = "Systems with critical\t" + numCurrent[5]
    numCurrent[6] = "Systems with severe\t" + numCurrent[6]
    numCurrent[7] = "Systems with moderate\t" + numCurrent[7]
    numCurrent[8] = "Systems with none\t" + numCurrent[8]

    difference[0] = "Difference in Total Assets\t" + str(difference[0]) + "\t" + str(pct[0]) + "%"
    difference[1] = "Difference in Total Vuln.\t" + str(difference[1]) + "\t" + str(pct[1]) + "%"
    difference[2] = "Difference in Critical Vuln.\t" + str(difference[2]) + "\t" + str(pct[2]) + "%"
    difference[3] = "Difference in Severe Vuln.\t" + str(difference[3]) + "\t" + str(pct[3]) + "%"
    difference[4] = "Difference in Moderate Vuln\t" + str(difference[4]) + "\t" + str(pct[4]) + "%"
    difference[5] = "Difference in Systems with Critical\t" + str(difference[5]) + "\t" + str(pct[5]) + "%"
    difference[6] = "Difference in Systems with Severe\t" + str(difference[6]) + "\t" + str(pct[6]) + "%"
    difference[7] = "Difference in Systems with Moderate\t" + str(difference[7]) + "\t" + str(pct[7]) + "%"
    difference[8] = "Difference in Systems with None\t" + str(difference[8]) + "\t" + str(pct[8]) + "%"
    os.chdir('..')
    outputFile = open("Output_Endpoint.txt", "w")
    outputFile.write('\n'.join(numPrevious))
    outputFile.write('\n\n')
    outputFile.write('\n'.join(numCurrent))
    outputFile.write('\n\n')
    outputFile.write("\n".join(difference))

    print("Success!")
    outputFile.close()
    os.startfile('Output_Endpoint.txt')
    input("Press enter to exit")
    sys.exit()
    
if __name__ == '__main__':
    print("Check parent directory for output location.")
    main()
