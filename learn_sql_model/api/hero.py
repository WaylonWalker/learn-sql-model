from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import SQLModel, Session

from learn_sql_model.api.websocket_connection_manager import manager
from learn_sql_model.config import get_config, get_session
from learn_sql_model.models.hero import Hero, HeroCreate, HeroRead, HeroUpdate

hero_router = APIRouter()


@hero_router.on_event("startup")
def on_startup() -> None:
    SQLModel.metadata.create_all(get_config().database.engine)


@hero_router.get("/hero/{hero_id}")
async def get_hero(
    *,
    session: Session = Depends(get_session),
    hero_id: int,
) -> HeroRead:
    "get one hero"
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    return hero


@hero_router.post("/hero/")
async def post_hero(
    *,
    session: Session = Depends(get_session),
    hero: HeroCreate,
) -> HeroRead:
    "read all the heros"
    db_hero = Hero.from_orm(hero)
    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)
    await manager.broadcast({hero.json()}, id=1)
    return db_hero


@hero_router.patch("/hero/")
async def patch_hero(
    *,
    session: Session = Depends(get_session),
    hero: HeroUpdate,
) -> HeroRead:
    "read all the heros"
    db_hero = session.get(Hero, hero.id)
    if not db_hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    for key, value in hero.dict(exclude_unset=True).items():
        setattr(db_hero, key, value)
    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)
    await manager.broadcast({hero.json()}, id=1)
    return db_hero


@hero_router.delete("/hero/{hero_id}")
async def delete_hero(
    *,
    session: Session = Depends(get_session),
    hero_id: int,
):
    "read all the heros"
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    session.delete(hero)
    session.commit()
    await manager.broadcast(f"deleted hero {hero_id}", id=1)
    return {"ok": True}


@hero_router.get("/heros/")
async def get_heros(
    *,
    session: Session = Depends(get_session),
) -> list[Hero]:
    "get all heros"
    return Heros.list(session=session)
