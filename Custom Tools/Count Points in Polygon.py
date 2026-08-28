import arcpy

########################################################################################
## Documentation Links:
##  https://doc.esri.com/en/arcgis-pro/latest/arcpy//functions/getparameter.htm
##  https://doc.esri.com/en/arcgis-pro/latest/arcpy/functions/getparameterastext.html
##  https://doc.esri.com/en/arcgis-pro/latest/tool-reference/data-management/calculate-field.html?tabs=python
##
########################################################################################

## Watch the video here: https://youtu.be/SQgEUi94XWs

## 🤗 Support content creation 👉 https://buymeacoffee.com/glenbambrick

########################################################################################
## USER INPUTS #########################################################################

## the points to count
point_features = arcpy.GetParameterAsText(0)

## optional where clause
where_clause = arcpy.GetParameterAsText(1)

## the polygon featyre classes to count the number of points
polygon_features = arcpy.GetParameterAsText(2)

## the field from the polygon_features to use for the count attribute
count_field = arcpy.GetParameterAsText(3)

########################################################################################
## COUNT POINTS IN POLYGON #############################################################

arcpy.management.CalculateField(
    in_table = polygon_features,
    field = count_field,
    expression = f"""var points = Filter(FeatureSetByName($datastore, "{point_features}", ["{where_clause.split(" ")[0]}"], false), "{where_clause}")
return Count(Intersects(points, $feature))""",
    expression_type = "ARCADE"
)

########################################################################################