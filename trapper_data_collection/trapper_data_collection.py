import pandas as pd
from arcgis.gis import GIS
from copy import deepcopy
gis = GIS("home")

traps_item = gis.content.get('ecce1f5fcca54365823c6914c3f92fde')
traps_flayer = traps_item.layers[0]
traps_fset = traps_flayer.query(where='INCLUDE_COORDINATES=\'NO\'') #querying without any conditions returns all the features
if len(traps_fset) > 0:
    grid_list = traps_fset.sdf['MESO_GRID_ID'].tolist()
    str_list = ','.join([f'\'{a}\'' for a in grid_list])
    sql = f'MesoCell IN ({str_list})'
    mesogrid_item = gis.content.get('75e90b00f2034c499a6ca4b55d30aa4c')
    mesogrid_flayer = mesogrid_item.layers[0]
    mesogrid_fset = mesogrid_flayer.query(where=sql)
    overlap_rows = pd.merge(left = traps_fset.sdf, right = mesogrid_fset.sdf, how='inner',
                       left_on = 'MESO_GRID_ID', right_on='MesoCell')
    
    features_for_update = [] #list containing corrected features
    all_features = traps_fset.features
    traps_fset.spatial_reference
    for trap_set in overlap_rows['SET_UNIQUE_ID']:
        # get the feature to be updated
        original_feature = [f for f in all_features if f.attributes['SET_UNIQUE_ID'] == trap_set][0]
        mesogrid_id = original_feature.attributes['MESO_GRID_ID']
        print(mesogrid_id)
        feature_to_be_updated = deepcopy(original_feature)
    
        matching_row = mesogrid_fset.sdf.where(mesogrid_fset.sdf.MesoCell == mesogrid_id).dropna()

        input_geometry = {'y':float(matching_row['CENTROID_Y']),
                           'x': float(matching_row['CENTROID_X'])}
        feature_to_be_updated.geometry = input_geometry
        
        features_for_update.append(feature_to_be_updated)
    
    traps_flayer.edit_features(updates=features_for_update)

    tbl_trap_check = traps_item.tables[0]
traps_fset = traps_flayer.query()
features_for_update = [] #list containing corrected features
all_features = traps_fset.features
for trap in traps_fset:
    unique_id = trap.attributes['SET_UNIQUE_ID']
    trap_status = trap.attributes['TRAP_STATUS']
    print(unique_id)
    trap_check_subset = tbl_trap_check.query(where=f'SET_UNIQUE_ID=\'{unique_id}\'')
    if len(trap_check_subset) == 0:
        continue
    lst_check_nums = trap_check_subset.sdf['TRAP_CHECK_NUMBER'].tolist()
#     set_id = trap_check_subset.sdf['TRAP_CHECK_NUMBER'].iloc[-1]

    print(lst_check_nums[-1])
    latest_check = trap_check_subset.sdf.loc[trap_check_subset.sdf['TRAP_CHECK_NUMBER'] == lst_check_nums[-1]]
    check_status = latest_check.iloc[0]['TRAP_STATUS']
    if trap_status != check_status:
        original_feature = [f for f in all_features if f.attributes['SET_UNIQUE_ID'] == unique_id][0]
        feature_to_be_updated = deepcopy(original_feature)
        feature_to_be_updated.attributes['TRAP_STATUS'] = check_status
        features_for_update.append(feature_to_be_updated)
if features_for_update:
    traps_flayer.edit_features(updates=features_for_update)



trap_check_fset = tbl_trap_check.query()
lst_oids = trap_check_fset.sdf['OBJECTID'].tolist()
attachments_for_update = []
for oid in lst_oids:
    lst_attachments = tbl_trap_check.attachments.get_list(oid=oid)
    if lst_attachments:
        for attachment in lst_attachments:
            print(attachment)
            print(attachment['name'])
            attachment_update = deepcopy(attachment)
            print(attachment_update)
            attachment_update['name'] = 'Test.jpg'
            print(attachment_update)
            attachments_for_update.append(attachment_update)
if attachments_for_update:
    tbl_trap_check.attachments.edit_features(updates=attachments_for_update)