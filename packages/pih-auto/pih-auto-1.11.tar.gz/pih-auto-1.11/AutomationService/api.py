from typing import Any, Callable
from dataclasses import dataclass

from pih.collections import Mark

@dataclass
class TimeTrackingReportConfiguration:
    division_id: int | None = None
    folder_name: str | None = None
    tab_number_list: list[str] | Callable[[None], list[str]] | None = None
    tab_number_filter_function: Callable[[Mark], bool] | None = None
    addition_tab_number_list: list[str] | Callable[[None], list[str]] | None = None
    additional_division_id: int | None = None
