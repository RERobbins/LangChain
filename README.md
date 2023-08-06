# LangChain
LangChain Sand Box

This is a working repository for various experiments that I am conducting with LangChain.

I use the the `python-dotenv` library to maintain the necessary API keys.

The files that I am using reside in the data subdirectory.

A collection of results from different experiments can be found in the screenshots subdirectory.

The `summarize.py script` is based on https://medium.com/mlearning-ai/building-a-custom-summarization-app-with-streamlit-and-langchain-11ab19099822

The `create_vectordb.py` script can be used to create a Chroma vector database from a source directory. Type `python create_vectordb.py -h` for more information.

The `chat_with_vectordb.py` script takes a path to a directory containing a Chroma vector database and initiates a chat.  You can quit the chat by typing `quit` and start a new conversation by typing `clear`.  The sources relied upon for each answer are included.