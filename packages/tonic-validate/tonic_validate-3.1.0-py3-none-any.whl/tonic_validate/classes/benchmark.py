from typing import Iterator, List, Optional
from dataclasses import dataclass
from uuid import UUID

from tonic_validate.utils.telemetry import Telemetry


@dataclass
class BenchmarkItem:
    question: str
    answer: Optional[str] = None
    benchmark_id: Optional[UUID] = None


class Benchmark:
    def __init__(
        self,
        questions: List[str],
        answers: Optional[List[str]] = None,
        name: Optional[str] = None,
    ):
        self.name: Optional[str] = name
        self.items: List[BenchmarkItem] = []
        self.telemetry = Telemetry()

        if answers is None:
            for question in questions:
                self.items.append(BenchmarkItem(question))
            return

        if len(questions) != len(answers):
            raise ValueError("Questions and answers must be the same length")
        for question, answer in zip(questions, answers):
            self.items.append(BenchmarkItem(question, answer))

        try:
            self.telemetry.log_benchmark(len(questions))
        except Exception as _:
            pass

    # define iterator
    def __iter__(self) -> Iterator[BenchmarkItem]:
        return iter(self.items)
