import psycopg2
from pathlib import Path
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('all-MiniLM-L6-v2')
print(f"Script is starting\n")
pdf_directory = Path("/root/pdf")
conn = psycopg2.connect( host="localhost", dbname="iadb", user="ia", password="Oracle.1989", port=5432)
cur = conn.cursor()
for pdf_path in pdf_directory.glob("*.pdf"):
    print(f"--- Processing: {pdf_path.name} ---")
    reader = PdfReader(pdf_path)
    doc_name = pdf_path.name
    text_chunks = []
    for idx, page in enumerate(reader.pages):
        text = page.extract_text()

        if not text.strip():
            continue
        clean_text = text.replace('\x00', '').strip()
        embedding = model.encode(clean_text).tolist()
        cur.execute("""
            INSERT INTO internal_procs (document_name, segment_id, contents, embedding)
            VALUES (%s, %s, %s, %s);
            """,
            (doc_name, idx + 1, clean_text, embedding)
        )
conn.commit()
cur.close()
conn.close()
print("PDF fully parsed and vectorized successfully!")



