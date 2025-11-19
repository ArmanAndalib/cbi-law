from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings

# --- Initialize embedding model ---
self_embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)

# --- Initialize vector store (old style, works with your DB) ---
try:
    vector_store = Chroma(
        persist_directory="./persian_law_db",
        embedding_function=self_embedding_model,
        collection_name="persian_laws"
    )
except Exception as e:
    print(f"❌ Error loading vector database: {e}")
    raise e

# --- Load GPT2 Persian model ---
model_path = "D:/projects/OfflineChatbot/gpt2-fa"
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForCausalLM.from_pretrained(model_path)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# --- RAG query function ---
def rag_query(query, top_k=3):
    # Retrieve top-k docs from Chroma
    results = vector_store.similarity_search(query, k=top_k)
    retrieved_texts = [doc.page_content for doc in results]

    # Concatenate retrieved docs as context
    context = "\n".join(retrieved_texts)
    prompt = f"سوال: {query}\nمتن مرتبط:\n{context}\nپاسخ به فارسی:"

    # Tokenize & truncate
    inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=512).to(device)

    # Generate response
    output_ids = model.generate(
        **inputs,
        max_new_tokens=150,
        do_sample=True,
        temperature=0.7,
        top_p=0.9
    )

    # Decode
    answer = tokenizer.decode(output_ids[0], skip_special_tokens=True)
    return answer

# --- Simple CLI test ---
if __name__ == "__main__":
    while True:
        q = input("Question: ")
        if q.strip().lower() in ["exit", "quit"]:
            break
        print("Answer:", rag_query(q))
