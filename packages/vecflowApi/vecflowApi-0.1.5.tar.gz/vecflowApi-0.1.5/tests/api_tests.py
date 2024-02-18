import time
import sys

from vecflowapi.Client import Client

client = Client()
api_list = client.list_api_keys("test@joe.com", "test")
print(api_list)
auth_client = Client(api_list[0])

test_pipeline = auth_client.create_pipeline(
    "test_pipeliin7ew83uu9",
    splitter_args={"chunk_size": 400, "chunk_overlap": 40, "length_function": "len"},
    embedder_args={"api_key": "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"},
    vector_store_args={
        "api_key": "371b67fa-0889-44e1-b538-e66208a6769b",
        "environment": "us-east-1-aws",
        "index": "apis",
    },
)
time.sleep(30)
curr_path = sys.path[0]
test_pipeline.upload(curr_path + "/test.txt")

time.sleep(30)

res = test_pipeline.query(
    "How could recent cases at the Supreme Court affect the internet?",
    llm_config={
        "llm": "TogetherAI",
        "model": "togethercomputer/llama-2-70b-chat",
        "api_key": "28b655a6430d7b94996808735856408a47928a37a1c32f10751fcb6e8bde7805",
        "chat_format": "[]",
    },
    retrieval_method={
        "type": "Simple",
        "dense_search_top_k": 10,
        "reranker_top_k": 5,
        "num_neighbors": 1,
    },
    history=[],
    system_message="You are a friendly assistant.",
)

print(res)
