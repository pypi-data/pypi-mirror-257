from datetime import datetime
from typing import List, cast

from datetimerange import DateTimeRange
from pydantic import BaseModel, Field


class ClimateDatum(BaseModel):
    timestamp: datetime
    u_mean_ms: float = Field(
        ..., description="Mean wind speed at 2 meters [m/s]"
    )
    RH_min: float = Field(..., description="Minimum relative humidity")
    ET_0: float = Field(..., description="Reference evapotranspiration")
    precipation_mm: float = Field(..., description="Precipitation [mm]", ge=0)


class ClimateData(object):
    def __init__(self, data: List[ClimateDatum]):
        sorted(data, key=lambda d: d.timestamp)
        self.data_points = data

    def get_data_within_range(
        self, date_range: DateTimeRange
    ) -> List[ClimateDatum]:
        """
        Get climate data within a date range
        """
        return [
            d
            for d in self.data_points
            if cast(datetime, date_range.start_datetime)
            <= d.timestamp
            <= cast(datetime, date_range.end_datetime)
        ]

    @property
    def time_range(self) -> DateTimeRange:
        """
        Get the range of the climate data
        """
        return DateTimeRange(
            self.data_points[0].timestamp, self.data_points[-1].timestamp
        )
