from dataclasses import dataclass


@dataclass
class Test:
    name: str
    age: int


test_dict = {
    "name": "dude",
    "age": 15
}

test = Test(**test_dict)
print(test)
