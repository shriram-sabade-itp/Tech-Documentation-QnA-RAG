import json
from pathlib import Path


REGISTRY_PATH = Path("app/data/registry/registry.json")
REGISTRY_PATH.parent.mkdir(parents=True, exist_ok=True)


class FileRegistry:

    def __init__(self):

        if not REGISTRY_PATH.exists():
            with open(REGISTRY_PATH, "w") as file:
                json.dump({}, file)

    def load_registry(self):

        with open(REGISTRY_PATH, "r") as file:
            return json.load(file)

    def save_registry(self, registry):

        with open(REGISTRY_PATH, "w") as file:
            json.dump(registry, file, indent=4)

    def is_already_ingested(self, checksum):

        registry = self.load_registry()

        return checksum in registry

    def register_document(self, checksum, doc_id):

        registry = self.load_registry()

        registry[checksum] = doc_id

        self.save_registry(registry)