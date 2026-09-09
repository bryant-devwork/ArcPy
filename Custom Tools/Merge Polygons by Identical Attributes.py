import arcpy

########################################################################################
## Documentation Links:
##  https://doc.esri.com/en/arcgis-pro/latest/arcpy//functions/getparameter.htm
##  https://doc.esri.com/en/arcgis-pro/latest/arcpy/data-access/searchcursor-class.html
##  https://doc.esri.com/en/arcgis-pro/latest/arcpy/classes/polygon.html
##  https://doc.esri.com/en/arcgis-pro/latest/tool-reference/data-management/delete-identical.html?tabs=python
##  https://doc.esri.com/en/arcgis-pro/latest/arcpy/data-access/updatecursor-class.html
##
##  Notes: Back up your original feature class. You could factor that into the script
##         to automatically backup with a datestamp.
##         Expects text fields that do not contain NULL values.
##         Modifies the input dataset.
##         Does not sum/average other fields.
##
########################################################################################

## Watch the video: https://youtu.be/2f0SKPqJPJU

## 🤗 Support content creation 👉 https://buymeacoffee.com/glenbambrick

########################################################################################
## USER INPUTS #########################################################################

## polygon input
polygon_fc = arcpy.GetParameter(0)

## text fields only
fields = arcpy.GetParameter(1)

########################################################################################
## REQUIRED OBJECTS ####################################################################

## get the field names as a list from the input
fields = [field.value for field in fields]

## get a set of unique attribute combinations
field_combos = {
    row
    for row in arcpy.da.SearchCursor(
        in_table = polygon_fc,
        field_names = fields
    )
}

## (field_1, field_2, field_3, field_n) : unioned geometry
geom_dict = {}

########################################################################################
## GET UNIONED GEOMETRY ################################################################

## NOTE: does not account for NULLS in fields ##

## for each available field_combo
for field_combo in field_combos:
    ## this will be the where clause
    ## eg. "field_1 = 'value_1' AND field_2 = 'value_2' AND field_3 = 'value_3'"
    sql_exp = " AND ".join(
        f"{field} = '{value}'"
        for field, value in zip(fields, field_combo)
    )

    ## get the geomtries
    geoms = [
        row[0]
        for row in arcpy.da.SearchCursor(
            in_table = polygon_fc,
            field_names = "SHAPE@",
            where_clause = sql_exp
        )
    ]

    ## no need to do anything for single features
    if len(geoms) > 1:
        ## union the polygon geoms
        unioned_geom = geoms[0]

        for geom in geoms[1:]:
            unioned_geom = unioned_geom.union(geom)

        ## add to dictionary
        geom_dict[field_combo] = unioned_geom

########################################################################################
## DELETE IDENTICAL ####################################################################

polygon_fc = arcpy.management.DeleteIdentical(
    in_dataset = polygon_fc,
    fields = fields
)

########################################################################################
## UPDATE GEOMETRY #####################################################################

## for each available field_combo
for field_combo in field_combos:
    ## this will be the where clause
    sql_exp = " AND ".join(
        f"{field} = '{value}'"
        for field, value in zip(fields, field_combo)
    )

    with arcpy.da.UpdateCursor(
        in_table = polygon_fc,
        field_names = fields + ["SHAPE@"],
        where_clause = sql_exp
    ) as cursor:
        for row in cursor:
            ## if union happened, its in the dict.
            if field_combo in geom_dict:
                row[-1] = geom_dict[field_combo]
                cursor.updateRow(row)

########################################################################################