#
# Copyright 2024 DataRobot, Inc. and its affiliates.
#
# All rights reserved.
#
# DataRobot, Inc.
#
# This is proprietary source code of DataRobot, Inc. and its
# affiliates.
#
# Released under the terms of DataRobot Tool and Utility Agreement.
from typing import Any, cast, List, Tuple, Union

import trafaret as t

from datarobot.insights.base import BaseInsight


class ShapPreview(BaseInsight):
    """
    Shap Preview Insight
    """

    INSIGHT_NAME = "shapPreview"
    INSIGHT_DATA = {
        t.Key("preview"): t.List(t.List(t.Tuple(t.String(), t.Or(t.Int(), t.Float()), t.Any()))),
    }

    @property
    def preview(self) -> List[List[Tuple[str, Union[int, float], Any]]]:
        """SHAP preview values

        Returns
        -------
        preview : List[List[Tuple[str, Union[int, float], Any]]]
            The outer list is the size of the rows in the preview. The inner list is the size of the features.
            The Tuples are ordered by decreasing shap value. Each Tuple is composed of the
            (feature name, shap value for the feature, original feature raw value) for the features of that row.

        """
        return cast(List[List[Tuple[str, Union[int, float], Any]]], self.data["preview"])
