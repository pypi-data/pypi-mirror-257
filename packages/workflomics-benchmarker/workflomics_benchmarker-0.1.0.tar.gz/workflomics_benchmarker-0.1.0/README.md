# Workflomics Benchmarker

Library used to execute workflows (in CWL) and benchmark them as part of the Workflomics ecosystem.

## Credits

The `workflomics benchmarker` script was developed by [Nauman Ahmed](@nahmedraja) as part of the [containers](https://github.com/Workflomics/containers) repository, but was since migrated to its own repository (see [PR #49](https://github.com/Workflomics/containers/pull/49)) to be published as a stand-alone package.

## Requirements

- Python 3.9+
- Poetry
- Docker or Singularity running

## Installation

```bash
poetry install 
```


## Usage

The command is used with Docker or Singularity service running. It will execute the workflow and benchmark it.

### Docker

```bash
workflomics benchmark tests/data/
```

which is equivalent to

```bash
python src/benchmarker/workflomics.py benchmark tests/data/
```

The results will be stored in the `./tests/data` folder.


### Singularity

Finally, you can run the test with Singularity. This will require you to have Singularity installed and running, and to use the `--singularity` flag.

```bash
python src/benchmarker/workflomics.py benchmark tests/data/ --singularity
```

## Testing

To run the tests, you can use the following command:

```bash
poetry run pytest -s
```

The tests will execute a workflow and benchmark it (require Docker running). The results will be stored in the `./tests/data` folder.