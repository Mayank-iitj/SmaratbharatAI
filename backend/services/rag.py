import os
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document

# In-memory store for demonstration
_vector_store = None

def get_embeddings():
    return HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

def init_vector_store():
    """Initializes the FAISS in-memory vector store with seed data."""
    global _vector_store
    
    docs = [
        Document(page_content="PM Kisan Samman Nidhi: Income support of Rs. 6000/- per year to all landholding farmer families.", metadata={"id": 1}),
        Document(page_content="Stand-Up India Scheme: Facilitates bank loans between 10 lakh and 1 Crore to at least one SC/ST borrower and at least one woman borrower.", metadata={"id": 2}),
        Document(page_content="Pradhan Mantri Awas Yojana (PMAY): Housing for all scheme providing subsidies for building homes for lower income groups.", metadata={"id": 3}),
        Document(page_content="Sukanya Samriddhi Yojana: Small deposit scheme for the girl child launched as a part of the Beti Bachao Beti Padhao campaign.", metadata={"id": 4}),
        Document(page_content="Post Matric Scholarship for Minorities: Financial assistance to meritorious students belonging to minority communities to pursue higher education.", metadata={"id": 5})
    ]
    
    embeddings = get_embeddings()
    _vector_store = FAISS.from_documents(docs, embeddings)
    print("Vector store initialized with seed schemes.")

def search_schemes(query: str, k: int = 2):
    """Searches the vector store for matching schemes."""
    global _vector_store
    if not _vector_store:
        init_vector_store()
    
    try:
        results = _vector_store.similarity_search_with_score(query, k=k)
        return [{"content": doc.page_content, "score": float(score), "metadata": doc.metadata} for doc, score in results]
    except Exception as e:
        print(f"Error searching schemes: {e}")
        return []
