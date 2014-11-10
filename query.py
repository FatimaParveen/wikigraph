from py2neo import neo4j
import json

def find_shortest_path(node1, node2):

	graph_db = neo4j.GraphDatabaseService()

	query = neo4j.CypherQuery(
		graph_db, 
		"""MATCH (m {node:'%s'}), (n {node:'%s'}), 
		p = shortestPath((m)-[*..20]->(n)) RETURN p""" % (node1, node2)
		)

	path = query.execute_one()
	print "\nShortest Path:"
	print path

	return path

def create_rels_list(path):

	rels_list = []

	for rel in path.relationships:
		start_node = rel.start_node.get_properties()['node']
		end_node = rel.end_node.get_properties()['node']
		rels_list.append({"source": int(start_node), "target": int(end_node)})

	return rels_list

def create_nodes_list(path):

	nodes_list = []

	for a_node in path.nodes:

		node, name = a_node.get_properties().values()
		name = name.replace('_', ' ')
		node = int(node)

		d = {"id": node, "name": name}

		labels = a_node.get_labels()
		label = labels - set(['Page']) # does it have a label other than Page?
		if label:
			d['type'] = list(label)[0]

		nodes_list.append(d)

	# print "\nnode name: %s (%s)" % (name, node)
	# for j in a_node.match(limit=2):
	# 	start_name = j.start_node.get_properties()['name']
	# 	end_name = j.end_node.get_properties()['name']
	# 	print start_name + " also links to", end_name

	return nodes_list

def create_lists(path):

	rels_list = create_rels_list(path)
	nodes_list = create_nodes_list(path)

	codes = {}
	id_counter = 0

	for node in nodes_list:
		node_id = node['id']
		if node_id not in codes:
			codes[node_id] = id_counter
			id_counter += 1
		node['id'] = codes[node_id]

	for rel in rels_list:
		rel['source'] = codes[rel['source']]
		rel['target'] = codes[rel['target']]




	print "\nnodes list:", nodes_list
	print "\nrels list:", rels_list, '\n'
	print '{ "directed": true, "nodes":', json.dumps(nodes_list) + ', "links":', json.dumps(rels_list)+', "multigraph": false }'
	

if __name__ == "__main__":
	path = find_shortest_path('98', '2800')
	create_lists(path)

