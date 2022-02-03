def change_camel_case_to_snake_case(string):
    snake_case = "".join(
        ["_" + i.lower() if i.isupper() else i for i in string]
    ).lstrip("_")
    return snake_case
