from enum import Enum


class GetPathMethod(Enum):
    Input = "Input"
    Choose = "Choose"


class ChoosePathMethod(str, Enum):
    Choose = "./it::Choose"
    Into = "./it/...::Into"
