from MainService import MainService
m = MainService()
m.updateAllData()
columns = ['Id','Id1', 'Corr1', 'Id2', 'Corr2', 'Id3', 'Corr3', 'Id4', 'Corr4', 'Id5', 'Corr5']
m.dropTable('HighestCorrelations')
m.createTable('HighestCorrelations', columns)
counter = 0
for Id in m.MasterData.MasterPrices:
    sql_vals = [Id]
    try:
        corrs = m.findFiveHighestCorrelated(Id)
        for tup in corrs:
            for val in tup:
                sql_vals.append(val)
        m.insertIntoTable('HighestCorrelations', columns, sql_vals)
    except:
        print('not five valid Ids')