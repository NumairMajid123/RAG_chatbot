RAG Chatbot
This project is designed to build a Retrieval-Augmented Generation (RAG) chatbot that answers questions based on content extracted from Confluence pages. It uses web scraping to collect the data, generates vector embeddings, stores them in a FAISS vector store, and finally performs a semantic search to retrieve relevant information for response generation.

Project Workflow
Step 1: Scraping Confluence Pages
The process begins with scraping Confluence content using a Python script. This script uses the BeautifulSoup library to parse HTML pages and extract meaningful text and content from the Confluence documentation. All the extracted information is saved in a structured JSON file. This file acts as the base dataset for the next stages of the pipeline.

Step 2: Embedding Generation and Storage
Once the data is scraped and saved in JSON format, another script processes this file to generate vector embeddings. These embeddings represent the semantic meaning of each document or section. The embeddings are then stored in a FAISS vector store, which allows for fast and efficient similarity searches later on.

Step 3: Retrieval-Augmented Generation (RAG)
The stored FAISS index is used to perform vector-based retrieval. When a user asks a question, the system searches through the vector database to find the most relevant chunks of content. These chunks are retrieved and provided as context to a language model, which then generates an accurate and context-aware answer. This is the core concept behind Retrieval-Augmented Generation.

Tools and Libraries Used
BeautifulSoup for HTML parsing and scraping Confluence content

JSON as the format for storing the scraped data

Embedding Models (hugging face sentence trannsformer)to convert text into vector representations

FAISS (Facebook AI Similarity Search) to store and search vector embeddings


Summary
This project creates an intelligent chatbot that leverages both document retrieval and generative AI to provide accurate answers based on a custom knowledge base. By combining scraping, embeddings, and vector search, it enables efficient and scalable access to internal documentation like Confluence pages.
