from __future__ import annotations


### Value Object

class Recevier:
    name: str
    phone: str

    def __init__(self, name, phone_number):
        self.phone_number = phone_number
        self.name = name

    def get_name(self):
        return self.name

    def get_phone_number(self):
        return self.phone_number


class Address:
    addres1: str
    addres2: str
    zipcode: str

    def __init__(self,
                 addres1,
                 addres2,
                 zipcode,
                 ):
        self.addres1 = addres1
        self.addres2 = addres2
        self.zipcode = zipcode


class Money:
    value: int

    def __init__(self, value):
        self.value = value

    def add(self, money: Money):
        return Money(value=self.value + money.value)

    def multiply(self, money: Money):
        return Money(value=self.value * money.value)


##### Entity

class ShippongInfo:
    receiver: Recevier
    address: Address

    def __init__(self,
                 receiver: Recevier,
                 address: Address,
                 ):
        self.receiver = receiver
        self.address = address
