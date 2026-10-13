from src.api.threads import schemas

def get_thread(
    thread_id: int
) -> schemas.ThreadGetResponseSchema:
    return schemas.ThreadGetResponseSchema()

def create_thread(
    payload: schemas.ThreadCreateSchema
) -> schemas.ThreadCreateResponseSchema:
    return schemas.ThreadCreateResponseSchema()

def delete_thread(
    payload: schemas.ThreadDeleteSchema
) -> schemas.ThreadDeleteResponseSchema:
    return schemas.ThreadDeleteResponseSchema()