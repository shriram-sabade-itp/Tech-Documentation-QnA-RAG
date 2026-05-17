import json
from pathlib import Path
from datetime import datetime

from app.ingestion.models import Checkpoint


CHECKPOINT_DIR = Path("app/data/checkpoints")
CHECKPOINT_DIR.mkdir(parents=True, exist_ok=True)


class CheckpointManager:

    @staticmethod
    def save_checkpoint(checkpoint: Checkpoint):

        checkpoint_path = CHECKPOINT_DIR / f"{checkpoint.doc_id}.json"

        with open(checkpoint_path, "w") as file:
            json.dump(
                checkpoint.model_dump(mode="json"),
                file,
                indent=4
            )

    @staticmethod
    def load_checkpoint(doc_id: str):

        checkpoint_path = CHECKPOINT_DIR / f"{doc_id}.json"

        if not checkpoint_path.exists():
            return None

        with open(checkpoint_path, "r") as file:
            data = json.load(file)

        return Checkpoint(**data)