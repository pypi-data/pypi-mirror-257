from typing import Literal

from pydantic import BaseModel, Field

SoilType = Literal[
    "sand",
    "loamy sand",
    "sandy loam",
    "loam",
    "silt loam",
    "silt",
    "silt clay loam",
    "silty clay",
    "clay",
]


class Soil(BaseModel):
    kind: SoilType = Field(description="Soil type", alias="soil_type")
    theta_fc_max: float = Field(
        description="Water content at field capacity (maximum)"
    )
    theta_fc_min: float = Field(
        description="Water content at field capacity (minimum)"
    )
    theta_wp_max: float = Field(
        description="Water content at wilting point (maximum)"
    )
    theta_wp_min: float = Field(
        description="Water content at wilting point (minimum)"
    )

    @property
    def theta_fc(self):
        """
        Water content at field capacity (average)
        """
        return (self.theta_fc_max + self.theta_fc_min) / 2

    @property
    def theta_wp(self):
        """
        Water content at wilting point (average)
        """
        return (self.theta_wp_max + self.theta_wp_min) / 2
