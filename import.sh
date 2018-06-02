cd src/data
sudo cp edges.csv nodes.csv /var/lib/neo4j/import
cd /usr
sudo bin/neo4j-admin import --ignore-missing-nodes true --nodes /var/lib/neo4j/import/nodes.csv --relationships /var/lib/neo4j/import/edges.csv