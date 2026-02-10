import argparse
import csv
import json
import logging
import pathlib
import pprint
import sys
from dataclasses import asdict
from typing import Any

import wandb

import src
from src.config import ExperimentConfig, config_to_dataclass
from src.distributed import setup_ddp

logging.basicConfig(
    level=logging.INFO,
    format="\033[90m%(asctime)s \033[36m[%(levelname)s] \033[1;33m%(module)s\033[0m: %(message)s",
)
logger = logging.getLogger(__name__)


def run(config: ExperimentConfig, rank: int):
    logger.info(f"Experiment config:\n{pprint.pformat(asdict(config))}")

    if rank == 0:
        wandb.init(project="perfect-research-repo", config=asdict(config))

    # Actual experiment (replace with your experimental code)
    if config.bar:
        result = src.square(x=config.foo)
    else:
        result = config.foo

    logger.info(f"Hello, {config.quz}!")
    logger.info(f"result={result}")

    if rank == 0:
        # Write predictions
        predictions = [["Input", "Output"], [config.foo, result]]
        predictions_path = pathlib.Path(args.config_path).parent / "predictions.csv"
        with open(predictions_path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(predictions)
        logger.info(f"Predictions written to {predictions_path}")

        # Compute metrics and write
        metrics: dict[str, Any] = {}
        if result == 42:
            metrics["accuracy"] = 1.0
        else:
            metrics["accuracy"] = 0.0

        metrics_path = pathlib.Path(args.config_path).parent / "metrics.json"
        with open(metrics_path, "w") as f:
            json.dump(metrics, f, indent=4)
        logger.info(f"Metrics written to {metrics_path}")

        wandb.log(data={"test": metrics})
        wandb.finish()


if __name__ == "__main__":
    minimum_python_version: tuple = (3, 11)
    if sys.version_info < minimum_python_version:
        raise Exception(f"Must be using Python v{'.'.join(str(v) for v in minimum_python_version)}")

    parser = argparse.ArgumentParser()
    parser.add_argument("config_path", help="Path to a .cfg file")
    parser.add_argument("--overrides", nargs="*", default=[], help="Key=value overrides")
    args = parser.parse_args()

    config = config_to_dataclass(args.config_path, args.overrides, ExperimentConfig)
    distributed_parameters = setup_ddp()

    run(config, rank=distributed_parameters["rank"])

    if distributed_parameters["distributed"]:
        import torch.distributed
        torch.distributed.destroy_process_group()
