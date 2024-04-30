import nanoid


def generate_entity_id() -> str:
    return nanoid.generate(size=16)
