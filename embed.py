from langchain_huggingface import HuggingFaceEmbeddings

embedding = HuggingFaceEmbeddings(model_name="BAAI/bge-m3")
embedding.embed_query("test")

print("OP::::::::::",embedding)

