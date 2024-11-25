from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Protocol, Union

from typeguard import typechecked


class ParserSettings(Protocol):
    def get_field_names(self) -> List[str]: ...

    def uses_header(self) -> bool: ...


@dataclass
class Transaction(Protocol):
    def to_dict(self) -> Dict[str, Union[int, float, str, datetime]]: ...

    def get_year(self) -> int: ...


# An example of extension/inheritance/sub-/super/(whatever) classes in Python.
class Shape(Protocol):
    def area(self) -> float: ...


class Circle:
    def __init__(self, radius: float):
        self.radius = radius

    def area(self) -> float:
        return 3.14 * self.radius**2


class Rectangle:
    def __init__(self, height: float, width: float):
        self.height = height
        self.width = width

    def area(self) -> float:
        return self.height * self.width


@typechecked
def calculate_area(shape: Shape) -> float:
    return shape.area()


circle = Circle(5)
rectangle = Rectangle(2, 6)

#print(calculate_area(circle))  # No error, structural typing matches.
#print(calculate_area(rectangle))  # No error, structural typing matches.
