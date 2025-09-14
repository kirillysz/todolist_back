from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_201_CREATED

from app.schemas.user.user import UserCreate

from app.db.session import get_db
from app.core.auth_key import generate_access_token

from app.crud.user.user_crud import UserCRUD
from app.core.security import pass_settings

router = APIRouter()
@router.post("/register", status_code=HTTP_201_CREATED)
async def register_user(
    response: Response,
    user: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    new_user = await UserCRUD.create_user(
        db=db,
        user_data=user
    )

    if not new_user:
        raise HTTPException(
            status_code=400,
            detail="Error creating user"
        )

    access_token = generate_access_token(
        payload={"sub": new_user.username}
    )
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=False, # !!!!! НА ПРОДЕ TRUE
        samesite="strict"
    )
    return {"message": "Logged in"}


@router.post("/login")
async def login_user(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    user = await UserCRUD.get_user_by_username(
        db=db,
        username=form_data.username
    )

    if not user:
        raise HTTPException(
            status_code=400,
            detail="Incorrect username or password"
        )

    is_valid_password = pass_settings.verify_password(
        plain_password=form_data.password,
        hashed_password=user.hashed_password
    )

    if not is_valid_password:
        raise HTTPException(
            status_code=400,
            detail="Incorrect username or password"
        )

    access_token = generate_access_token(
        payload={"sub": user.username}
    )

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=False, # !!!!! НА ПРОДЕ TRUE
        samesite="strict"
    )
    return {"message": "Logged in"}