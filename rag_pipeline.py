from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
import os
from dotenv import load_dotenv
import re
import ollama

def clean_text(text):
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"\n", " ", text)
    return text.strip()


def answer_question_from_pdf(doc_path, question):

    load_dotenv()
    token = os.getenv('HUGGINGFACEHUB_API_TOKEN')

    reader = PdfReader(doc_path)
    text = ''.join([page.extract_text() or '' for page in reader.pages])

    text = clean_text(text)

    splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=20)
    chunks = splitter.split_text(text)

    embeddings = HuggingFaceEmbeddings(model_name='all-MiniLM-L6-v2')
    db = FAISS.from_texts(chunks, embedding=embeddings)

    query = question
    docs = db.similarity_search(query, k=8)
    context = '\n\n'.join([doc.page_content for doc in docs])

    
    prompt = (
        "You are a helpful assistant. Use the following document excerpts to answer the question as clearly as possible.\n\n"
        f"Document:\n{context}\n\n"
        f"Question: {question}\n\n"
        "Answer:"
    )

    response = ollama.generate(model='gemma3', prompt=prompt)
    answer = response['response'].strip()

   

    return answer


if __name__ == '__main__':
    answer = answer_question_from_pdf(r"C:\Users\tlext\Desktop\MASTERS\DISSERTATION\2498906.pdf", "What is this document about?")
    print('Answer:', answer)



