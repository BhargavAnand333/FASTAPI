from fastapi import APIRouter, Depends, status, HTTPException
from .. import schemas
from .. import database, models
from sqlalchemy.orm import Session
from ..hashing import Hash

get_db = database.get_db

router = APIRouter(
    tags = ['Users'],
    prefix = "/user"
)

@router.post('/', response_model= schemas.ShowUser)
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    new_user = models.User(name = request.name, email = request.email, password = Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get('/{id}', response_model = schemas.ShowUser)
def get_user(id:int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"User with id {id} not found")
    return user
