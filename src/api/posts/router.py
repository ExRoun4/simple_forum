from fastapi import APIRouter, status, Path
from src.api.posts import service, schemas, constants

router = APIRouter(
    prefix=constants.Routes.PREFIX,
    tags=constants.tags
)

@router.get("/{post_id}", response_model=schemas.PostGetResponse)
def get_post(
    post_id: int = Path()
) -> schemas.PostGetResponse:
    post_response = service.get_post(post_id)
    return post_response

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostCreateResponseSchema)
def create_post(
    payload: schemas.PostCreateSchema
) -> schemas.PostCreateResponseSchema:
    created_post_response = service.create_post(payload)
    return created_post_response

@router.delete("/", response_model=schemas.PostDeleteResponseSchema)
def delete_post(
    payload: schemas.PostDeleteSchema
) -> schemas.PostDeleteResponseSchema:
    deleted_post_response = service.delete_post(payload)
    return deleted_post_response
