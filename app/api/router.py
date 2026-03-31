from fastapi import APIRouter

from .user import router as users_router
# from .book import router as books_router
# from .swap import router as swap_router

router = APIRouter()
router.include_router(prefix='/api/users', tags=['users'], router=users_router)
# router.include_router(prefix='/api/books', tags=['books'], router=books_router)
# router.include_router(prefix='/api/buy', tags=['swap'], router=swap_router)
