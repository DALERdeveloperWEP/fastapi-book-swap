from fastapi.routing import APIRouter

router = APIRouter()

@router.POST('/register'):
    async def create_user()