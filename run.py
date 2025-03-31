import argparse
import configparser
import csv
import json
import pathlib
import sys
from typing import Any

import src


def run_experiment(folder: pathlib.Path):
    config = configparser.ConfigParser()
    config.read(folder / "config.ini")

    # Code for running experiment with specific config
    log_file = open(folder / "output.log", "w", encoding="utf-8")
    log_file.write("Starting experiment. Hello world!\n")

    foo = config.getint("ec", "foo")
    bar = config.getboolean("ec", "bar")
    quz = config.get("ec", "quz")

    # Actual experiment (replace with your experimental code)
    if bar:
        result = src.square(x=foo)
    else:
        result = foo

    log_file.write(f"Hello, {quz}!\n")
    log_file.write(f"{result=}\n")

    # Write predictions
    predictions = [["Input", "Output"], [foo, result]]
    with open(folder / "predictions.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(predictions)
    print(f"Predictions written to {folder / 'predictions.csv'}")

    # Compute metrics and write
    metrics: dict[str, Any] = {}
    if result == 42:
        metrics["accuracy"] = 1.0
    else:
        metrics["accuracy"] = 0.0
    with open(folder / "metrics.json", "w") as f:
        json.dump(metrics, f, indent=4)
    print(f"Predictions written to {folder / 'metrics.json'}")


if __name__ == "__main__":
    minimum_python_version: tuple = (3, 11)
    if sys.version_info < minimum_python_version:
        raise Exception(f"Must be using Python v{'.'.join(minimum_python_version)}")
    parser = argparse.ArgumentParser()
    parser.add_argument("experiment_folder")
    args = parser.parse_args()
    run_experiment(pathlib.Path(args.experiment_folder))
