from fastapi import APIRouter, UploadFile, File
from utils.resume_parser import parse_resume

router = APIRouter()

@router.post("/upload")
async def upload_resume(file: UploadFile = File(...)):
    contents = await file.read()
    result = parse_resume(contents)
    return {"parsed_data": result}
