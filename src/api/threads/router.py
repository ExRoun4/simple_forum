from fastapi import APIRouter, status, Query, Path
from src.api.threads import service, schemas, constants

router = APIRouter(
    prefix=constants.Routes.PREFIX,
    tags=constants.tags
)

# threads
@router.get("/{thread_id}", response_model=schemas.ThreadGetResponseSchema)
def get_thread(
    thread_id: int = Path()
) -> schemas.ThreadGetResponseSchema:
    thread = service.get_thread(thread_id)
    return thread

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.ThreadCreateResponseSchema)
def create_thread(
    payload: schemas.ThreadCreateSchema
) -> schemas.ThreadCreateResponseSchema:
    created_response = service.create_thread(payload)
    return created_response

@router.delete("/", response_model=schemas.ThreadDeleteResponseSchema)
def delete_thread(
    payload: schemas.ThreadDeleteSchema
) -> schemas.ThreadDeleteResponseSchema:
    deleted_response = service.delete_thread(payload)
    return deleted_response
