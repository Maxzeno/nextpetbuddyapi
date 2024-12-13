import shortuuid

def unique_id(model):
    while True:
        random = shortuuid.ShortUUID().random(length=8)
        if not model.objects.filter(id=random).exists():
            break
    return random
