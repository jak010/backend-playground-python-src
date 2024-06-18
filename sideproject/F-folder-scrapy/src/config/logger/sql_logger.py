from __future__ import annotations

import copy
import datetime
import json
import logging
import uuid
from typing import Any

import sqlparse
from rich.logging import RichHandler


class SQLJSONEndoer(json.JSONEncoder):
    def default(self, o: Any) -> Any:
        if isinstance(o, uuid.UUID):
            return o.hex
        if isinstance(o, datetime.datetime):
            return o.isoformat()

        return json.JSONEncoder.default(self, o)


class SQLAlchemySQLFormatter(logging.Formatter):

    def format(self, record):

        if len(record.args) == 2:
            param1, param2 = record.args
            if isinstance(param2.params, dict):

                data = copy.deepcopy(param2.params)

                if content := data.get("content", None):
                    data['content'] = content[0:10] + f"...({str(len(content))})sized"

                return f"[{param1}]:{json.dumps(data, indent=8, ensure_ascii=False, cls=SQLJSONEndoer)}"
        else:
            return self.parsing(sql_text=record.getMessage())

    def parsing(self, sql_text):
        sql = sqlparse.format(
            sql_text,
            keyword_case='upper',
            identifier_case='lower',
            truncate_strings=50,
            reindent=True).strip('\n')
        return sql


def get_handler():
    rich_handler = RichHandler(rich_tracebacks=True, level="INFO")
    rich_handler.setFormatter(SQLAlchemySQLFormatter())
    return rich_handler
