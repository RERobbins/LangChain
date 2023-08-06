import argparse
import os
import shutil
import openai

from dotenv import load_dotenv, find_dotenv
from langchain.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings

from langchain.vectorstores import Chroma

load_dotenv(find_dotenv())
openai.api_key = os.environ["OPENAI_API_KEY"]


def main():
    parser = argparse.ArgumentParser(
        description="Create OpenAI embedding vector database from source directory."
    )
    parser.add_argument("source_directory", help="Path to the source directory")
    parser.add_argument("vector_directory", help="Path to the vector directory")
    parser.add_argument(
        "--chunk_size", type=int, default=1500, help="Chunk size (default: 1500)"
    )
    parser.add_argument(
        "--chunk_overlap", type=int, default=150, help="Chunk overlap (default: 150)"
    )

    args = parser.parse_args()
    source_directory = args.source_directory
    vector_directory = args.vector_directory
    chunk_size = args.chunk_size
    chunk_overlap = args.chunk_overlap

    print(f"{source_directory=}\n{vector_directory=}\n{chunk_size=}\n{chunk_overlap=}")

    loader = DirectoryLoader(source_directory, show_progress=True)
    docs = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap
    )
    splits = text_splitter.split_documents(docs)

    embeddings = OpenAIEmbeddings()

    try:
        shutil.rmtree(vector_directory)
    except FileNotFoundError:
        pass

    vectordb = Chroma.from_documents(
        documents=splits, embedding=embeddings, persist_directory=vector_directory
    )
    print(f"Embedding count={vectordb._collection.count()}")


if __name__ == "__main__":
    main()
