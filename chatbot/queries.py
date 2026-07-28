import psycopg
from pgvector.psycopg import register_vector
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('all-MiniLM-L6-v2')

def query_response(question):
    #conn = psycopg2.connect( host="localhost", dbname="iadb", user="ia", password="Oracle.1989", port=5432)
    conn = psycopg.connect("postgresql://ia:Oracle.1989@localhost:5432/iadb")
    register_vector(conn)
    embedding = model.encode(question).tolist()
    with conn.cursor() as cur:
        query = """
        SELECT contents
        FROM internal_procs 
        ORDER BY embedding <=> %s::vector 
        LIMIT 1;
        """
        cur.execute(query, (embedding,))
        results = cur.fetchall()
        result_string = "\n".join(result[0] for result in results)
        conn.close()
    return result_string
