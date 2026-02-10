import os
from typing import TypedDict

import torch


class DistributedParameters(TypedDict):
    world_size: int
    rank: int
    local_rank: int
    device: torch.device
    device_type: str
    distributed: bool


def setup_ddp() -> DistributedParameters:
    """Detect distributed environment and initialize process group if needed."""
    if "RANK" in os.environ and "WORLD_SIZE" in os.environ:
        rank = int(os.environ["RANK"])
        world_size = int(os.environ["WORLD_SIZE"])
        local_rank = int(os.environ["LOCAL_RANK"])
        torch.cuda.set_device(local_rank)
        torch.distributed.init_process_group("nccl", rank=rank, world_size=world_size)
        return DistributedParameters(
            world_size=world_size,
            rank=rank,
            local_rank=local_rank,
            device=torch.device(f"cuda:{local_rank}"),
            device_type="cuda",
            distributed=True,
        )
    else:
        if torch.cuda.is_available():
            device = torch.device("cuda")
            device_type = "cuda"
        elif torch.backends.mps.is_available():
            device = torch.device("mps")
            device_type = "mps"
        else:
            device = torch.device("cpu")
            device_type = "cpu"
        return DistributedParameters(
            world_size=1,
            rank=0,
            local_rank=0,
            device=device,
            device_type=device_type,
            distributed=False,
        )
