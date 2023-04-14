from elasticsearch import Elasticsearch

# Connect to Elasticsearch running on localhost
es = Elasticsearch()

# Create an index
es.indices.create(index='table1')

# Index a document
for i in range(100):
    doc = {'title': 'My First Document', 'content': f'This is the content {i} of my first document.'}
    es.index(index='my_index', doc_type='doc', body=doc)

# Search for documents
search_results = es.search(index='table1', body={'query': {'match': {'content': 'content'}}})
print(search_results)
