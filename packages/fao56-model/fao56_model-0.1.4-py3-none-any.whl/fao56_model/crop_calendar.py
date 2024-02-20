from datetime import date, datetime
from typing import List, Optional, Tuple

from fao56_model.data_models.climate import ClimateData
from fao56_model.data_models.crop import Crop
from fao56_model.planted_crop import PlantedCrop
from fao56_model.utils import is_overlapping


class CropCalendar:
    def __init__(self, crop_plus_sowing: List[Tuple[Crop, date]]) -> None:
        self.set_crops(crop_plus_sowing)

    def set_crops(self, crop_plus_sowing: List[Tuple[Crop, date]]) -> None:
        self.planted_crops: List[PlantedCrop] = []
        for c, d in crop_plus_sowing:
            self.planted_crops.append(PlantedCrop(c, d))
        if is_overlapping([pc.growing_period for pc in self.planted_crops]):
            raise ValueError("Overlapping crop growing periods")
        sorted(self.planted_crops, key=lambda pc: pc.sowing_date)

    @property
    def time_range(self):
        period = None
        for planted_crop in self.planted_crops:
            period = (
                planted_crop.growing_period
                if period is None
                else period.encompass(planted_crop.growing_period)
            )
        return period

    def get_crop(self, timestamp: datetime) -> Optional[PlantedCrop]:
        for planted_crop in self.planted_crops:
            if timestamp in planted_crop.growing_period:
                return planted_crop
        return None

    def calendar_range_is_within_climate_data(
        self, climate_data: ClimateData
    ) -> bool:
        return self.time_range in climate_data.time_range

    def set_corrected_crop_coeffients(self, climate_data: ClimateData) -> None:
        if not self.calendar_range_is_within_climate_data(climate_data):
            raise ValueError(
                "Climate data does not cover the crop calendar range"
            )
        for planted_crop in self.planted_crops:
            kc_ini = planted_crop.crop.crop_coefficient_ini
            period_mid = planted_crop.mid_stage
            data_mid = climate_data.get_data_within_range(period_mid)
            umean_mid = sum([d.u_mean_ms for d in data_mid]) / len(data_mid)
            RHmin_mid = sum([d.RH_min for d in data_mid]) / len(data_mid)
            kc_mid = planted_crop.get_corrected_crop_coefficient_w_correlation(
                planted_crop.crop.crop_coefficient_mid, umean_mid, RHmin_mid
            )
            period_end = planted_crop.end_stage
            data_end = climate_data.get_data_within_range(period_end)
            umean_end = sum([d.u_mean_ms for d in data_end]) / len(data_end)
            RHmin_end = sum([d.RH_min for d in data_end]) / len(data_end)
            kc_ini = planted_crop.crop.crop_coefficient_ini
            kc_end = planted_crop.get_corrected_crop_coefficient_w_correlation(
                planted_crop.crop.crop_coefficient_end, umean_end, RHmin_end
            )
            planted_crop.set_coefficients(kc_ini, kc_mid, kc_end)
