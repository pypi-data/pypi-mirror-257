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
        """
        Initializes the PlantedCrops using the sowing dates
        """
        self.planted_crops: List[PlantedCrop] = []
        for c, d in crop_plus_sowing:
            self.planted_crops.append(PlantedCrop(c, d))
        if is_overlapping([pc.growing_period for pc in self.planted_crops]):
            raise ValueError("Overlapping crop growing periods")
        sorted(self.planted_crops, key=lambda pc: pc.sowing_date)

    @property
    def time_range(self):
        """
        Returns the time range of the crop calendar
        """
        period = None
        for planted_crop in self.planted_crops:
            period = (
                planted_crop.growing_period
                if period is None
                else period.encompass(planted_crop.growing_period)
            )
        return period

    def get_crop(self, timestamp: datetime) -> Optional[PlantedCrop]:
        """
        Returns the planted crop for the given timestamp
        """
        for planted_crop in self.planted_crops:
            if timestamp in planted_crop.growing_period:
                return planted_crop
        return None

    def set_corrected_crop_coeffients(self, climate_data: ClimateData) -> None:
        """
        Sets the corrected crop coefficients for the planted crops
        using the climate data
        """
        for planted_crop in self.planted_crops:
            kc_ini = planted_crop.crop.crop_coefficient_ini
            # correct midseason stage coefficient
            period_mid = planted_crop.mid_stage
            data_mid = climate_data.get_data_within_range(period_mid)
            umean_mid = sum([d.wind_speed_2m_ms for d in data_mid]) / len(
                data_mid
            )
            RHmin_mid = sum(
                [d.min_relative_humidity_pct for d in data_mid]
            ) / len(data_mid)
            kc_mid = planted_crop.get_corrected_crop_coefficient_w_correlation(
                planted_crop.crop.crop_coefficient_mid, umean_mid, RHmin_mid
            )
            # correct end stage coefficient
            period_end = planted_crop.end_stage
            data_end = climate_data.get_data_within_range(period_end)
            umean_end = sum([d.wind_speed_2m_ms for d in data_end]) / len(
                data_end
            )
            RHmin_end = sum(
                [d.min_relative_humidity_pct for d in data_end]
            ) / len(data_end)
            kc_end = planted_crop.get_corrected_crop_coefficient_w_correlation(
                planted_crop.crop.crop_coefficient_end, umean_end, RHmin_end
            )
            planted_crop.set_coefficients(kc_ini, kc_mid, kc_end)
