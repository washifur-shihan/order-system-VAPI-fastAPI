from fastapi import APIRouter, UploadFile, File, BackgroundTasks, HTTPException
from uuid import uuid4
from app.db.supabase import supabase
from app.services.pdf_ingest import ingest_menu_pdf
from app.services.retrieval import search_menu

router = APIRouter()

@router.post("/upload")
async def upload_menu(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    content = await file.read()
    storage_path = f"menus/{uuid4()}-{file.filename}"

    supabase.storage.from_("menu-files").upload(
        path=storage_path,
        file=content,
        file_options={"content-type": "application/pdf"}
    )

    doc = supabase.table("menu_documents").insert({
        "name": file.filename,
        "storage_path": storage_path,
        "is_active": True
    }).execute()

    document_id = doc.data[0]["id"]
    background_tasks.add_task(ingest_menu_pdf, document_id, storage_path)

    return {"status": "uploaded", "document_id": document_id}


@router.get("/test-search")
async def test_search(q: str):
    results = search_menu(q, match_count=5)
    return {"results": results}