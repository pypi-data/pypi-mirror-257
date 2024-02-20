from datetime import date, datetime, timedelta
from typing import Dict, Literal, Optional, cast

import pytz
from datetimerange import DateTimeRange

from fao56_model.data_models.crop import Crop

CropStage = Literal["ini", "dev", "mid", "end"]


class PlantedCrop(object):
    def __init__(self, crop: Crop, sowing_date: date):
        self.crop = crop
        self._set_dates(
            datetime.combine(sowing_date, datetime.min.time(), tzinfo=pytz.UTC)
        )
        self._crop_coefficient_ini_correct: Optional[float] = None
        self._crop_coefficient_mid_correct: Optional[float] = None
        self._crop_coefficient_end_correct: Optional[float] = None

    def set_coefficients(self, kc_ini: float, kc_mid: float, kc_end: float):
        """
        Set the corrected crop coefficients
        """
        self._crop_coefficient_ini_correct = kc_ini
        self._crop_coefficient_mid_correct = kc_mid
        self._crop_coefficient_end_correct = kc_end

    @property
    def crop_coefficient_ini_correct(self) -> float:
        """
        Returns the corrected crop coefficient for the initial stage
        """
        if self._crop_coefficient_ini_correct is None:
            raise ValueError("Corrected crop coefficients not set")
        return self._crop_coefficient_ini_correct

    @property
    def crop_coefficient_mid_correct(self) -> float:
        """
        Returns the corrected crop coefficient for the mid stage
        """
        if self._crop_coefficient_mid_correct is None:
            raise ValueError("Corrected crop coefficients not set")
        return self._crop_coefficient_mid_correct

    @property
    def crop_coefficient_end_correct(self) -> float:
        """
        Returns the corrected crop coefficient for the end stage
        """
        if self._crop_coefficient_end_correct is None:
            raise ValueError("Corrected crop coefficients not set")
        return self._crop_coefficient_end_correct

    def _set_dates(self, sowing_date: datetime) -> None:
        self.sowing_date = sowing_date
        initial_end = self.sowing_date + timedelta(
            days=self.crop.growth_stage_ini_d
        )
        development_end = initial_end + timedelta(
            days=self.crop.growth_stage_dev_d
        )
        mid_end = development_end + timedelta(
            days=self.crop.growth_stage_mid_d
        )
        end_end = mid_end + timedelta(days=self.crop.growth_stage_end_d)

        self.initial_stage = DateTimeRange(self.sowing_date, initial_end)
        self.development_stage = DateTimeRange(initial_end, development_end)
        self.mid_stage = DateTimeRange(development_end, mid_end)
        self.end_stage = DateTimeRange(mid_end, end_end)
        self.growing_period = (
            self.initial_stage.encompass(self.development_stage)
            .encompass(self.mid_stage)
            .encompass(self.end_stage)
        )
        self.harvest_date = cast(
            datetime, self.growing_period.end_datetime
        ).date()
        self.stages: Dict[CropStage, DateTimeRange] = {
            "ini": self.initial_stage,
            "dev": self.development_stage,
            "mid": self.mid_stage,
            "end": self.end_stage,
        }

    def get_crop_coefficient(self, current_date: date) -> float:
        """
        Returns the crop coefficient for the given date
        using linear interpolation for the development stage
        """
        current_datetime = datetime.combine(
            current_date, datetime.min.time(), tzinfo=pytz.UTC
        )
        stage = self.get_crop_stage(current_datetime)
        coefficients: Dict[CropStage, float] = {
            "ini": self.crop_coefficient_ini_correct,
            "mid": self.crop_coefficient_mid_correct,
            "end": self.crop_coefficient_end_correct,
        }
        if stage == "dev":
            current_timedelta = DateTimeRange(
                self.initial_stage.end_datetime, current_datetime
            ).timedelta
            dev_timedelta = self.development_stage.timedelta
            return self.crop_coefficient_ini_correct + (
                current_timedelta / dev_timedelta
            ) * (
                self.crop_coefficient_mid_correct
                - self.crop_coefficient_ini_correct
            )
        else:
            return coefficients[stage]

    def get_crop_stage(self, current_datetime: datetime) -> CropStage:
        """
        Determine the crop stage based on the current date.
        """
        stages: Dict[CropStage, DateTimeRange] = {
            "ini": self.initial_stage,
            "dev": self.development_stage,
            "mid": self.mid_stage,
            "end": self.end_stage,
        }
        for stage_name, stage_range in stages.items():
            if current_datetime in stage_range:
                return stage_name
        raise ValueError("Date is not within the growing period")

    def get_corrected_crop_coefficient_w_correlation(
        self, default_crop_coefficient: float, u_mean_ms: float, RH_min: float
    ) -> float:
        """
        Crop coefficient correlation
        """
        return default_crop_coefficient + (
            0.04 * (u_mean_ms - 2) - 0.004 * (RH_min - 45)
        ) * (self.crop.max_crop_height_m / 3)

    def get_rooting_depth(self, current_date: datetime) -> float:
        """
        Returns the rooting depth [meters]
        """
        if current_date not in self.growing_period:
            raise ValueError("Date is not within the growing period")
        t = (current_date - self.sowing_date).days
        t_x = self.crop.sowing_to_max_rooting_depth_d
        t_0 = self.crop.sowing_to_emergence_d
        z_0 = (
            self.crop.start_root_depth_pct / 100.0 * self.crop.min_root_depth_m
        )

        z_max = self.crop.max_root_depth_m
        z_min = self.crop.min_root_depth_m
        z = z_0 + (z_max - z_0) * (t - t_0 / 2) / (t_x - t_0 / 2)
        z_r = min(max(z_min, z), z_max)
        return z_r

    def get_relative_yield_factor(self, ET_rel: float) -> float:
        """
        Returns the relative yield factor given relative evapotranspiration [-]
        """
        return max(0, 1 - self.crop.yield_response_factor_total * (1 - ET_rel))
