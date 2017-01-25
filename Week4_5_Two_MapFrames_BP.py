"""
This scripts controls various components of the mxd from outside of the Arc environment.
Controlled elements include the data frame extent and scale bar, title and figure name text,
ancillary text elements, and queries on various map layers.

Contact http://github.com/parkerw13 with any questions pertaining to the script
"""

#import arcpy and os
import arcpy, os

#print statement for starting the script
print "starting . . . "


#variables
#insert today's date to give figures unique name
todaysDate = "20151027"
print todaysDate
#create an mxd object
mxd = arcpy.mapping.MapDocument(r"C:\Users\William\Desktop\Python\Week4\Week4\MXDs\MapAdjust_TwoFrames.mxd")
#create sql query to select specific routes/stops
SQL = "NAME = '71 IB' AND BUS_SIGNAG = 'Ferry Plaza'"
#Create object for the top map frame
TopLayer = arcpy.mapping.ListDataFrames(mxd)[0]
print TopLayer
#Create object for the bottom map frame
BottomLayer = arcpy.mapping.ListDataFrames(mxd)[1]
print BottomLayer
#Create object for the grid layer in the top map frame
TopLayerDriver = arcpy.mapping.ListLayers(TopLayer,"Bus Stops*")[0]
print TopLayerDriver
#Create object for the grid layer in the bottom map frame
BottomLayerDriver = arcpy.mapping.ListLayers(BottomLayer,"Bus Stops*")[0]
print BottomLayerDriver


#Make feature layers for the top and bottom grid layers
arcpy.MakeFeatureLayer_management(TopLayerDriver,"TopFL",SQL)
arcpy.MakeFeatureLayer_management(BottomLayerDriver,"BotFL",SQL)

#print statment to show where in the script you are
print "Checkpoint 1"

#PDF folder to output all pdfs to
pdfFolder = r"C:\Users\William\Desktop\Python\Week4\Week4\PDF_output"
print "check set pdf folder"
#MXD folder to save all mxds to
mxdFolder = r"C:\Users\William\Desktop\Python\Week4\Week4\MXD_output"
print "check set mxd folder"

#total pages in the grid to be run
totalPages = 4 #change as needed

#starting page number
n = 1

#print statment to show where in the script you are
print "Checkpoint 2"

#start a while loop to create new sets of maps
while n <= totalPages:

    #SQL statement to select the Driver map for the top
    sqlTop = SQL + "AND SEQUENCE = {0}".format(n)
    print sqlTop 
    TopLayerDriver.definitionQuery  = sqlTop
    #SQL statement to select the Driver map for the bottom
    sqlBot = SQL + "AND SEQUENCE = {0}".format(n+1)
    print sqlBot
    BottomLayerDriver.definitionQuery  = sqlBot

    #Select Driver layer by the sql statement 
    arcpy.SelectLayerByAttribute_management ("TopFL", "NEW_SELECTION", sqlTop)
    arcpy.SelectLayerByAttribute_management ("BotFL", "NEW_SELECTION", sqlBot)
    print "check select layer by attribute"

    #Iterate through the top grid to get page number and scale information for later use
    rows = arcpy.SearchCursor ("TopFL")
    print "check create search cursor"
    for row in rows:
        #get the page number value from the grid index
        PageNumber = row.getValue("SEQUENCE")
        print PageNumber
    #set extent to the selected scale
    selectExtent = TopLayerDriver.getSelectedExtent()
    TopLayer.extent = selectExtent
    TopLayer.scale = 4000
    arcpy.RefreshActiveView()

    #Iterate through the top grid to get page number and scale information for later use
    brows = arcpy.SearchCursor ("BotFL")
    print "check create search cursor"
    for brow in brows:
        #get the page number value from the grid index
        PageNumberB = brow.getValue("SEQUENCE")
        print PageNumberB
    #set extent to the selected scale
    selectExtentB = BottomLayerDriver.getSelectedExtent()
    BottomLayer.extent = selectExtentB
    BottomLayer.scale = 4000
    arcpy.RefreshActiveView()



    # update text elements in the map
    print "Updating text elements . . . "
    #set the title 
    Title = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "Title")[0]
    Title.text = SQL.replace("NAME = ","Bus Route: ").replace("'","").replace("BUS_SIGNAG = ","Bus Signage: ")
    print Title.text
    Title.elementPositionX = 9.6967
    Title.elementPositionY = 7.9
    
    #set subtitle
    subTitle = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "Subtitle")[0]
    subTitle.text = "Pages " + str(PageNumber) + " and " + str(PageNumberB) + " of " + str(totalPages)
    print Title.text
    subTitle.elementPositionX = 9.7001
    subTitle.elementPositionY = 7.6714

    #position scale bar
    scaleBar = arcpy.mapping.ListLayoutElements(mxd, "MAPSURROUND_ELEMENT", "ScaleBar")[0]
    scaleBar.elementPositionX = 8.9
    scaleBar.elementPositionY = 1.1125

    #create pdf name and export to pdf
    pdfName = SQL.replace(" = ","_").replace("'","").replace(" ","") + str(PageNumber) + "_" + str(PageNumberB)
    outputPDF = os.path.join(pdfFolder,pdfName)
    arcpy.mapping.ExportToPDF(mxd, outputPDF)

    print pdfName + " exported"
    print "saving mxd . . . "

    #save as an mxd
    mxdName = pdfName + ".mxd"
    outputMXD = os.path.join(mxdFolder,mxdName)
    mxd.saveACopy(outputMXD)
    print mxdName + " saved"

    print "......................"
    print "......................"
    #increase n by 2
    n += 2

   
#delete mxd object to release schema lock on mxd
del mxd

#Print a finishing statement
print "script completed" 

    
