import shebaoka

jgh_sht = shebaoka.readJghExcle("机构号.xls")
print(jgh_sht)
shebaoka.writesql_jgh(jgh_sht)
