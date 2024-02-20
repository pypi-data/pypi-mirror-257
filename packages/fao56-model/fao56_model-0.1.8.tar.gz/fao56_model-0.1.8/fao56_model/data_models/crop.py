from typing import Literal

from pydantic import BaseModel, Field

CropType = Literal["spring wheat"]


class Crop(BaseModel):
    kind: CropType = Field(..., description="Crop type", alias="crop_type")
    crop_coefficient_ini: float = Field(
        ..., description="Initial crop coefficient", alias="kc_ini"
    )
    crop_coefficient_mid: float = Field(
        ..., description="Midseason crop coefficient", alias="kc_mid"
    )
    crop_coefficient_end_min: float = Field(
        ...,
        description="Endseason crop coefficient (minimum)",
        alias="kc_end_min",
    )
    crop_coefficient_end_max: float = Field(
        ...,
        description="Endseason crop coefficient (maximum)",
        alias="kc_end_max",
    )
    growth_stage_ini_d: int = Field(
        ..., description="Length of initial growth stage [days]", alias="l_ini"
    )
    growth_stage_dev_d: int = Field(
        ...,
        description="Length of development growth stage [days]",
        alias="l_dev",
    )
    growth_stage_mid_d: int = Field(
        ..., description="Length of middle growth stage [days]", alias="l_mid"
    )
    growth_stage_end_d: int = Field(
        ..., description="Length of ending growth stage [days]", alias="l_end"
    )
    max_crop_height_m: float = Field(
        ..., description="Maximum crop height [meters]", alias="h_max"
    )
    max_root_depth_max_m: float = Field(
        ..., description="Maximum root depth [meters]", alias="zr_max_max"
    )
    max_root_depth_min_m: float = Field(
        ..., description="Minimum root depth [meters]", alias="zr_max_min"
    )
    min_root_depth_m: float = Field(
        ..., description="Minimum root depth [meters]", alias="zr_min"
    )
    sowing_to_emergence_d: int = Field(
        ...,
        description="Time from sowing to emergence [days]",
        alias="l_emergence",
    )
    const_depletion_factor: float = Field(
        ..., description="Depletion factor", alias="p"
    )

    sowing_to_max_rooting_depth_d: int = Field(
        20, description="Time from sowing to maximum rooting depth [days]"
    )
    start_root_depth_pct: float = Field(
        50, description="Virtual starting root depth [%]", alias="z0_pct"
    )
    yield_max_min: float = Field(
        0.6, description="Yield max (minimum)", alias="y_max_min"
    )
    yield_max_max: float = Field(
        1.4, description="Yield max (maximum)", alias="y_max_max"
    )

    yield_response_factor_total: float = Field(
        ...,
        description="Yield response factor (total period)",
        alias="k_y_total",
    )

    @property
    def crop_coefficient_end(self) -> float:
        return (
            self.crop_coefficient_end_min + self.crop_coefficient_end_max
        ) / 2

    @property
    def max_root_depth_m(self) -> float:
        return (self.max_root_depth_min_m + self.max_root_depth_max_m) / 2

    @property
    def yield_max(self) -> float:
        return (self.yield_max_min + self.yield_max_max) / 2
