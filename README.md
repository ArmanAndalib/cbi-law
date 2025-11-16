🎯 What This Project Does

It's a smart chatbot that can answer questions about Persian laws in Farsi. You ask questions about laws, and it gives you accurate answers based on actual legal texts.
🏗️ Project Structure - 4 Main Parts
1. Data Collection (manual_input.py)

What it does: Gets the law text into the system

    You copy-paste Persian law text into the program

    It saves the text to a file called persian_law.txt

    Think of it like: Scanning a law book into the computer

2. Knowledge Base (create_knowledge_base.py)

What it does: Makes the law text "understandable" to the AI

    Takes the law text and breaks it into small chunks (like cutting a book into paragraphs)

    Converts each chunk into numbers (called "embeddings") that computers can understand

    Stores these numbered chunks in a special database

    Think of it like: Creating a super-smart index for the law book

3. Brain (law_chatbot.py)

What it does: The actual AI that answers questions

    When you ask a question, it searches the knowledge base for relevant law sections

    Sends your question + relevant laws to Groq AI (like ChatGPT but faster)

    Gets the answer back and shows it to you

    Think of it like: A very smart lawyer who instantly reads all relevant laws to answer your question

4. User Interface (app.py)

What it does: The website you interact with

    Creates a nice web page where you can type questions

    Shows the conversation history

    Displays answers in proper Persian (right-to-left)

    Think of it like: A chat window specifically for legal questions

🔧 How the Magic Happens - Step by Step
Step 1: You Ask a Question

Example: "What are the penalties for fraud?"
Step 2: Smart Search

    The system searches through all the law chunks

    Finds the most relevant sections about fraud penalties

    Like: Using Ctrl+F but much smarter - it understands meaning, not just words

Step 3: AI Processing

    Sends your question + relevant law texts to Groq AI

    The AI reads both and writes a perfect answer in Persian

    Like: Giving a human assistant the question and the relevant law pages to formulate an answer

Step 4: You Get Answer

    Shows you a clear, well-written answer in Persian

    Tells you which laws were used for the answer

🛠️ Technical Components Explained Simply
Vector Database

    What: Special storage that understands meaning

    Why: Regular databases only find exact word matches. Vector databases find similar meanings.

    Example: If you search "car accident," it will also find "vehicle collision"

Embeddings

    What: Converting text to numbers that represent meaning

    Why: Computers understand numbers better than words

    Example: "Law" might become [0.1, 0.5, -0.3] and "Legal" becomes [0.12, 0.48, -0.28] (very similar!)

Groq AI

    What: A very fast AI service

    Why: It's optimized for speed and works well with Persian language

    Alternative: Could use OpenAI (ChatGPT) but Groq is faster and free

RTL Support

    What: Right-to-Left text display

    Why: Persian/Arabic languages read from right to left

    How: Special CSS styling makes everything display correctly

📁 File by File Purpose

    manual_input.py - Get law text from you

    persian_law.txt - Store the law text

    create_knowledge_base.py - Process law text for AI

    law_chatbot.py - The AI brain that answers questions

    app.py - The web interface

    persian_law_db/ - The processed law database (created automatically)

🔄 Workflow - How to Use

    Setup: Run manual_input.py → paste law text

    Process: Run create_knowledge_base.py → creates AI-ready database

    Use: Run app.py → opens web interface → ask questions

🎪 Real-World Analogy

Think of this system like a super-efficient legal research team:

    You (the user) = Client with legal questions

    Vector Database = Team of paralegals who instantly find relevant law sections

    Groq AI = Senior lawyer who reads the laws and writes the answer

    Streamlit UI = Your meeting room where conversations happen

    Persian Law Text = The law library

When you ask "What are my rights as an employee?":

    Paralegals (vector database) quickly find employment law sections

    Senior lawyer (Groq AI) reads them and writes a clear answer

    You get the answer in your meeting room (web interface)

💡 Key Benefits

    Fast: Gets answers in seconds instead of hours of research

    Accurate: Based on actual law texts, not opinions

    Accessible: Anyone can ask legal questions without legal training

    Persian-native: Works perfectly with Farsi language

    Free: Uses free AI services

This is essentially a legal research assistant that makes understanding laws as easy as having a conversation!
