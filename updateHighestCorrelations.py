from MainService import MainService
m = MainService()
m.updateAllData()
columns = ['Id','Id1', 'Corr1', 'Id2', 'Corr2', 'Id3', 'Corr3', 'Id4', 'Corr4', 'Id5', 'Corr5']
m.dropTable('HighestCorrelations')
m.createTable('HighestCorrelations', columns)
counter = 0
to_execute = []
for Id in m.MasterData.MasterPrices:
	print(Id)
	sql_vals = [Id]
	corrs = m.findFiveHighestCorrelated(Id)
	for tup in corrs:
	    for val in tup:
	        sql_vals.append(val)
	to_execute.append(tuple(sql_vals))
db, cursor = m.connectToSqlServer()
vals = [None,None,None,None,None,None,None,None,None,None,None]
command = m.insertIntoTable('HighestCorrelations', columns, vals)
cursor.executemany(command, to_execute)
db.commit()
