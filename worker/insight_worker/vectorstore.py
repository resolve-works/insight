import os
import logging
from llama_index import VectorStoreIndex
from llama_index.vector_stores import PGVectorStore
from llama_index.schema import TextNode, NodeRelationship, RelatedNodeInfo


vector_store = PGVectorStore.from_params(
    connection_string=os.environ.get("POSTGRES_URI"),
    port=5432,
    schema_name="private",
    table_name="page",
    perform_setup=False,
    embed_dim=1536,
)

vector_store_index = VectorStoreIndex.from_vector_store(vector_store)


def store_embeddings(pages):
    nodes = [
        TextNode(text=page["contents"], id_=f"{page['file_id']}_{page['index']}")
        for page in pages
    ]
    for previous, current in zip(nodes[0:-1], nodes[1:]):
        previous.relationships[NodeRelationship.NEXT] = RelatedNodeInfo(
            node_id=current.node_id
        )
        current.relationships[NodeRelationship.PREVIOUS] = RelatedNodeInfo(
            node_id=previous.node_id
        )
    vector_store_index.insert_nodes(nodes)


def answer_prompt(id, query):
    query_engine = vector_store_index.as_query_engine()
    response = query_engine.query(query)
    logging.info(f"query: {query}")
    logging.info(f"response: {response}")
