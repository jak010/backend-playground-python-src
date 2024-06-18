from __future__ import annotations

from typing import TypeVar

from dependency_injector.wiring import Provide
from sqlalchemy.orm.session import Session

from settings.container.db_container import DataBaseContainer

T = TypeVar("T")


class AbstracrtRDBRepository:
    session: Session = Provide[DataBaseContainer.session]
