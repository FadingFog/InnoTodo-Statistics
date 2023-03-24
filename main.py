from fastapi import FastAPI, Depends

from app.db import init_database
from app.models import UserAction
from app.schemas import Statistics
from app.services import StatisticsServices

app = FastAPI()


@app.on_event("startup")
async def start_database():
    await init_database()


@app.post("/api/statistics", response_model=UserAction)
async def create_user_action(action_schema: UserAction, service: StatisticsServices = Depends(StatisticsServices)):
    user_action = await service.create_user_action(action_schema)
    return user_action


@app.get("/api/statistics/{user_id}", response_model=Statistics)
async def retrieve_statistics(user_id: int, service: StatisticsServices = Depends(StatisticsServices)):
    data = await service.retrieve_statistics(user_id)
    return data
