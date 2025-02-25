from App.src.Dehoop import Dehoop
from App.src.TransFormer import Transerfrom_addColumn,Transerfrom_mappingList,ExtraColumn,ReMappingList

projectName = "恒邦POT"

d = Dehoop("192.168.16.100",30104)
d.Login("hbbxlb","hbbx@2024")
toTableName = "ggcode"
fromTableName = "hbcore_20160531.ggcode"
fromDbId = "643763299611049984"
toDbId = "643766294172139520"
column_list:list[dict]= d.GetColumnInfos(projectName,toDbId,toTableName,"dist")
column_list_src:list[dict] = d.GetColumnInfos(projectName,fromDbId,fromTableName,"src")
mappingList = Transerfrom_mappingList(column_list,fromTableName,toTableName)

field,uuid,new_column = ExtraColumn("etl_timestamp",fromTableName,"localtimestamp")
mappingList = ReMappingList(mappingList,field,uuid)

addColumnList = Transerfrom_addColumn(column_list_src,fromTableName)
addColumnList.append(new_column)

d.SaveOrUpdateSyncWork(projectName,"677539718023348224",fromDbId,fromTableName,toDbId,toTableName,mappingList,addColumnList)
