from dataclasses import dataclass


@dataclass
class ExperimentConfig:
    foo: int = 0
    bar: bool = False
    quz: str = ""
