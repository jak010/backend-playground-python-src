from eventsourcing.domain import Aggregate, event


class Dog(Aggregate):

    @event("Registered")
    def __init__(self, name):
        self.name = name
        self.tricks = []

    @event("TrickAdded")
    def add_tricks(self, trick):
        return self.tricks.append(trick)

    @event("ChangeName")
    def change_name(self, name):
        self.name = name


if __name__ == '__main__':
    dog = Dog("Fido")

    # print(dog)

    dog.change_name(name="Unfido")

    # print(dog)
    events = dog.collect_events()

    for e in events:
        print(e.apply(dog))

    print(dog)
