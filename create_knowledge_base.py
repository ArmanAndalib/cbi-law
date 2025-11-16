import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

def create_knowledge_base():
    """
    Create vector database from the manually inputted law text
    """
    print("🧠 Creating knowledge base...")
    
    # Check if law text file exists
    if not os.path.exists('persian_law.txt'):
        print("❌ Error: persian_law.txt not found!")
        print("Please run manual_input.py first to create the law text file.")
        return None
    
    # Read the law text
    with open('persian_law.txt', 'r', encoding='utf-8') as f:
        law_text = f.read()
    
    print(f"📖 Read {len(law_text)} characters from law text")
    
    if len(law_text.strip()) == 0:
        print("❌ Error: The law text file is empty!")
        return None
    
    # Initialize embedding model for Persian
    print("🔧 Loading embedding model...")
    try:
        embedding_model = HuggingFaceEmbeddings(
            model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
        )
    except Exception as e:
        print(f"❌ Error loading embedding model: {e}")
        return None
    
    # Initialize text splitter optimized for legal text
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,  # Good for legal paragraphs
        chunk_overlap=100,
        separators=["\n\n", "\n", ". ", "? ", "! ", "۔ ", "؟ ", "! ", " ", ""]
    )
    
    # Split the document into chunks
    print("✂️ Splitting text into chunks...")
    chunks = text_splitter.split_text(law_text)
    print(f"📚 Created {len(chunks)} text chunks")
    
    if len(chunks) == 0:
        print("❌ Error: No chunks were created from the text!")
        return None
    
    # Create vector store
    print("💾 Creating vector database...")
    try:
        vector_store = Chroma.from_texts(
            texts=chunks,
            embedding=embedding_model,
            metadatas=[{"source": "persian_law", "chunk_id": i} for i in range(len(chunks))],
            persist_directory="./persian_law_db",
            collection_name="persian_laws"
        )
        
        print("✅ Knowledge base created successfully!")
        return vector_store
        
    except Exception as e:
        print(f"❌ Error creating vector database: {e}")
        return None

if __name__ == "__main__":
    create_knowledge_base()