import time
import unittest
from os import system

import helpers
from fusion_logger_python import FusionLogFormatter, FusionLogLevel, FusionLoggerBuilder

cls = lambda: system('cls')
cls()


class MyTestCase(unittest.TestCase):
    formatter = FusionLogFormatter("[{LEVEL}] {TIMESTAMP} [{NAME}] {MESSAGE}")
    benchmark_file = "benchmark.log"
    benchmark_logger = (FusionLoggerBuilder()
                        .set_formatter(formatter)
                        .set_name(__name__)
                        .set_min_level(FusionLogLevel.DEBUG)
                        .write_to_file(benchmark_file)
                        .build())

    uut_file = "temp/logging.log"
    uut_logger = (FusionLoggerBuilder()
                  .set_formatter(formatter)
                  .set_name(__name__)
                  .set_min_level(FusionLogLevel.DEBUG)
                  .write_to_file(uut_file)
                  .build())

    def benchmark_x(self, runs: int) -> float:

        # Run the command and time it
        random_strs: list[str] = []
        for i in range(runs):
            random_strs.append(str(i) + helpers.random_utf8_string(1, 250))
        t = time.process_time()
        for i in range(runs):
            self.uut_logger.warning(random_strs[i])
        elapsed_time = time.process_time() - t

        # Clear Console and file
        cls()
        open(self.uut_file, 'w').close()
        return elapsed_time

    def test_benchmark(self):
        open(self.benchmark_file, 'w').close()

        elapsed: float = self.benchmark_x(100)
        self.benchmark_output("Benchmark-100 Calls", 100, elapsed)

        elapsed: float = self.benchmark_x(1_000)
        self.benchmark_output("Benchmark-1.000 Calls", 1000, elapsed)

        elapsed: float = self.benchmark_x(10_000)
        self.benchmark_output("Benchmark-10.000 Calls", 10000, elapsed)

        elapsed: float = self.benchmark_x(100_000)
        self.benchmark_output("Benchmark-100.000 Calls", 100000, elapsed)

        elapsed: float = self.benchmark_x(1_000_000)
        self.benchmark_output("Benchmark-1.000.000 Calls", 1_000_000, elapsed)

    def benchmark_output(self, name: str, runs: int, elapsed: float) -> None:
        self.benchmark_logger.info("+++++++++++++++++++++++++++++++++++++++++++++++++++")
        self.benchmark_logger.info("| Benchmarking...")
        self.benchmark_logger.info("| Name: " + name)
        self.benchmark_logger.info("| Elapsed time: " + str(elapsed))
        self.benchmark_logger.info("| Avg. time per call: " + str(elapsed / runs))
        self.benchmark_logger.info("| Avg. msg per sec: " + str(runs / elapsed))
        self.benchmark_logger.info("+++++++++++++++++++++++++++++++++++++++++++++++++++\n")


if __name__ == '__main__':
    unittest.main()
