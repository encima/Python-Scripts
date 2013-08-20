import MySQLdb as ms
from ConfigParser import SafeConfigParser


def connect(key):
	parser = SafeConfigParser()
	parser.read('config.ini')
	db  = ms.connect(parser.get(key, 'HOST'), parser.get(key, 'USER'), parser.get(key, 'PWD'), parser.get(key, 'DB'))
	return db.cursor(ms.cursors.DictCursor)

def query(cursor, string):
	cursor.execute(string)
	return cursor.fetchall()