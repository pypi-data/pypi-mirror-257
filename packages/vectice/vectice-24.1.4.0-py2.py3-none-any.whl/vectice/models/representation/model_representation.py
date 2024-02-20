from typing import TYPE_CHECKING

from vectice.api.json.model_representation import ModelRepresentationOutput
from vectice.utils.common_utils import repr_class

if TYPE_CHECKING:
    from vectice.api.client import Client


class ModelRepresentation:
    def __init__(self, output: ModelRepresentationOutput, client: "Client"):
        self.id = output.id
        self.project_id = output.project_id
        self.name = output.name
        self.type = output.type
        self.description = output.description
        self._last_version = output.version

    def __repr__(self):
        return repr_class(self)

    def _asdict(self):
        return {"name": self.name, "id": self.id, "description": self.description, "type": self.type}
