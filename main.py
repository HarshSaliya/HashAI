import os

from langchain_text_splitters import RecursiveCharacterTextSplitter
import pdfplumber

from sentence_transformers import SentenceTransformer
import psycopg
from dotenv import load_dotenv
from pgvector.psycopg import register_vector
# from pgvector import Pg

load_dotenv()

file_path = "/home/harsh-saliya/python project/HashAi/media/Harsh_Saliya_Portfolio.pdf"

with pdfplumber.open(file_path) as pdf:
    for page in pdf.pages:
        # print(page.extract_text())
        # print(page.extract_tables())
        pass


text = """
Harsh Saliya
Software Engineer — Backend & Retrieval Systems
About
Backend is where I do my best thinking. I'm a Software Engineer with 2 years building backend systems in
Django, PostgreSQL and AWS Lambda. I design the data model, the API surface and the pipeline that feeds
them, then tune the whole thing until it holds up under real load.
Lately that's extended into retrieval. I build RAG pipelines on Qdrant and pgvector that route a plain-English
question to either vector search or generated SQL — so PDFs and spreadsheets can answer for themselves.
My day job is fintech: REST APIs for lending and transaction workflows, ETL pipelines on AWS Glue, invoice
and revenue automation, and PostgreSQL queries tuned with indexing and join strategy until slow endpoints
run 80–90% faster.
Skills
Languages: Python, SQL
Backend: Django, Django REST Framework, REST API Design, Serverless Architecture
Databases: PostgreSQL, MongoDB, SQLite3, Qdrant, pgvector
AWS & Cloud: AWS Lambda, API Gateway, Amazon S3, AWS Glue, CloudWatch
AI / Retrieval: RAG, LangChain, Embeddings
Tooling: Docker, Git, GitHub, Postman
Operating Systems: Linux, Windows
Experience
Software Engineer — Lambda Logs
Jan 2025 – Present (Internship: Jan 2025 – Apr 2025 · Full-time: Apr 2025 – Present)
Project: MoneyClub
(cid:127) Built REST APIs on AWS Lambda and API Gateway for lending and transaction workflows.
(cid:127) Refactored logic and tuned PostgreSQL queries, cutting response times on slow endpoints by around 60%.
(cid:127) Automated invoice generation and daily revenue reporting with AWS Glue ETL pipelines.
(cid:127) Migrated legacy PHP modules to Python/Django, keeping loans, repayments and transactions consistent in
production.
Project: HRMS
(cid:127) Built a complete HRMS backend covering employees, payroll and leave.
(cid:127) Designed and implemented REST APIs end-to-end in Django REST Framework with PostgreSQL.
(cid:127) Handled role-based permissions so admin, HR and employee each get their own level of access.
(cid:127) Kept clean architecture throughout — structured model design, serializers and migrations stayed
maintainable as the system grew.
Projects
DocsAi — Document Q&A RAG system
[]
github.com/HarshSaliya/DocsAi
(cid:127) Flask backend with a Streamlit frontend for question-answering over uploaded documents.
(cid:127) Qdrant for vector search and sentence-transformers for embeddings, with the Groq API handling
generation.
CareerGo — Job Portal
College project · Django
(cid:127) Job seekers can browse listings and apply; companies and HR can post openings.
(cid:127) ATS-style resume scoring to screen applicants against job requirements.
Travello — Travel Package Booking
College project · Django
(cid:127) Users can browse and book travel packages end-to-end.
Education
Master of Computer Applications (MCA) — LJ University
2023 – 2025
Bachelor of Computer Applications (BCA) — Gujarat University, Ahmedabad
2020 – 2023
[]"""

text = text.replace("(cid:127)", "-").replace("\n[]", "")

# text_splilter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)

# chunks = text_splilter.split_text(text)

# print("RES ::::",chunks)
model = SentenceTransformer("BAAI/bge-m3")


vec = model.encode("Hii what this ?")
print(vec)

# data = embedding.embed_documents(chunks)

# print("AFTER EMBEDIING ::: ------------->", len(data), "vectors of", len(data[0]))


# with psycopg.connect(os.getenv("DATABASE_URL")) as conn:
#     register_vector(conn)

#     conn.execute("DELETE FROM resume_chunks")

#     with conn.cursor() as cur:
#         cur.executemany(
#             "INSERT INTO resume_chunks (content, embedding) VALUES (%s, %s)",
#             list(zip(chunks, data)),
#         )

#     count = conn.execute("SELECT count(*) FROM resume_chunks").fetchone()[0]

# print("SAVED ::: rows in table =", count)


# with psycopg.connect(os.getenv("DATABASE_URL")) as conn:
#     # register_vector(register_vector)
    
#     result = conn.execute("SELECT * from resume_chunks;").fetchone()
    

# print("RES:::", result)pip install sentence-transformers

# query_fetch = SentenceTransformer(model_name="BAAI/bge-m3")
# vec = query_fetch.embed_query("what the designation ?")
# print(vec)
# query = ("what the designation ?")

# result = query_fetch.similarity_search()