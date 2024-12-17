import shortuuid

def unique_id(model):
    while True:
        random = shortuuid.ShortUUID().random(length=8)
        if not model.objects.filter(id=random).exists():
            break
    return random


def convert_drf_form_error_to_norm(data):
    result = ''
    for key in data.keys():
        for j in data[key]:
            result += j + ' '
    return result[:-1]
