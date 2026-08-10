import arcpy

########################################################################################
## ArcPy Reference Links:
##  https://doc.esri.com/en/arcgis-pro/latest/tool-reference/environment-settings/current-workspace.html
##  https://doc.esri.com/en/arcgis-pro/latest/arcpy/functions/listfeatureclasses.html
##  https://doc.esri.com/en/arcgis-pro/latest/tool-reference/conversion/feature-class-to-geodatabase.html?tabs=python
##
########################################################################################

## Watch the video: https://youtu.be/2AtL1BIrOt8

## 🤗 Support content creation 👉 https://buymeacoffee.com/glenbambrick

########################################################################################
## USER INPUT ##########################################################################

## folder that stores the shapefiles
shp_folder = r"C:\Users\glenb\Documents\Blogs\Shapefiles"

## path to the file geodatabase
gdb_path = r"C:\Users\glenb\Documents\APRX\Blogs\Processed_Data.gdb"

########################################################################################
## SET THE WORKSPACE ###################################################################

## set the current workspace to shp_folder
arcpy.env.workspace = shp_folder

########################################################################################
## PRINT LIST OF SHAPEFILES ############################################################

##print(*arcpy.ListFeatureClasses(wild_card="*.shp"), sep="\n")

########################################################################################
## OPTION1: CONVERT INDIVIDUALLY #######################################################

## for each shapefile
for shp in arcpy.ListFeatureClasses(wild_card = "*.shp"):
    ## convert to fgdb feature class
    ## you could use another geopocessing tool here instead
    ## for example; you might want to clip all shapefiles to an area of interest
    arcpy.conversion.FeatureClassToGeodatabase(
        Input_Features = shp,
        Output_Geodatabase = gdb_path
    )

########################################################################################
## OPTION 2: BATCH CONVERT #############################################################

## get a list of shapefile names
shp_list = arcpy.ListFeatureClasses(wild_card = "*.shp")

## covert all at once to a fgdb feature class
arcpy.conversion.FeatureClassToGeodatabase(
    Input_Features = shp_list,
    Output_Geodatabase = gdb_path
)

########################################################################################
print("\nSCRIPT COMPLETE")
