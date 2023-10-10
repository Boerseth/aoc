import json


class Problem:
    def __init__(self, year: int, day: int, test: bool, base_dir: str) -> None:
        self.year = year
        self.day = day
        self.test = test
        self.path =  f"{base_dir}/{self.year}/{self.day}"

    def get_problem_file(self, filename: str) -> str:
        prefix = "test" if self.test else ""
        file_path = f"{self.path}/{prefix}{filename}"
        with open(file_path, "r") as f:
            return f.read()

    def input(self) -> str | None:
        try:
            return self.get_problem_file("input")
        except Exception:
            return None

    def solutions(self) -> list[str | None]:
        try:
            return json.loads(self.get_problem_file("solution.json"))
        except Exception:
            return [None, None]
