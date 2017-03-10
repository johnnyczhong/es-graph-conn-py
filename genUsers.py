# generate and store 2 million dummy users into ES

from elasticsearch import Elasticsearch, helpers
import genNodes

DEBUG = True

es = Elasticsearch(['http://elastic:changeme@localhost:9200']) # es instance

numUsers = 2000000
numEdges = 20000000

esIndex = 'prod'
esType = 'user'


def main():
	if DEBUG:
		print('starting main')

	# generate nodes and random edges between nodes
	users = [x for x in range(numUsers)]
	graph = genNodes.random_walk(users, numEdges)

	# create user docs with base data
	userList = numUsers * [None]
	for i in range(numUsers):
		userList[i] = {
			'_op_type' : 'index',
			'_index' : esIndex,
			'_type' : esType,
			'_id' : i,
			'_source' : {
				'uid' : i,
				'conn' : []
			}
		}

    # graph.edges is list of edges (tuple of nodes)
    # walk through each edge and add connections to both nodes
	for e in graph.edges:
		left = e[0]
		right = e[1]
		userList[left]['_source']['conn'].append(right)
		userList[right]['_source']['conn'].append(left)

	if DEBUG:
		print('bulk adding records')

	# bulk add all users
	helpers.bulk(es, userList)

	# finish with refresh to make searchable
	es.indices.refresh(index = esIndex)


if __name__ == '__main__':
	main()