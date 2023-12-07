from fastapi import APIRouter, Request
from pydantic import BaseModel
from src import database as db
import sqlalchemy
from sqlalchemy.exc import DBAPIError

router = APIRouter(
    prefix="/aliases",
    tags=["aliases"]
)

class AliasInfo(BaseModel):
    name: str
    owner_uid: str

@router.post("/")
def create_alias(info: AliasInfo):
    '''create a new alias for this account'''
    try:
        with db.engine.begin() as connection:
            connection.execute(
                sqlalchemy.text('''
                Insert into aliases
                (name, owner)
                Values
                (:name, :owner)
                '''),
                {
                    'name': info.name,
                    'owner': info.owner_uid
                }
            )
        return [True]
    except DBAPIError as error:
        print(error)
        return [False]

@router.get("/{alias_id}")
def get_alias_info(alias_id: int):
    '''get information about an alias'''
    try:
        with db.engine.begin() as connection:
            row = connection.execute(
                sqlalchemy.text('''Select aliases.name as alias, accounts.name as owner
                from aliases join accounts on aliases.owner = accounts.uid
                where aliases.id = :id'''),
                {
                    'id': alias_id
                }
            ).first()
            return [
                True, 
                {
                    'alias': row.alias,
                    'owner': row.owner
                }
            ]
    except DBAPIError as error:
        print(error)
        return [False, {}]