from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.models import User
from app.schemas.schemas import (
    VaultItemCreate, VaultItemUpdate, VaultItemOut, VaultAskRequest, VaultActionRequest
)
from app.services.vault_service import vault_service
from app.storage.file_storage import file_storage
from app.ai.orchestrator import ai_orchestrator
from app.api.deps import get_current_user

router = APIRouter(prefix="/vault", tags=["Knowledge Vault"])

@router.post("/items", response_model=VaultItemOut)
def create_vault_item(
    item_in: VaultItemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Save note, formula, code snippet, link, or saved AI answer to Knowledge Vault."""
    return vault_service.create_item(db, current_user.id, item_in)

@router.post("/upload", response_model=VaultItemOut)
async def upload_vault_file(
    file: UploadFile = File(...),
    topic: Optional[str] = Form("General"),
    folder: Optional[str] = Form("Personal Reference"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Secure file upload for PDFs, Markdown, TXT, and diagrams.
    Extracts text, uses AI to extract concepts/tags/summary, and saves to Knowledge Vault.
    """
    file_bytes = await file.read()
    try:
        file_path, original_filename, file_size = file_storage.save_file(
            filename=file.filename,
            file_bytes=file_bytes,
            mime_type=file.content_type
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    # Extract text content from PDF or text file
    extracted_text = file_storage.extract_text(file_path, file.content_type)
    if not extracted_text:
        extracted_text = f"Stored file: {original_filename}"

    # Determine content type
    ext = file.filename.split(".")[-1].lower() if "." in file.filename else ""
    if ext in ["png", "jpg", "jpeg", "webp"]:
        c_type = "image"
    elif ext == "pdf":
        c_type = "document"
    else:
        c_type = "document"

    # AI metadata extraction
    analysis = ai_orchestrator.analyze_vault_item(
        title=original_filename,
        content=extracted_text,
        content_type=c_type
    )

    item_in = VaultItemCreate(
        content_type=c_type,
        title=original_filename,
        content=extracted_text,
        file_path=file_path,
        file_name=original_filename,
        file_size=file_size,
        mime_type=file.content_type,
        topic=analysis.get("topic", topic),
        folder=folder,
        tags=analysis.get("tags", []),
        extracted_concepts=analysis.get("extracted_concepts", []),
        ai_summary=analysis.get("ai_summary", "")
    )

    return vault_service.create_item(db, current_user.id, item_in)

@router.get("/items", response_model=List[VaultItemOut])
def get_vault_items(
    content_type: Optional[str] = None,
    folder: Optional[str] = None,
    topic: Optional[str] = None,
    is_favorite: Optional[bool] = None,
    search: Optional[str] = None,
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Retrieve saved items with full search and categorical filtering."""
    return vault_service.get_items(
        db=db,
        user_id=current_user.id,
        content_type=content_type,
        folder=folder,
        topic=topic,
        is_favorite=is_favorite,
        search_query=search,
        skip=skip,
        limit=limit
    )

@router.get("/items/{item_id}", response_model=VaultItemOut)
def get_single_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    item = vault_service.get_item_by_id(db, current_user.id, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Vault item not found.")
    return item

@router.put("/items/{item_id}", response_model=VaultItemOut)
def update_vault_item(
    item_id: int,
    item_update: VaultItemUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    item = vault_service.update_item(db, current_user.id, item_id, item_update)
    if not item:
        raise HTTPException(status_code=404, detail="Vault item not found.")
    return item

@router.delete("/items/{item_id}")
def delete_vault_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    deleted = vault_service.delete_item(db, current_user.id, item_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Vault item not found.")
    return {"message": "Vault item deleted successfully."}

@router.post("/items/{item_id}/ask")
def ask_vault_item(
    item_id: int,
    req: VaultAskRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Grounded Q&A over this specific saved material."""
    try:
        return vault_service.ask_item(db, current_user.id, item_id, req.question)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/items/{item_id}/file")
def get_vault_file(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Authenticated, user-isolated file streaming for Knowledge Vault uploads.
    Verifies ownership before streaming and prevents path traversal.
    """
    import os
    from fastapi.responses import FileResponse
    from app.core.config import settings

    item = vault_service.get_item_by_id(db, current_user.id, item_id)
    if not item or not item.file_path:
        raise HTTPException(status_code=404, detail="File not found or not owned by current user.")

    upload_dir_abs = os.path.abspath(settings.UPLOAD_DIR)
    file_path_abs = os.path.abspath(item.file_path)
    if not file_path_abs.startswith(upload_dir_abs) or not os.path.isfile(file_path_abs):
        raise HTTPException(status_code=404, detail="File not found on storage.")

    return FileResponse(
        path=file_path_abs,
        filename=item.file_name or "document",
        media_type=item.mime_type or "application/octet-stream"
    )

@router.post("/action")
def perform_ai_study_action(
    req: VaultActionRequest,
    current_user: User = Depends(get_current_user)
):
    """Execute ad-hoc AI study actions: summarize, explain, or generate flashcards."""
    return vault_service.perform_ai_action(
        item_content=req.content or "",
        item_title="Saved Study Material",
        action=req.action
    )

@router.get("/revisions")
@router.get("/revision")
def get_revision_recommendations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Smart Revision: Suggests saved Vault reference materials for weak concepts."""
    return vault_service.get_revision_recommendations(db, current_user.id)
