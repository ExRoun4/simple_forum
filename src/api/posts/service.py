from src.api.posts import schemas

def get_post(
    post_id: int
) -> schemas.PostGetResponse:
    return schemas.PostGetResponse()

def create_post(
    payload: schemas.PostCreateSchema
) -> schemas.PostCreateResponseSchema:
    return schemas.PostCreateResponseSchema()

def delete_post(
    payload: schemas.PostDeleteSchema
) -> schemas.PostDeleteResponseSchema:
    return schemas.PostDeleteResponseSchema()