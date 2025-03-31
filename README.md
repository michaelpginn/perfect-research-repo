# perfect-research-repo

## Introduction

Research code is notoriously unpleasant. Part of that is because there aren't great standards for project organization, and research repos quickly become incomprehensible mazes of interlocking (and likely broken) code.

In an attempt to solve this, this repo provides (another) standard template for a research project. It utilizes no external dependencies and a strict division between implementation and experimentation code. Furthermore, experiments are specified with config files, which clearly indicate all of the configured parameters for a run.

## Installation

```bash
# Must be using Python >=3.11
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Usage

```bash
python run.py experiments/<experiment_folder_name>
```
