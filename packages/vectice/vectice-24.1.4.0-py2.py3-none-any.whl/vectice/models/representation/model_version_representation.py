from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any, Dict

from vectice.api.json.model_version import ModelVersionStatus
from vectice.api.json.model_version_representation import ModelVersionRepresentationOutput, ModelVersionUpdateInput
from vectice.utils.common_utils import repr_class, strip_dict_list
from vectice.utils.dataframe_utils import repr_list_as_pd_dataframe

_logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from vectice.api.client import Client


class ModelVersionRepresentation:
    """Represents the metadata of a Vectice model version.

    A Model Version Representation details a specific model version's metadata retrieved from the Vectice app, facilitating metadata retrieval and readability from the API.

    NOTE: **Hint**
        Identify a model version by its ID, which starts with 'MDV-XXX'. Retrieve it using the Vectice App through the connect.model_version or connect.browse methods (see Connection page).

    Attributes:
        id (str): The unique identifier of the model version.
        project_id (str): The identifier of the project to which the model version belongs.
        name (str): The name of the model version. For model versions it corresponds to the version number.
        status (str): The status of the model version (EXPERIMENTATION, STAGING, PRODUCTION, or RETIRED).
        description (str): The description of the model version.
        technique (str): The technique used by the model version.
        library (str): The library used by the model version.
        metrics (List[Dict[str, Any]]): The metrics associated with the model version.
        properties (List[Dict[str, Any]]): The properties associated with the model version.
        model_representation_instance (ModelRepresentation): Reflects the source instance of the model linked to a specific model version.

    """

    def __init__(self, output: ModelVersionRepresentationOutput, client: "Client"):
        from vectice.models.representation.model_representation import ModelRepresentation

        self.id = output.id
        self.project_id = output.project_id
        self.name = output.name
        self.status = output.status
        self.description = output.description
        self.technique = output.technique
        self.library = output.library
        self.metrics = output.metrics
        self.properties = strip_dict_list(output.properties)
        self.model_representation_instance = ModelRepresentation(output.model, client)

        self._client = client

    def __repr__(self):
        return repr_class(self)

    def asdict(self) -> Dict[str, Any]:
        """Transform the ModelVersionRepresentation into a organised dictionary.

        Returns:
            The object represented as a dictionary
        """
        flat_metrics = {metric["key"]: metric["value"] for metric in self.metrics}
        flat_properties = {prop["key"]: prop["value"] for prop in self.properties}

        return {
            "id": self.id,
            "project_id": self.project_id,
            "name": self.name,
            "status": self.status,
            "description": self.description,
            "technique": self.technique,
            "library": self.library,
            "metrics": flat_metrics,
            "properties": flat_properties,
            "model_representation_instance": (
                self.model_representation_instance._asdict()  # pyright: ignore reportPrivateUsage
                if self.model_representation_instance
                else None
            ),
        }

    def metrics_as_dataframe(self) -> Any:
        """Transforms the metrics of the ModelVersionRepresentation into a DataFrame for better readability.

        Returns:
            pd.DataFrame: A DataFrame containing the metrics of the model version.
        """
        return repr_list_as_pd_dataframe(self.metrics)

    def properties_as_dataframe(self) -> Any:
        """Transforms the properties of the ModelVersionRepresentation into a DataFrame for better readability.

        Returns:
            pd.DataFrame: A DataFrame containing the properties of the model version.
        """
        return repr_list_as_pd_dataframe(self.properties)

    def update(self, status: str | None = None) -> None:
        """Update the status of the Model Version from the API.

        Parameters:
            status: The new status of the model. Accepted values are EXPERIMENTATION, STAGING, PRODUCTION and RETIRED.

        Returns:
            None
        """
        if status is None:
            _logger.warning("No status update provided. Nothing to update.")
            return

        try:
            status_enum = ModelVersionStatus(status.strip().upper())
        except ValueError as err:
            accepted_statuses = ", ".join([f"{status_enum.value!r}" for status_enum in ModelVersionStatus])
            raise ValueError(f"'{status}' is an invalid value. Please use [{accepted_statuses}].") from err

        model_input = ModelVersionUpdateInput(status=status_enum.value)
        self._client.update_model(self.id, model_input)
        old_status = self.status
        self.status = status_enum.value
        _logger.info(f"Model version {self.id!r} transitioned from {old_status!r} to {self.status!r}.")
