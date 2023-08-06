import argparse
import os
import openai
import textwrap

from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA, ConversationalRetrievalChain
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate

from dotenv import load_dotenv, find_dotenv
from pathlib import Path

load_dotenv(find_dotenv())
openai.api_key = os.environ["OPENAI_API_KEY"]

def main():
    parser = argparse.ArgumentParser(description="Chat with vector database.")
    parser.add_argument("vector_directory", help="Path to the vector directory")

    args = parser.parse_args()
    vector_directory = args.vector_directory

    embeddings = OpenAIEmbeddings()
    vectordb = Chroma(persist_directory=vector_directory, embedding_function=embeddings)
    
    llm_model_name = "gpt-3.5-turbo"
    #llm_model_name = "gpt-4"

    llm = ChatOpenAI(model_name=llm_model_name, temperature=0)
    retriever = vectordb.as_retriever(search_type="mmr", search_kwargs={"k":5})
    
    QUESTION_PROMPT = PromptTemplate.from_template("""Given the following conversation and a follow up question, rephrase the follow up question to be a standalone question.

        Chat History:
        {chat_history}
        Follow Up Input: {question}
        Standalone question:""")
    
    qa = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        condense_question_prompt=QUESTION_PROMPT,
        return_source_documents=True,
        verbose=False)
    
    chat_history = []
    
    while True:
        query = input('you: ')
        
        if query == 'quit':
            break
            
        if query == 'clear':
            chat_history = []
            continue
            
        chat_history = ask_question_with_context(qa, query, chat_history)


def ask_question_with_context(qa, question, chat_history):
    result = qa({"question": question, "chat_history": chat_history})
    print(f"\n{textwrap.fill(result['answer'])}\n")
    
    source_paths = set([document.metadata['source'] for document in result['source_documents']])
    source_names = [Path(path).name for path in source_paths]
    print (f"Sources: {source_names}")
    
    chat_history = [(question, result["answer"])]
    return chat_history

if __name__ == "__main__":
    main()