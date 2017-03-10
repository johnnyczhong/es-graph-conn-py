# Connections.py
import json
import urllib.request
import random
import time
random.seed()

esIndex = "prod"
esDoctype = "user"
host = 'localhost'
port = '9200'
timeout = 5000 
sampleSize = 2000000 # population count
returnSize = 200000 # max data points to return
testId = random.randint(0, sampleSize)


class User:
	def __init__(self, uid):
		self.uid = uid
		self.conn1d = None
		self.conn2d = None
		self.conn3d = None

	def set1and2dConn(self, graphConn):
		resp = graphConn.makeRequest((self.uid,), 2)
		connections = graphConn.parseVertices(resp)
		self.conn1d = connections['uid'] 
		self.conn2d = connections['conn']

	def set3dConn(self, graphConn):
		resp = graphConn.makeRequest(self.conn2d, 1, excludes = self.conn1d)
		connections = graphConn.parseVertices(resp)
		self.conn3d = connections['conn']


class GraphApi:
	def __init__(self, host, port, index):
		self.reqEndpoint = 'http://{0}:{1}/{2}/_graph/explore'.format(host, port, index)
		# self.reqHeaders = {'Content-Type': 'application/json'}

	def buildReqBody(self, uidList, degree, excludes = None):
		strList = [str(x) for x in uidList]

		# testing with terminal value
		# if excludes:
		# 	excludes = excludes + [-1]
		# else:
		# 	excludes = [-1]

		# remove false positives (looping back to self)
		if not excludes:
			excludes = [-1]

		# 1st degree = connections
		if degree is 1:
			spiderOrigin = 'uid'
		# 2nd degree = connections of connections
		elif degree is 2:
			spiderOrigin = 'conn'

		reqBody = {
		    "controls" : {
		    	"use_significance" : False,
				"sample_size" : returnSize,
				"timeout" : timeout
			},
			"vertices" : [
				{
		            "field" : spiderOrigin,
		            "include" : strList,
		            "shard_min_doc_count" : 1,
		            "min_doc_count" : 1,
		            "size" : returnSize
				}
			],
		    "connections" : {
		        "vertices" : [
		            {
		                "field" : "conn",
		                "exclude" : excludes,
		                "size" : returnSize,
		                "shard_min_doc_count" : 1,
		                "min_doc_count" : 1
		            },
			        {
			            "field": "uid",
			            "size": returnSize,
			            "shard_min_doc_count": 1,
			            "min_doc_count": 1
			        }
		        ]
		    }
		}

		return reqBody


	# purpose: interface to elasticsearch graph endpoint
	def makeRequest(self, uidList, degree, excludes = None):
		reqBody = self.buildReqBody(uidList, degree, excludes)

		jsonEncodedBody = json.dumps(reqBody)
		bytesEncodedBody = jsonEncodedBody.encode('utf-8')

		resp = urllib.request.urlopen(self.reqEndpoint, data=bytesEncodedBody)
		respContent = json.loads(resp.read().decode())

		return respContent



	# purpose: returns connections that are not self
	def parseVertices(self, resp):
		vertices = resp['vertices']
		connections = {
			'uid' : [],
			'conn' : []
		}
		# list of dicts
		for i in vertices:
			if i['depth'] != 0:
				if i['field'] == 'uid':
					connections['uid'].append(i['term'])
				elif i['field'] == 'conn':
					connections['conn'].append(i['term'])
		return connections
	

def main():
	# todo: pass query params as args via cmdline

	initTime = time.time()
	print('userId: {}'.format(testId))

	newUser = User(testId)
	gc = GraphApi(host, port, esIndex)

	newUser.set1and2dConn(gc)
	newUser.set3dConn(gc)

	# print('Num 1st degree Connections: {}'.format(len(newUser.conn1d)))
	print('1st degree Connection: {}'.format(newUser.conn1d[10]))
	# print('Num 2nd degree Connections: {}'.format(len(newUser.conn2d)))
	print('2nd degree Connection: {}'.format(newUser.conn2d[10]))
	# print('Num 3rd degree connections: {}'.format(len(newUser.conn3d)))
	print('3rd degree Connection: {}'.format(newUser.conn3d[10]))

	finalTime = time.time()

	print('Elapsed Time: {}'.format(finalTime - initTime))

if __name__ == '__main__':
	main()