from flask import Flask
import Connections
import time
app = Flask(__name__)
host = 'localhost'
port = '9200'

@app.route('/')
def hello():
	return "Hello Person!"

# @app.route('/{}/user/<uid>'.format(index), methods = ['GET'])
@app.route('/<index>/user/<int:uid>', methods = ['GET'])
def getUserConnections(index, uid):
	iTime = time.time()

	# init objects
	queryUser = Connections.User(uid)
	gc = Connections.GraphApi(host, port, index)

	queryUser.set1and2dConn(gc)
	queryUser.set3dConn(gc)
	# conn3d = newUser.get1stFromList(conn2d, excludes = conn1d)

	fTime = time.time()
	str1st = 'Num 1st degree Connections: {}'.format(len(queryUser.conn1d))
	str2nd = 'Num 2nd degree Connections: {}'.format(len(queryUser.conn2d))
	str3rd = 'Num 3rd degree connections: {}'.format(len(queryUser.conn3d))
	return '{} \n{} \n{} \nTook {}s'.format(str1st, str2nd, str3rd, (fTime - iTime))


if __name__ == '__main__':
	app.run()