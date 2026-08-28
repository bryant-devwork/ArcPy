import arcpy

########################################################################################
## Documentation Links:
##  https://doc.esri.com/en/arcgis-pro/latest/arcpy//functions/getparameter.htm
##  https://doc.esri.com/en/arcgis-pro/latest/arcpy/functions/getparameterastext.html
##  https://doc.esri.com/en/arcgis-pro/latest/tool-reference/data-management/calculate-field.html?tabs=python
##
##  Note: this will not tell you if attachments are enabled or not. If attachments
##        are not enabled, 0 (zero) will be returned for each feature.
##
########################################################################################

## Watch the video: https://youtu.be/rbTYMNiLLng

## 🤗 Support content creation 👉 https://buymeacoffee.com/glenbambrick

########################################################################################
## USER INPUTS #########################################################################

## the feature layer to count the attachments for
in_features = arcpy.GetParameter(0)

## the field to update the counts
count_field = arcpy.GetParameterAsText(1)

########################################################################################
## GET ATTACHMENT COUNT PER FEATURE ####################################################

arcpy.management.CalculateField(
    in_table = in_features,
    field = count_field,
    expression = "Count(Attachments($feature))",
    expression_type = "ARCADE"
)

########################################################################################