# perfect-research-repo

## Introduction

Research code is notoriously unpleasant. Part of that is because there aren't great standards for project organization, and research repos quickly become incomprehensible mazes of interlocking (and likely broken) code.

In an attempt to solve this, this repo provides (another) standard template for a research project. It uses a strict division between implementation and experimentation code. Experiments are specified with `.cfg` files, which clearly indicate all of the configured parameters for a run. Logging is handled with `logging.logger` and `wandb`. Distributed data parallel (DDP) is supported via `torchrun`.

## Installation

```bash
# Must be using Python >=3.11
uv sync
```

## Usage

```bash
uv run run.py experiments/example_exp1/config.cfg
```

With CLI overrides:

```bash
uv run run.py experiments/example_exp1/config.cfg --overrides foo=10 bar=yes
```

For distributed training with DDP:

```bash
torchrun --nproc_per_node=NUM_GPUS run.py experiments/example_exp1/config.cfg
```
