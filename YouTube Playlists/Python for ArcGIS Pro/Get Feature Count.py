import arcpy

########################################################################################
## ArcPy Reference Links:
##  https://pro.arcgis.com/en/pro-app/latest/tool-reference/data-management/get-count.htm
##  https://pro.arcgis.com/en/pro-app/latest/arcpy/classes/result.htm
##
########################################################################################

## Watch the video: https://youtu.be/5kUfhX8vu4s

## 🤗 Support content creation 👉 https://buymeacoffee.com/glenbambrick

########################################################################################
## USER INPUT ##########################################################################

## the path to the feature class to get the feature count
fc_path = r"C:\path\to\fc_or_table"

########################################################################################
## GET COUNT ###########################################################################

feature_count = arcpy.management.GetCount(
    in_rows = fc_path
)

print(feature_count)
#print(int(feature_count)) ## this will fail (TypeError) cannot cast Result to int
print(feature_count[0])
print(type(feature_count[0])) # number is a string
print(int(feature_count[0])) # cast to integer
print(type(feature_count)) # Result object returned from geoproccessing tool.
print(feature_count.outputCount) # GetCount returns one output
print(feature_count.getOutput(0)) # access the output via the Result object

########################################################################################
print("\nSCRIPT COMPLETE")