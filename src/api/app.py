from http import HTTPStatus
from typing import Annotated

from fastapi import FastAPI, Header
from sqlalchemy import func
from sqlalchemy.orm import Session

from src.api.api_models import Message, TotalAmount
from src.api.database_client import DatabaseClient
from src.api.database_models import Customer, Sale

app = FastAPI()


@app.get(
    '/', 
    status_code=HTTPStatus.OK, 
    response_model=Message
)
async def health_check():
    return Message(message="It's working!")


@app.get('/customers/', status_code=HTTPStatus.OK)
async def get_customers(cd_customer: Annotated[str, Header()]):
    database_client = DatabaseClient()

    with Session(database_client.engine) as session:
        result = session.query(Customer).filter_by(cd_customer=cd_customer).first()

    return result


@app.get('/sales/', status_code=HTTPStatus.OK)
async def get_total_amount_sales(cd_customer: Annotated[str, Header()]):
    database_client = DatabaseClient()

    with Session(database_client.engine) as session:
        total = (
            session.query(func.coalesce(func.sum(Sale.total_value), 0))
            .filter(Sale.cd_customer == cd_customer)
            .scalar()
        ) 

    return TotalAmount(total=total)