import os
import shutil
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.layout import LAParams
from pdfminer.converter import TextConverter
from io import StringIO
from pdfminer.pdfpage import PDFPage
import datetime
from tkinter.filedialog import askdirectory
import PySimpleGUI as sg

def get_pdf_file_content(path_to_pdf):

    #PDFResourceManager is used to store shared resources such as fonts or images that 
    #we might encounter in the files. 
    resource_manager = PDFResourceManager(caching=True)
    
    #create a string object that will contain the final text the representation of the pdf. 
    out_text = StringIO()
    
    #UTF-8 is one of the most commonly used encodings, and Python often defaults to using it.
    #In our case, we are going to specify in order to avoid some encoding errors.
    codec = 'utf-8'
    
    #LAParams is the object containing the Layout parameters with a certain default value. 
    laParams = LAParams()
    
    #Create a TextConverter Object, taking :
    #- ressource_manager,
    #- out_text 
    #- layout parameters.
    text_converter = TextConverter(resource_manager, out_text, laparams=laParams)
    fp = open(path_to_pdf, 'rb')
    
    #Create a PDF interpreter object taking: 
    #- ressource_manager 
    #- text_converter
    interpreter = PDFPageInterpreter(resource_manager, text_converter)
    
    #We are going to process the content of each page of the original PDF File
    for page in PDFPage.get_pages(fp, pagenos=set(), maxpages=0, password="", caching=True, check_extractable=True):
        interpreter.process_page(page)

    #Retrieve the entire contents of the “file” at any time 
    #before the StringIO object’s close() method is called.
    text = out_text.getvalue()

    #Closing all the ressources we previously opened
    fp.close()
    text_converter.close()
    out_text.close()
    
    #Return the final variable containing all the text of the PDF
    return text
    
    
def createDatesTuple(startDay, startMonth, startYear, endDay, endMonth, endYear):
    #Create an empty tuple
    dates = []

    #Create 2 datetime objects by parameters
    currentDate = datetime.datetime(startYear,startMonth,startDay)
    endDate = datetime.datetime(endYear,endMonth,endDay)
 
    #Add the whole days from the range between currentDate to endDate
    while(endDate!=currentDate):
        dates.append(str(currentDate.strftime("%d/%m/%Y")))
        currentDate+=datetime.timedelta(days=1)

    #Return tuple full with dates
    return dates


def runFilter():
    
    #Ask the user to choose source folder
    sourceDirPath = askdirectory(title='Select Source folder')
    print("Source Folder is: " + sourceDirPath)

    #Ask the user to choose target folder
    targetDirPath = askdirectory(title='Select Target folder')
    print("Target Folder is: " + targetDirPath)

    #Create list of files from the source folder
    pdfs = os.listdir(sourceDirPath)

    #Delete unimportant file
    if("desktop.ini" in pdfs):
        pdfs.remove("desktop.ini")
    
    #Print how many files found in the source folder
    print(str(len(pdfs)) + " found in the source folder")

    #Empty variables for the filters
    startDate=""
    endDate=""
    mustHaveWords=""

    #Build the layout of the GUI using pySimpleGUI
    layout = [  [sg.Text('Select dates')],
                [sg.Text('Enter start date'), sg.InputText(key='start_date')],
                [sg.Text('Enter end date'), sg.InputText(key='end_date')],
                [sg.Text('Enter must-have words'), sg.InputText(key='must_have_words')],                
                [sg.Button('Ok')]]

    #Create the filters Window
    window = sg.Window("Filters", layout).Finalize()

    #Event Loop to process "events" and get the "values" of the inputs
    while True:
        
        event, values = window.read()

        #If the button clicked than save the filters variables
        if event in ('Ok'):
            startDate=str(values['start_date'])
            endDate=str(values['end_date'])
            mustHaveWords=str(values['must_have_words'])
            break

    window.close()
    
    #Create tuple for every date (string format "dd/mm/yyyy" to tuple -> a[0]=day, a[1]=month, a[2]=year)
    startDateList = startDate.split("/")
    endDateList = endDate.split("/")

    #Create tuple for keywords that must appear in the text
    mustHaveWordsList = mustHaveWords.split(",")

    #Using the createDatesTuple function by user input
    dates = createDatesTuple(int(startDateList[0]),int(startDateList[1]),int(startDateList[2]),int(endDateList[0]),int(endDateList[1]),int(endDateList[2]))
    print("Starting to search " + dates[0] + "-" +dates[len(dates)-1])

    #Current file index
    count=1
    #Loop over all the files in source folder
    for pdf in pdfs:
        
        #Calculate the current file path in source folder
        filePath =r""+sourceDirPath+"\\"+str(pdf)

        #Change it into lowercase text
        text = get_pdf_file_content(filePath).lower()
        
        #Print cuurent file index
        print(count)

        #Check if every word is in the text
        inWords = True
        for word in mustHaveWordsList:
            if word not in text:
                inWords = False
                break

        #Check if one of the dates from the tuple is in the text
        inDates = False
        for day in dates:
            if day in text:
                inDates = True
                break
        
        #Check if both conditions are met
        if(inDates==True):
            if(inWords==True):
                print(filePath)#Print file path
                shutil.move(filePath,targetDirPath)#Move the file to the target folder
        
        #Moving to the next file
        count+=1

#Main call
runFilter()

