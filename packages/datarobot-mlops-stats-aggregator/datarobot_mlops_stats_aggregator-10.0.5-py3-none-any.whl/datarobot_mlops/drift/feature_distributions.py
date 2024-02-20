#  --------------------------------------------------------------------------------
#  Copyright (c) 2021 DataRobot, Inc. and its affiliates. All rights reserved.
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
from typing import List
from typing import NamedTuple
from typing import Union

import pandas as pd

BIN_VALUES_COLUMN = 'Bin Values'
BASELINE_HIST_VALUES_COLUMN = 'Baseline'
CURRENT_HIST_VALUES_COLUMN = 'Current'


class FeatureDistributions(NamedTuple):
    """
    Class containing all necessary info to compute drift metrics.
    """

    feature_name: str
    feature_type: str
    bin_values: List[str]
    ref_histogram: Union[List[int], List[float]]
    expected_sample_size: int
    com_histogram: Union[List[int], List[float]]
    actual_sample_size: int

    def to_df(self):
        return pd.DataFrame(
            {
                BIN_VALUES_COLUMN: self.bin_values,
                BASELINE_HIST_VALUES_COLUMN: self.ref_histogram,
                CURRENT_HIST_VALUES_COLUMN: self.com_histogram,
            }
        )

    def plot(self, *args, **kwargs):
        df = self.to_df()
        params = dict(kwargs)
        if 'kind' not in params:
            params['kind'] = 'bar'
        params['x'] = BIN_VALUES_COLUMN
        params['y'] = [BASELINE_HIST_VALUES_COLUMN, CURRENT_HIST_VALUES_COLUMN]
        if 'title' not in params:
            params['title'] = (
                f'Feature="{self.feature_name}", Type="{self.feature_type}", '
                f'Baseline # {self.expected_sample_size}, Current # {self.actual_sample_size}'
            )
        df.plot(*args, **params)
