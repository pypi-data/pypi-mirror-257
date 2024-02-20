from dataclasses import dataclass

import pandas as pd

from xleap.metrics.common import ItemResult, Metric
from xleap.metrics.config import config
from xleap.metrics.validation import EvaluationMode


@dataclass
class MetricResultItem:
    value: float | int
    reason: str | None = None


class PromptLength(Metric):
    name = "prompt-length"

    evaluation_mode = EvaluationMode.qcg

    def init_model(self):
        pass

    def compute(self, df: pd.Series, force=False):
        return super().compute(df, force) or ItemResult(
            len(df[config.prompt_column]), None
        )


class ResponseLength(Metric):
    name = "response-length-123"

    evaluation_mode = EvaluationMode.qcg

    def init_model(self):
        pass

    def compute(self, df: pd.Series, force=False):
        return super().compute(df, force) or ItemResult(
            len(df[config.response_column]), None
        )


class ResponseSpaceCount(Metric):
    name = "response-space-count-123"

    evaluation_mode = EvaluationMode.qcg

    def init_model(self):
        pass

    def compute(self, df: pd.Series, force=False):
        return super().compute(df, force) or ItemResult(
            len(df[config.response_column] + df[config.prompt_column]), None
        )


prompt_length = PromptLength(batch_size=20)
response_length = ResponseLength(batch_size=20)
response_space_count = ResponseSpaceCount(batch_size=20)
