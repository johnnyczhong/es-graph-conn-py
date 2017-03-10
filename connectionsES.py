from flask import Flask
import Connections
import time
from elasticsearch import client, Elasticsearch


app = Flask(__name__)
es = Elasticsearch(['http://localhost:9200'])
ic = client.IndicesClient(es)

host = 'localhost'
port = '9200'

@app.route('/')
def hello():
	return "hello world!"

@app.route('/<index>/user/<int:uid>/connections/all', methods = ['GET'])
def getAllUserConnections(index, uid):
	if not validateId(index, uid):
		return 'Please check bounds of uid.'

	iTime = time.time()

	# init objects
	queryUser = Connections.User(uid)
	gc = Connections.GraphApi(host, port, index)

	queryUser.set1and2dConn(gc)
	queryUser.set3dConn(gc)

	fTime = time.time()
	str1st = 'Num 1st degree Connections: {}'.format(len(queryUser.conn1d))
	str2nd = 'Num 2nd degree Connections: {}'.format(len(queryUser.conn2d))
	str3rd = 'Num 3rd degree connections: {}'.format(len(queryUser.conn3d))
	return '{} \n{} \n{} \nTook {}s'.format(str1st, str2nd, str3rd, (fTime - iTime))


@app.route('/<index>/user/<int:uid>/connections/<int:conn>', methods = ['GET'])
def getSingleDegreeConnections(index, uid, conn):
	if not validateId(index, uid):
		return 'Please check bounds of uid.'

	iTime = time.time()

	queryUser = Connections.User(uid)
	gc = Connections.GraphApi(host, port, index)

	if conn == 1:
		queryUser.set1dConn(gc)
		retString = 'Num 1st Degree Connections: {}'.format(len(queryUser.conn1d))
	elif conn == 2:
		queryUser.set1and2dConn(gc)
		retString = 'Num 2nd Degree Connections: {}'.format(len(queryUser.conn2d))
	elif conn == 3:
		queryUser.set1and2dConn(gc)
		queryUser.set3dConn(gc)
		retString = 'Num 3rd Degree Connections: {}'.format(len(queryUser.conn3d))
	else:
		return 'Please provide a number between 1-3.'

	fTime = time.time()
	retString += ' Took: {}'.format(fTime - iTime)
	return retString

def validateId(index, uid):
	upperLimit = (ic.stats(index = index))['indices'][index]['primaries']['docs']['count']
	return (uid <= upperLimit and uid >= 0)

if __name__ == '__main__':
	app.run()