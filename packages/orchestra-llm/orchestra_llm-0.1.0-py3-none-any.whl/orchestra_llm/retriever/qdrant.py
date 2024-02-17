from langchain_community.vectorstores import Qdrant
from qdrant_client import QdrantClient

class QDrantVectorDB:

    def __init__(self, host, port, collection_name, embeddings):
        self.embeddings = embeddings
        self.collection_name = collection_name
        self.host = host
        self.port = port
        self.client = QdrantClient(self.host, port=self.port)


    def search(self, query:str):
        """
        Searches for relevant documents based on the given query.

        Args:
            query (str): The query string used for searching.

        Returns:
            list: A list of relevant documents.
        """
        vector_store = Qdrant(
            client=self.client,
            collection_name = self.collection_name,
            embeddings = self.embeddings
        )
        retriever = vector_store.as_retriever()
        relevant_documents = retriever.get_relevant_documents(query)
        return relevant_documents

    def get_retriever(self, k=5, **kwargs):
        vector_store = Qdrant(
            client=self.client,
            collection_name = self.collection_name,
            embeddings = self.embeddings
        )
        retriever = vector_store.as_retriever(search_kwargs={"k": k})
        return retriever
    
    def from_documents(self, docs):
        """
        Generate a vector store from a list of documents.

        Parameters:
            docs (list): A list of documents.

        Returns:
            vector_store (Qdrant): The generated vector store.
        """
        vector_store = Qdrant.from_documents(
            docs, 
            self.embeddings, 
            url=self.host, 
            prefer_grpc=True, 
            collection_name = self.collection_name
        )
        return vector_store