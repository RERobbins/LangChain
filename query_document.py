import argparse
import os
import openai

from langchain.document_loaders import UnstructuredFileLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma


from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

from langchain.chat_models import ChatOpenAI
from langchain.chains.question_answering import load_qa_chain


from dotenv import load_dotenv, find_dotenv
from pathlib import Path

load_dotenv(find_dotenv())
openai.api_key = os.environ["OPENAI_API_KEY"]


def main():
    parser = argparse.ArgumentParser(description="Query a document.")
    parser.add_argument("source_document", help="Path to the source document")
    parser.add_argument("query", help="Document related question or task.")
    parser.add_argument(
        "--chunk_size", type=int, default=1500, help="Chunk size (default: 1500)"
    )
    parser.add_argument(
        "--chunk_overlap", type=int, default=150, help="Chunk overlap (default: 150)"
    )

    args = parser.parse_args()
    source_document = args.source_document
    document_query = args.query
    chunk_size = args.chunk_size
    chunk_overlap = args.chunk_overlap

    vectordb = create_vectordb(source_document, chunk_size, chunk_overlap)

    llm_model_name = "gpt-3.5-turbo"
  # llm_model_name = "gpt-4"

    llm = ChatOpenAI(model_name=llm_model_name, temperature=0)

    template = """You are reviewing outside counsel guidelines prepared by an corporation.  Outside Counsel Guidelines 
    have become standard practice in the working relationships between law firms and their corporate clients. 
    These requirements put forth by the corporate client include specific instructions on how law firms 
    should conduct their business when doing legal work for that particular corporate client. Use the following pieces 
    of context to answer the question at the end.   If you don't know the answer, just say that you don't know, don't try 
    to make up an answer.  Keep the answer as concise as possible.  Just provide the answer as a single word or phrase.  If the
    answer is an abbreviation for something that is spelled out in the guidelines, provide the short and longer answers.

        {context}
        Question: {question}
        Answer:"""
    
    QA_CHAIN_PROMPT = PromptTemplate.from_template(template)
    
    retriever = vectordb.as_retriever(search_type="mmr")

    qa_chain = RetrievalQA.from_chain_type(
        llm,
        retriever=retriever,
        chain_type_kwargs={"prompt": QA_CHAIN_PROMPT}
        )
    
    result = qa_chain({"query": document_query})
    print (result["result"])


def create_vectordb(source_document, chunk_size, chunk_overlap):
    loader = UnstructuredFileLoader(source_document)
    docs = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap
    )
    splits = text_splitter.split_documents(docs)
    embeddings = OpenAIEmbeddings()

    return Chroma.from_documents(documents=splits, embedding=embeddings)


if __name__ == "__main__":
    main()
