#  --------------------------------------------------------------------------------
#  Copyright (c) 2020 DataRobot, Inc. and its affiliates. All rights reserved.
#  Last updated 2023.
#
#  DataRobot, Inc. Confidential.
#  This is proprietary source code of DataRobot, Inc. and its affiliates.
#
#  This file and its contents are subject to DataRobot Tool and Utility Agreement.
#  For details, see
#  https://www.datarobot.com/wp-content/uploads/2021/07/DataRobot-Tool-and-Utility-Agreement.pdf.
#
#  --------------------------------------------------------------------------------

from pathlib import Path
from typing import Any
from typing import Dict
from typing import Optional as Nullable

import yaml
from schema import And
from schema import Optional
from schema import Or
from schema import Schema
from schema import Use


class DeploymentInfo:
    """
    A wrapper for the deployment info dict (from the deployment info YAML)
    """

    # TODO: the kev_value_config should be all optional and validated by the specific plugin
    def __init__(self, deployment_info: Dict[str, Any]):
        schema = Schema(
            {
                "id": And(str, len),
                "modelId": And(str, len),
                "modelExecutionType": And(str, len),
                Optional("keyValueConfig", default={}): dict,
                Optional("name"): str,
                Optional("description"): Or(None, str),
                Optional("modelArtifact"): Or(None, And(str, len, Use(Path))),
                Optional("modelFormat"): Or(None, str),
                Optional("newModelId"): And(str, len),
                Optional("featureTypes"): Or(None, And(str, len, Use(Path))),
                Optional("settings"): Or(None, And(str, len, Use(Path))),
                Optional("isPredictionExplanationsSupported"): Or(None, bool),
            },
            ignore_extra_keys=True,
        )

        self._deployment_info = schema.validate(deployment_info)

    def to_dict(self) -> Dict[str, Any]:
        tmp = self._deployment_info.copy()
        if "modelArtifact" in tmp:
            # convert Path to str if present in the data
            tmp["modelArtifact"] = str(tmp["modelArtifact"])
        return tmp

    def to_yaml(self) -> str:
        return yaml.safe_dump(self.to_dict(), indent=4)

    def __str__(self):
        return self.to_yaml()

    @property
    def id(self) -> str:
        return self._deployment_info["id"]

    @property
    def name(self) -> Nullable[str]:
        return self._deployment_info.get("name")

    @property
    def description(self) -> Nullable[str]:
        return self._deployment_info.get("description")

    @property
    def model_id(self) -> str:
        return self._deployment_info["modelId"]

    @property
    def model_artifact(self) -> Nullable[Path]:
        return self._deployment_info.get("modelArtifact")

    @property
    def model_format(self) -> Nullable[str]:
        return self._deployment_info.get("modelFormat")

    @property
    def model_execution_type(self) -> str:
        return self._deployment_info["modelExecutionType"]

    @property
    def kv_config(self) -> Dict[str, Any]:
        return self._deployment_info["keyValueConfig"]

    @property
    def new_model_id(self) -> Nullable[str]:
        return self._deployment_info.get("newModelId")

    @property
    def feature_types_path(self) -> Nullable[Path]:
        return self._deployment_info.get("featureTypes")

    @property
    def settings_path(self) -> Nullable[Path]:
        return self._deployment_info.get("settings")

    @property
    def is_prediction_explanations_supported(self) -> bool:
        return self._deployment_info.get("isPredictionExplanationsSupported", False)
