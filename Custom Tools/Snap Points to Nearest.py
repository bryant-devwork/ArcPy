import arcpy

########################################################################################
## ESRI Documentation:
##  https://doc.esri.com/en/arcgis-pro/latest/arcpy/functions/getparameterastext.html
##  https://doc.esri.com/en/arcgis-pro/latest/tool-reference/analysis/generate-near-table.html?tabs=python
##  https://doc.esri.com/en/arcgis-pro/latest/arcpy/functions/listfields.html
##  https://doc.esri.com/en/arcgis-pro/latest/arcpy/classes/pointgeometry.html
##  https://doc.esri.com/en/arcgis-pro/latest/arcpy/classes/point.html
##  https://doc.esri.com/en/arcgis-pro/latest/arcpy/data-access/searchcursor-class.html
##  https://doc.esri.com/en/arcgis-pro/latest/arcpy/data-access/editor.html
##  https://doc.esri.com/en/arcgis-pro/latest/arcpy/data-access/updatecursor-class.html
##  https://doc.esri.com/en/arcgis-pro/latest/tool-reference/data-management/delete.html?tabs=python
##
##  CAUTION: modifies the input data
##
########################################################################################

## Watch the video: https://youtu.be/KtYGWlPr_dA

## 🤗 Support content creation 👉 https://buymeacoffee.com/glenbambrick

########################################################################################
## USER INPUTS #########################################################################

## input points fc
in_points = arcpy.GetParameter(0)

## the features to snap to
snap_to = arcpy.GetParameter(1)

## only snap within this distance (optional)
search_radius = arcpy.GetParameterAsText(2)

########################################################################################
## REQUIRED OBJECTS ####################################################################

workspace = arcpy.da.Describe(in_points)["path"]

oid_field = [field.name for field in arcpy.ListFields(in_points) if field.type == "OID"][0]

########################################################################################
## GENERATE NEAR TABLE #################################################################

near_tbl = arcpy.analysis.GenerateNearTable(
    in_features = in_points,
    near_features = snap_to,
    out_table = "memory\\near_tbl",
    search_radius = search_radius,
    location = "LOCATION",
    closest = "CLOSEST"
)

########################################################################################
## CREATE OID : NEAR INFORMATION DICTIONARY ############################################

## OID : [X, Y] - to shift to
oid_dict = {
    row[0] : arcpy.PointGeometry(
        inputs = arcpy.Point(
            X = row[1], Y = row[2]
        )
    )
    for row in arcpy.da.SearchCursor(
        in_table = near_tbl,
        field_names = ["IN_FID", "NEAR_X", "NEAR_Y"]
    )
}

##arcpy.AddMessage(oid_dict)

########################################################################################
## DELETE TEMPORARY DATA ###############################################################

arcpy.management.Delete(
    in_data = near_tbl
)

########################################################################################
## MOVE THE POINTS #####################################################################

with arcpy.da.Editor(workspace):
    with arcpy.da.UpdateCursor(
        in_table = in_points,
        field_names = [oid_field, "SHAPE@"]
    ) as u_cursor:
        for row in u_cursor:
            ## if the OID has a matching IN_FID in the oid_dict
            if row[0] in oid_dict:
                ## update the point geometry
                row[1] = oid_dict[row[0]]
                u_cursor.updateRow(row)

########################################################################################
