from insight_worker.rag import embed


def test_embedding():
    embeddings = list(embed(["This is a test string"]))

    assert len(embeddings[0]) == 1536
