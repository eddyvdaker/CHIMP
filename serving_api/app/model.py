import numpy as np
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional, Dict, Any, List, Union
from onnxruntime.capi.onnxruntime_pybind11_state import (
    InvalidArgument as OnnxInvalidArgument,
)

from app.errors import InvalidDataFormatError


class BaseModel(ABC):
    """Base class for models."""

    name: str
    _models: Dict[str, Any] = {}
    updated: datetime

    def __init__(self, model_name: str, models: Dict[str, Any]):
        self.name = model_name
        self._models = models
        self.updated = datetime.utcnow()

    @abstractmethod
    def predict(
        self,
        data: Any,
        stage: Optional[str] = "production",
        model_id: Optional[str] = "",
    ) -> Any:
        """Run a prediction on the given data.

        Parameters
        ----------
        data : Any
            The data to run a prediction on.
        stage : Optional[str]
            The stage of the model to use (defaults to production).
        model_id : Optional[str]
            Optionally use a calibrated model.

        Returns
        -------
        The prediction for the given data.
        """
        pass

    def update_model(self, tag: str, updated_model: Any) -> None:
        """Update a model with a given tag (either staging or a calibrated model).

        Parameters
        ----------
        tag : str
            The tag for the model to update.
        updated_model : Any
            New model to store for the given tag.
        """
        self._models[tag] = updated_model

    def get_model_tags(self) -> List[str]:
        """Get a list of available tags.

        Returns
        -------
        A list of available tags for this model.
        """
        return list(self._models.keys())

    def get_model_by_tag(self, tag: str) -> Union[Any, None]:
        """Get a model based on a given tag.

        Parameters
        ----------
        tag : str
            The tag to return a model for.

        Returns
        -------
        The model for the given tag or None if no model with a given tag is found
        """
        return self._models.get(tag)


class OnnxModel(BaseModel):
    """Implementation of BaseModel voor ONNX models."""

    def predict(
        self,
        data: Any,
        stage: Optional[str] = "production",
        model_id: Optional[str] = "",
    ) -> Any:
        if type(data) is not list:
            raise InvalidDataFormatError("Expected a list as data input")
        try:
            if model_id and model_id in self._models:
                model = self._models[model_id]
            else:
                model = self._models[stage]
            data = np.asarray(data)
            return {k: v.tolist() for k, v in model.predict(data).items()}
        except OnnxInvalidArgument:
            raise InvalidDataFormatError()
