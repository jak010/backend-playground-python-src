from __future__ import annotations
from abc import abstractmethod, ABCMeta, ABC
from typing import TypeVar, Generic, Type, Protocol, NewType

from enum import Enum
from collections import abc

import typing

from abc import ABC, abstractmethod

"""
protocol_classes.py: An example of using protocol classes.
"""

from abc import ABC, abstractmethod


class Vehicle(metaclass=ABCMeta):

    def run(self):
        raise NotImplementedError()


class Car(Vehicle):

    def run(self): ...


class ByCycle(Vehicle):

    def run(self): ...