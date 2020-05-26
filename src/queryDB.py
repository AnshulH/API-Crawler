from tinydb import TinyDB, Query

# A sample query to database that returns all parent categories
db = TinyDB('databases/parentCategoryDB.json')
parentCategoryDB = db.table('CategoryEntries')
print('All parent categories from public api')
print()
print(parentCategoryDB.all())
print()


# A sample query to database that returns all api entries whose parent category == 'Tracking'
# More sample queries can be found at -> https://www.idkrtm.com/using-tinydb-with-python/
db = TinyDB('databases/categoryEntryDB.json')
categoryEntryDB = db.table('ApiEntries')
result = categoryEntryDB.search(Query()['ParentCategory'] == 'Tracking')
print(result)
