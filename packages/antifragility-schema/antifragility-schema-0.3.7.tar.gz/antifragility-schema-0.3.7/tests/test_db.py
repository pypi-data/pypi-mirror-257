from asyncio import run
from os import getenv as env
from dotenv import load_dotenv
from tortoise_api_model import init_db
from tortoise.backends.asyncpg import AsyncpgDBClient

from antifragility_schema import models
from antifragility_schema.models import Cur

load_dotenv()


def test_init_db():
    res = run(init_db(env('PG_DSN'), models))
    assert isinstance(res, AsyncpgDBClient), "DB corrupt"


# def test_models():
#     test_init_db()
#     c = Cur.all()
#     assert c.model, "DB corrupt"
