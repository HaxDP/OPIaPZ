from __future__ import annotations

from dataclasses import dataclass
from io import StringIO
from time import perf_counter, process_time
from typing import Callable, Iterable, Protocol
import cProfile
import pstats
import tracemalloc


@dataclass(frozen=True)
class analysisResult:
	n: int
	value: int


@dataclass(frozen=True)
class profileData:
	elapsed_seconds: float
	cpu_seconds: float
	peak_memory_bytes: int
	profiler_top: str


class sequenceAnalyzer(Protocol):
	def name(self) -> str:
		...

	def analyze(self, n: int) -> analysisResult:
		...


class resourceProfiler(Protocol):
	def profile(self, func: Callable[..., analysisResult], *args: object) -> tuple[analysisResult, profileData]:
		...


class naiveSumSquaresAnalyzer:
	def name(self) -> str:
		return "Базовий алгоритм"

	def analyze(self, n: int) -> analysisResult:
		# простий цикл обчислювання
		result = 0
		for i in range(1, n + 1):
			result += i * i
		return analysisResult(n=n, value=result)


class formulaSumSquaresAnalyzer:
	def name(self) -> str:
		return "Оптимізований алгоритм"

	def analyze(self, n: int) -> analysisResult:
		# оптимізований цикл обчислювання
		result = n * (n + 1) * (2 * n + 1) // 6
		return analysisResult(n=n, value=result)


class cProfileResourceProfiler:
	def __init__(self, top_entries: int = 5) -> None:
		self._top_entries = top_entries

	def profile(self, func: Callable[..., analysisResult], *args: object) -> tuple[analysisResult, profileData]:
		profiler = cProfile.Profile()
		tracemalloc.start()
		wall_start = perf_counter()
		cpu_start = process_time()
		profiler.enable()
		result = func(*args)
		profiler.disable()
		cpu_end = process_time()
		wall_end = perf_counter()
		_, peak = tracemalloc.get_traced_memory()
		tracemalloc.stop()

		output = StringIO()
		stats = pstats.Stats(profiler, stream=output).sort_stats("cumtime")
		stats.print_stats(self._top_entries)

		profile_data = profileData(
			elapsed_seconds=wall_end - wall_start,
			cpu_seconds=cpu_end - cpu_start,
			peak_memory_bytes=peak,
			profiler_top=output.getvalue().strip(),
		)
		return result, profile_data


@dataclass(frozen=True)
class benchmarkRow:
	algorithm_name: str
	n: int
	value: int
	elapsed_seconds: float
	cpu_seconds: float
	peak_memory_bytes: int
	profiler_top: str


class benchmarkService:
	def __init__(self, analyzers: Iterable[sequenceAnalyzer], profiler: resourceProfiler) -> None:
		self._analyzers = list(analyzers)
		self._profiler = profiler

	def run(self, scenarios: Iterable[int]) -> list[benchmarkRow]:
		rows: list[benchmarkRow] = []
		for n in scenarios:
			for analyzer in self._analyzers:
				result, profile = self._profiler.profile(analyzer.analyze, n)
				row = benchmarkRow(
					algorithm_name=analyzer.name(),
					n=result.n,
					value=result.value,
					elapsed_seconds=profile.elapsed_seconds,
					cpu_seconds=profile.cpu_seconds,
					peak_memory_bytes=profile.peak_memory_bytes,
					profiler_top=profile.profiler_top,
				)
				rows.append(row)
		return rows


class consistencyChecker:
	def validate(self, rows: Iterable[benchmarkRow]) -> list[str]:
		grouped: dict[int, set[int]] = {}
		for row in rows:
			grouped.setdefault(row.n, set()).add(row.value)

		messages: list[str] = []
		for n, values in grouped.items():
			if len(values) == 1:
				messages.append(f"Перевірка n={n}: результати співпадають.")
			else:
				messages.append(f"Перевірка n={n}: знайдено розбіжності!")
		return messages


class ukrainianReportFormatter:
	def format(self, rows: Iterable[benchmarkRow], checks: Iterable[str]) -> str:
		lines = [
			"Порівняння продуктивності алгоритмів",
			"=" * 40,
		]

		for row in rows:
			lines.append(f"Алгоритм: {row.algorithm_name}")
			lines.append(f"Сценарій n = {row.n}")
			lines.append(f"Результат: {row.value}")
			lines.append(f"Час виконання: {row.elapsed_seconds:.6f} с")
			lines.append(f"Процесорний час: {row.cpu_seconds:.6f} с")
			lines.append(f"Пікове використання пам'яті: {row.peak_memory_bytes} байт")
			lines.append("Зріз профайлера:")
			lines.append(row.profiler_top)
			lines.append("-" * 40)

		lines.append("Перевірка коректності")
		lines.append("=" * 40)
		lines.extend(checks)
		return "\n".join(lines)


class consolePrinter:
	def print(self, text: str) -> None:
		print(text)


class application:
	def __init__(
		self,
		benchmark_service: benchmarkService,
		checker: consistencyChecker,
		formatter: ukrainianReportFormatter,
		printer: consolePrinter,
	) -> None:
		self._benchmark_service = benchmark_service
		self._checker = checker
		self._formatter = formatter
		self._printer = printer

	def run(self) -> None:
		scenarios = [10_000, 100_000, 1_000_000]
		rows = self._benchmark_service.run(scenarios)
		checks = self._checker.validate(rows)
		report = self._formatter.format(rows, checks)
		self._printer.print(report)


def build_application() -> application:
	analyzers: list[sequenceAnalyzer] = [naiveSumSquaresAnalyzer(), formulaSumSquaresAnalyzer()]
	profiler = cProfileResourceProfiler(top_entries=3)
	benchmark_service = benchmarkService(analyzers=analyzers, profiler=profiler)
	checker = consistencyChecker()
	formatter = ukrainianReportFormatter()
	printer = consolePrinter()
	return application(benchmark_service, checker, formatter, printer)


if __name__ == "__main__":
	app = build_application()
	app.run()