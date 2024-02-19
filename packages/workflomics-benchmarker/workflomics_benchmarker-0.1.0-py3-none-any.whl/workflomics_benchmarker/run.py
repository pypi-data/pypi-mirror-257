

# Simulate 'benchmark' command
from argparse import Namespace

from workflomics_benchmarker.cwltool_runtime_benchmark import CWLToolRuntimeBenchmark



test_args = Namespace(workflows='tests/data/', verbose=True)

runner  = CWLToolRuntimeBenchmark(test_args)
runner.run_workflows()
