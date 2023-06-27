from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from learn_sql_model.config import get_session
from learn_sql_model.models.hero import Hero, HeroCreate, HeroRead, HeroUpdate, Heros

hero_router = APIRouter()


@hero_router.on_event("startup")
async def on_startup() -> None:
    # SQLModel.metadata.create_all(get_config().database.engine)
    ...


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
    "create a hero"
    db_hero = Hero.from_orm(hero)
    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)
    # await manager.broadcast({hero.json()}, id=1)
    return db_hero


@hero_router.patch("/hero/")
async def patch_hero(
    *,
    session: Session = Depends(get_session),
    hero: HeroUpdate,
) -> HeroRead:
    "update a hero"
    db_hero = session.get(Hero, hero.id)
    if not db_hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    for key, value in hero.dict(exclude_unset=True).items():
        setattr(db_hero, key, value)
    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)
    # await manager.broadcast({hero.json()}, id=1)
    return db_hero


@hero_router.delete("/hero/{hero_id}")
async def delete_hero(
    *,
    session: Session = Depends(get_session),
    hero_id: int,
):
    "delete a hero"
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    session.delete(hero)
    session.commit()
    # await manager.broadcast(f"deleted hero {hero_id}", id=1)
    return {"ok": True}


@hero_router.get("/heros/")
async def get_heros(
    *,
    session: Session = Depends(get_session),
) -> Heros:
    "get all heros"
    statement = select(Hero)
    heros = session.execute(statement).all()
    return Heros(__root__=heros)
