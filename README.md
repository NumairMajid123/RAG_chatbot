RAG Chatbot
This project is designed to build a Retrieval-Augmented Generation (RAG) chatbot that answers questions based on content extracted from Confluence pages. It uses web scraping to collect the data, generates vector embeddings, stores them in a FAISS vector store, and finally performs a semantic search to retrieve relevant information for response generation.

Project Workflow
Step 1: Scraping Confluence Pages
The process begins with scraping Confluence content using a Python script. This script uses the BeautifulSoup library to parse HTML pages and extract meaningful text and content from the Confluence documentation. All the extracted information is saved in a structured JSON file. This file acts as the base dataset for the next stages of the pipeline.

Step 2: Embedding Generation and Storage
Once the data is scraped and saved in JSON format, another script processes this file to generate vector embeddings. These embeddings represent the semantic meaning of each document or section. The embeddings are then stored in a FAISS vector store, which allows for fast and efficient similarity searches later on.

Step 3: Retrieval-Augmented Generation (RAG)
When a user submits a query, the system converts that query into an embedding using the same embedding model. It then performs a similarity search in the FAISS vector store to retrieve the most relevant pieces of content from the Confluence data. The top-matching results are returned directly to the user.

Tools and Libraries Used
BeautifulSoup for HTML parsing and scraping Confluence content

JSON as the format for storing the scraped data

Embedding Models (hugging face sentence trannsformer)to convert text into vector representations

FAISS (Facebook AI Similarity Search) to store and search vector embeddings


Summary
This project creates an intelligent chatbot that leverages both document retrieval and generative AI to provide accurate answers based on a custom knowledge base. By combining scraping, embeddings, and vector search, it enables efficient and scalable access to internal documentation like Confluence pages.

demo link: https://drive.google.com/file/d/1WKdbjQW1jklUIdTxacQONMjOep-c59Yg/view
