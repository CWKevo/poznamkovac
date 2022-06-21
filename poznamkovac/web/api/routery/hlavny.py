from fastapi import APIRouter


HLAVNY_ROUTER = APIRouter()



@HLAVNY_ROUTER.get('/test')
async def test():
    return {'message': 'Toto je hlavný router. Vypadá to tak, že funguje.'}
