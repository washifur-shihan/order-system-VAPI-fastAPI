from io import BytesIO
from pypdf import PdfReader
from app.db.supabase import supabase
from app.services.llm import embed_texts

def chunk_text(text: str, chunk_size: int = 700, overlap: int = 100):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks

def ingest_menu_pdf(document_id: str, storage_path: str):
    response = supabase.storage.from_("menu-files").download(storage_path)
    pdf = PdfReader(BytesIO(response))
    text = "\n".join(page.extract_text() or "" for page in pdf.pages)

    chunks = chunk_text(text)
    embeddings = embed_texts(chunks)

    rows = []
    for i, (chunk, emb) in enumerate(zip(chunks, embeddings)):
        rows.append({
            "document_id": document_id,
            "chunk_index": i,
            "content": chunk,
            "metadata": {"source": storage_path},
            "embedding": emb
        })

    if rows:
        supabase.table("menu_chunks").insert(rows).execute()