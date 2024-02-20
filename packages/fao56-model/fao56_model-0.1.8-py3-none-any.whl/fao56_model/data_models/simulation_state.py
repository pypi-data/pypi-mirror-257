from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class SimulationState(BaseModel):
    timestamp: datetime = Field(..., description="Timestamp of the simulation")
    etref_mm: float = Field(
        100, description="Reference evapotranspiration [mm/day]"
    )
    ET_c: Optional[float] = Field(
        None, description="Crop evapotranspiration [mm/day]"
    )
    d: Optional[float] = Field(None, description="Depletion fraction [-]")
    TAW: Optional[float] = Field(
        None, description="Total available water [mm]"
    )
    RO: float = Field(0, description="Runoff [mm/day]")
    RAW: Optional[float] = Field(
        None, description="Readily available water [mm]"
    )
    I_dem: Optional[float] = Field(
        None, description="Irrigation demand [mm/day]"
    )
    I_del: float = Field(0, description="Irrigation demand [mm/day]")
    K_s: Optional[float] = Field(
        None, description="Soil water stress coefficient [-]"
    )
    ET_a: Optional[float] = Field(
        None, description="Actual evapotranspiration [mm/day]"
    )
    Y_rel: Optional[float] = Field(
        None, description="Relative yield factor [-]"
    )
    Z_r: Optional[float] = Field(None, description="Root zone depth [mm]")
    D_r: Optional[float] = Field(None, description="Root zone depletion [mm]")
    ET_rel: Optional[float] = Field(
        None, description="Relative evapotranspiration [-]"
    )
    precip_mm: float = Field(0, description="Precipitation [mm]")
    K_c_correct: Optional[float] = Field(
        None, description="Corrected crop coefficient [-]"
    )
