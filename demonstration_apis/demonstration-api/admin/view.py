from fastapi import FastAPI

from settings.dev import patch_ioc
from src import backgrounds
from src.api.concurrency_lock_test import *
from src.api.relation_test import *
from src.api.router_v2.index_router import index_router_v1
from src.utils import start_mapper

from sqladmin import Admin, ModelView
from src.orm import Member
from src import orm

from settings.dev import get_engine


class UserAmdinView(ModelView, model=Member):
    column_list = [Member.pk, Member.name]
