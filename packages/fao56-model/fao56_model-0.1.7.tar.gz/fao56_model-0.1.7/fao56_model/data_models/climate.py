import math
from datetime import datetime
from typing import List, cast

from datetimerange import DateTimeRange
from pydantic import BaseModel, Field


class ClimateDatum(BaseModel):
    timestamp: datetime
    wind_speed_10m_ms: float = Field(
        ..., description="Mean wind speed at 10 meters [m/s]"
    )
    min_relative_humidity_pct: float = Field(
        ..., description="Minimum relative humidity"
    )
    etref_mm: float = Field(..., description="Reference evapotranspiration")
    precip_mm: float = Field(..., description="Precipitation [mm]", ge=0)

    @property
    def wind_speed_2m_ms(self) -> float:
        """
        Mean wind speed at 2 meters [m/s]
        """
        h = 10
        return self.wind_speed_10m_ms * (4.87 / math.log(67.8 * h - 5.42))


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
