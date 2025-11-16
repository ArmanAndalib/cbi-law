import os
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from groq import Groq

class PersianLawChatbot:
    def __init__(self):
        print("🚀 Initializing Persian Law Chatbot...")
        
        # Check if knowledge base exists
        if not os.path.exists("./persian_law_db"):
            print("❌ Knowledge base not found!")
            print("Please run create_knowledge_base.py first.")
            return
        
        # Initialize embedding model
        try:
            self.embedding_model = HuggingFaceEmbeddings(
                model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
            )
        except Exception as e:
            print(f"❌ Error loading embedding model: {e}")
            return
        
        # Initialize vector store
        try:
            self.vector_store = Chroma(
                persist_directory="./persian_law_db",
                embedding_function=self.embedding_model,
                collection_name="persian_laws"
            )
        except Exception as e:
            print(f"❌ Error loading vector database: {e}")
            return
        
        # Initialize Groq client
        try:
            self.groq_client = Groq(api_key=self.get_groq_api_key())
            self.available_models = self.get_available_models()
        except Exception as e:
            print(f"❌ Error initializing Groq client: {e}")
            return
        
        self.chat_history = []
        print("✅ Chatbot ready!")
    
    def get_groq_api_key(self):
        """Get Groq API key from environment or user input"""
        api_key = os.getenv("GROQ_API_KEY")
        if api_key:
            return api_key
        
        print("\n🔑 Groq API Key Setup:")
        print("1. Go to: https://console.groq.com/")
        print("2. Sign up for free account")
        print("3. Create API key")
        print("4. Enter your key below:")
        
        api_key = input("Enter your Groq API key: ").strip()
        
        if not api_key:
            print("❌ No API key provided!")
            return None
        
        # Save to environment for future use
        os.environ["GROQ_API_KEY"] = api_key
        print("✅ API key saved!")
        return api_key
    
    def get_available_models(self):
        """Get list of available Groq models"""
        try:
            models = self.groq_client.models.list()
            available_models = [model.id for model in models.data]
            print("🤖 Available Groq models:")
            for model in available_models:
                print(f"   - {model}")
            return available_models
        except Exception as e:
            print(f"⚠️ Could not fetch available models: {e}")
            # Return default models that are typically available
            return [
                "llama-3.1-8b-instant",  # Fast model, good for Persian
                "llama-3.1-70b-versatile",  # More powerful but slower
                "mixtral-8x7b-32768",
                "gemma2-9b-it"
            ]
    
    def select_model(self):
        """Select the best available model for Persian"""
        # Priority list for Persian language support
        preferred_models = [
            "llama-3.1-8b-instant",
            "llama-3.1-70b-versatile", 
            "mixtral-8x7b-32768",
            "gemma2-9b-it",
            "llama3-8b-8192"  # Fallback
        ]
        
        for model in preferred_models:
            if model in self.available_models:
                print(f"✅ Selected model: {model}")
                return model
        
        # If no preferred models available, use the first available one
        if self.available_models:
            selected = self.available_models[0]
            print(f"⚠️ Using available model: {selected}")
            return selected
        
        # Fallback
        print("⚠️ Using default model: llama-3.1-8b-instant")
        return "llama-3.1-8b-instant"
    
    def find_relevant_context(self, question, k=4):
        """Find relevant law sections for the question"""
        try:
            docs = self.vector_store.similarity_search(question, k=k)
            context = "\n\n".join([doc.page_content for doc in docs])
            sources = list(set([doc.metadata.get('source', 'Unknown') for doc in docs]))
            return context, sources
        except Exception as e:
            print(f"Error searching database: {e}")
            return "", []
    
    def ask_question(self, question):
        """Ask a question about Persian law"""
        if not question.strip():
            return "لطفاً یک سوال معتبر مطرح کنید.", []
        
        print("🔍 Searching in legal database...")
        context, sources = self.find_relevant_context(question)
        
        if not context:
            return "متاسفانه اطلاعات مرتبطی در پایگاه داده قوانین یافت نشد. لطفاً سوال خود را به شکل دیگری مطرح کنید.", []
        
        # Select the best available model
        model_name = self.select_model()
        
        # Enhanced system prompt in Persian
        system_prompt = """
        شما یک دستیار حقوقی هوشمند و متخصص در قوانین ایران هستید. وظیفه شما پاسخ به سوالات حقوقی بر اساس متون قانونی ارائه شده است.

        دستورالعمل های مهم:
        1. همیشه به زبان فارسی روان و ساده پاسخ دهید
        2. پاسخ های خود را مستقیماً بر اساس متن قانونی ارائه شده (Context) بنا کنید
        3. در صورت لزوم، توضیح مختصر و مفیدی ارائه دهید
        4. اگر پاسخ در متن موجود نیست، صادقانه بگویید: "پاسخ این سوال در متون قانونی موجود یافت نشد."
        5. از ساختار منظم استفاده کنید اما بیش از حد رسمی نباشید
        6. در پاسخ به موارد حقوقی، دقت و احتیاط را رعایت کنید
        7. در صورت اشاره به مواد قانونی، شماره ماده را ذکر کنید

        متن قانونی مرتبط:
        {context}
        """
        
        formatted_system_prompt = system_prompt.format(context=context)
        
        try:
            print(f"🤖 Generating answer with {model_name}...")
            # Get response from Groq
            chat_completion = self.groq_client.chat.completions.create(
                messages=[
                    {
                        "role": "system", 
                        "content": formatted_system_prompt
                    },
                    {
                        "role": "user", 
                        "content": f"سوال: {question}"
                    }
                ],
                model=model_name,
                temperature=0.3,
                max_tokens=1024,
                top_p=0.9
            )
            
            answer = chat_completion.choices[0].message.content
            
            # Update chat history
            self.chat_history.append({
                "question": question, 
                "answer": answer,
                "sources": sources,
                "model_used": model_name
            })
            
            return answer, sources
            
        except Exception as e:
            error_msg = f"خطا در ارتباط با سرویس هوش مصنوعی: {str(e)}"
            print(f"❌ API Error: {e}")
            return error_msg, []

def main():
    print("🤖 PERSIAN LAW CHATBOT")
    print("=" * 50)
    
    try:
        chatbot = PersianLawChatbot()
        
        # Check if chatbot initialized successfully
        if not hasattr(chatbot, 'groq_client') or chatbot.groq_client is None:
            print("❌ Chatbot initialization failed!")
            return
        
        print("\n🎯 Ready to answer your law questions!")
        print("💡 Example questions:")
        print("   - 'مفاد اصلی این قانون چیست؟'")
        print("   - 'شرایط و ضوابط این قانون چه مواردی هستند؟'")
        print("   - 'مجازات های پیش بینی شده در این قانون چیست؟'")
        print("\nبرای خروج 'خروج' تایپ کنید")
        print("=" * 50)
        
        while True:
            try:
                user_question = input("\n🧑‍💼 شما: ").strip()
                
                if user_question.lower() in ['خروج', 'exit', 'quit', 'q']:
                    print("خدانگهدار! 👋")
                    break
                
                if not user_question:
                    continue
                
                answer, sources = chatbot.ask_question(user_question)
                
                print(f"\n🤖 ربات: {answer}")
                if sources:
                    print(f"📚 منابع: {sources}")
                print(f"💬 ({len(chatbot.chat_history)} سوال در این نشست)")
                    
            except KeyboardInterrupt:
                print("\n\nخدانگهدار! 👋")
                break
            except Exception as e:
                print(f"خطای غیرمنتظره: {e}")
                
    except Exception as e:
        print(f"خطا در راه اندازی ربات: {e}")

if __name__ == "__main__":
    main()