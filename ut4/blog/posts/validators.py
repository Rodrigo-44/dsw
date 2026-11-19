from django.core.exceptions import ValidationError


def validate_title(value: str):
    if not value.istitle():
        raise ValidationError(f'{value} is not in title format')


def cacharacter_post(value: int):
    MAX_CHARACTERS = 20
    if value > MAX_CHARACTERS:
        raise ValidationError(
            f'{MAX_CHARACTERS} is the max_character permited in post not {value} '
        )
