from tinydb import TinyDB, Query

db = TinyDB('databases/categoryEntryDB.json')
categoryEntryDB = db.table('ApiEntries')
result = categoryEntryDB.search(Query()['ParentCategory'] == 'Anti-Malware')
print(result)