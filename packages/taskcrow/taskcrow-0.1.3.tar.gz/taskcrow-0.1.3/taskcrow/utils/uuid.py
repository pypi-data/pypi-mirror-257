import uuid


def generate_uuid_from_seed(text):
    namespace = uuid.UUID('00000000-0000-0000-0000-000000000000')
    result = uuid.uuid5(namespace, text)
    return result
