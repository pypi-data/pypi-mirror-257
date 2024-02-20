from datetime import date, timedelta
from typing import List, Tuple, cast

import pandas as pd

from fao56_model.crop_calendar import CropCalendar
from fao56_model.data_models.climate import ClimateData
from fao56_model.data_models.simulation_state import SimulationState
from fao56_model.data_models.soil import Soil


class CropSimulation:
    def __init__(
        self, calendar: CropCalendar, soil: Soil, climate_date: ClimateData
    ):
        self.calendar = calendar
        self.climate_data = climate_date
        self.soil = soil
        if not self.climate_data_is_within_range():
            raise ValueError(
                "Climate data does not cover the crop calendar range"
            )
        self.initialize_states()

    def climate_data_is_within_range(self) -> bool:
        """
        Check if the data is within the crop calendar range
        """
        return self.calendar.time_range in self.climate_data.time_range

    def get_total_available_water(self, rooting_depth: float) -> float:
        """
        Returns the total available water for the given rooting depth
        """
        return (
            1000
            * (self.soil.theta_fc - self.soil.theta_wp)
            * 0.5
            * rooting_depth
        )

    def initialize_states(self) -> None:
        """
        Initialize the states with the climate data and the soil data
        """
        self.states = [
            SimulationState(
                timestamp=d.timestamp,
                ET_0=d.ET_0,
                precipation_mm=d.precipation_mm,
            )
            for d in self.climate_data.data_points
        ]
        # initialize the root zone depletion to
        # the readily available water one day before the sowing date
        crop_start_times = [c.sowing_date for c in self.calendar.planted_crops]
        for i, state in enumerate(self.states):
            if state.timestamp in crop_start_times:
                crop = self.calendar.get_crop(state.timestamp)
                assert crop
                self.states[i - 1].Z_r = crop.crop.min_root_depth_m
                self.states[i - 1].D_r = self.get_total_available_water(
                    crop.crop.min_root_depth_m
                )
                break

    def run(self) -> None:
        """
        Run the simulation
        """
        for i, state in enumerate(self.states[1:]):
            idx = i + 1
            prev_state = self.states[idx - 1]
            planted_crop = self.calendar.get_crop(state.timestamp)
            if planted_crop:
                assert prev_state.D_r is not None
                state.K_c_correct = planted_crop.get_crop_coefficient(
                    state.timestamp
                )
                state.ET_c = state.K_c_correct * state.ET_0
                state.d = planted_crop.crop.const_depletion_factor + 0.04 * (
                    5 - state.ET_c
                )
                state.Z_r = planted_crop.get_rooting_depth(state.timestamp)
                state.TAW = self.get_total_available_water(state.Z_r)
                state.RAW = state.d * state.TAW
                state.D_r = (
                    state.TAW
                    * (
                        -prev_state.D_r * state.d
                        + prev_state.D_r
                        + state.ET_c
                        + state.I_del * state.d
                        - state.I_del
                        + state.precipation_mm * state.d
                        - state.precipation_mm
                        - state.RO * state.d
                        + state.RO
                    )
                ) / (state.ET_c - state.TAW * state.d + state.TAW)
                state.D_r = max(min(state.D_r, state.TAW), 0)
                state.K_s = 1
                if state.D_r > state.RAW:
                    state.K_s = (state.TAW - state.D_r) / (
                        (1 - state.d) * state.TAW
                    )
                state.ET_a = state.K_s * state.ET_c
                state.ET_rel = state.ET_a / state.ET_0
                state.Y_rel = planted_crop.get_relative_yield_factor(
                    state.ET_rel
                )

    def calc_yield(self) -> List[Tuple[date, float, float]]:
        """
        Calculate the yield
        """
        crops = [crop for crop in self.calendar.planted_crops]
        harvest_dates = [c.harvest_date for c in self.calendar.planted_crops]
        ls_actual_yields = []
        ls_max_yields = [crop.crop.yield_max for crop in crops]
        for crop in crops:
            period = crop.growing_period
            timestamps = [d for d in period.range(timedelta(days=1))]
            Y_rel = [
                cast(float, s.Y_rel)
                for s in self.states
                if s.timestamp in timestamps
            ]
            avg_Y_rel = sum(Y_rel) / len(Y_rel)
            actual_yield = crop.crop.yield_max * avg_Y_rel
            ls_actual_yields.append(actual_yield)
        return list(zip(harvest_dates, ls_actual_yields, ls_max_yields))

    @property
    def df(self) -> pd.DataFrame:
        return pd.DataFrame([s.model_dump() for s in self.states])
