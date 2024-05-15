"""Model class."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from mashumaro import DataClassDictMixin, field_options
from mashumaro.types import SerializationStrategy

from .helpers import camel2snake, doors_status, lights_status, windows_status


class Locked(SerializationStrategy):
    def serialize(self, value: str) -> str:
        return value

    def deserialize(self, value: str) -> bool:
        return value == "locked"


class OnOff(SerializationStrategy):
    def serialize(self, value: str) -> str:
        return value

    def deserialize(self, value: str) -> bool:
        return value != "off"


@dataclass
class Base(DataClassDictMixin):
    @classmethod
    def __pre_deserialize__(cls, d: dict[Any, Any]) -> dict[Any, Any]:
        if isinstance(d, dict):
            return {camel2snake(k): v for k, v in d.items()}
        return d


# SECTION
@dataclass
class Position(Base):
    longitude: float | None = field(metadata=field_options(alias="lon"), default=None)
    latitude: float | None = field(metadata=field_options(alias="lat"), default=None)
    last_access: datetime | None = field(
        metadata=field_options(alias="car_captured_timestamp"), default=None
    )


# SECTION
@dataclass
class Location(Base):
    proprietaries: list[dict[str, Any]] | None = None
    addresses: list[dict[str, Any]] | None = None


# SECTION
@dataclass
class Access(Base):
    access_status: AccessStatus | None = None


@dataclass
class AccessStatus(Base):
    """Return accessStatus."""

    car_captured_timestamp: datetime
    overall_status: str | None = None
    door_lock_status: bool | None = field(
        metadata=field_options(serialization_strategy=Locked()),
        default=None,
    )
    doors: dict[str, Any] | None = field(
        metadata=field_options(deserialize=doors_status), default=None
    )
    windows: dict[str, Any] | None = field(
        metadata=field_options(deserialize=windows_status), default=None
    )


# SECTION
@dataclass
class Charging(Base):
    battery_status: BatteryStatus | None = None
    charging_status: ChargingStatus | None = None
    charging_settings: ChargingSettings | None = None
    plug_status: PlugStatus | None = None
    charge_mode: ChargeMode | None = None


@dataclass
class BatteryStatus(Base):
    current_soc_pct: int | None = field(
        metadata=field_options(alias="currentSOC_pct"), default=None
    )
    cruising_range_electric_km: int | None = None


@dataclass
class ChargingStatus(Base):
    remaining: int | None = field(
        metadata=field_options(alias="remainingChargingTimeToComplete_min"),
        default=None,
    )
    charging_state: bool | None = field(
        metadata=field_options(deserialize=lambda x: x == "charging"), default=None
    )
    charge_mode: str | None = None
    charge_power_kw: float | None = None
    charge_rate_kmph: int | None = None
    charge_type: str | None = None
    charge_settings: str | None = None


@dataclass
class ChargingSettings(Base):
    max_charge_current_ac: str | None = None
    aut_unlock_plug_when_charged: bool | None = field(
        metadata=field_options(serialization_strategy=OnOff()), default=None
    )
    auto_unlock_plug_when_charged_ac: bool | None = field(
        metadata=field_options(serialization_strategy=OnOff()), default=None
    )
    target_soc_pct: int | None = field(
        metadata=field_options(alias="targetSOC_pct"), default=None
    )


@dataclass
class PlugStatus(Base):
    plug_connection_state: int | None = field(
        metadata=field_options(deserialize=lambda x: x == "connected"), default=None
    )
    plug_lock_state: bool | None = field(
        metadata=field_options(serialization_strategy=Locked()), default=None
    )
    external_power: str | None = None
    led_color: str | None = None


@dataclass
class ChargeMode(Base):
    preferred_charge_mode: str | None = None
    available_charge_modes: list[str] | None = None


# SECTION
@dataclass
class Climatisation(Base):
    window_heating_status: WindowHeatingStatus | None = None
    climatisation_status: ClimatisationStatus | None = None
    climatisation_settings: ClimatisationSettings | None = None


@dataclass
class WindowHeatingStatus(Base):
    window_heating_status: list[dict[str, str]] | None = None


@dataclass
class ClimatisationStatus(Base):
    remaining_climatisation_time_min: int | None = None
    climatisation_state: bool | None = field(
        metadata=field_options(serialization_strategy=OnOff()), default=None
    )


@dataclass
class ClimatisationSettings(Base):
    target_temperature_C: int | None = None
    target_temperature_F: int | None = None
    unit_in_car: str | None = None
    climatization_at_unlock: bool | None = None
    window_heating_enabled: bool | None = None
    zone_front_left_enabled: bool | None = None
    zone_front_right_enabled: bool | None = None
    zone_rear_left_enabled: bool | None = None
    zone_rear_right_enabled: bool | None = None


# SECTION
@dataclass
class ClimatisationTimers(Base):
    climatisation_timers_status: ClimatisationTimersStatus | None = None


@dataclass
class ClimatisationTimersStatus(Base):
    time_in_car: datetime | None = field(
        metadata=field_options(
            deserialize=lambda x: datetime.strptime(x, "%Y-%m-%dT%H:%M:%S%z")
        ),
        default=None,
    )
    timers: list[Timer] | None = None


@dataclass
class Timer(Base):
    id: int
    enabled: bool
    single_timer: SingleTimer


@dataclass
class SingleTimer(Base):
    start: datetime = field(metadata=field_options(alias="startDateTime"))
    target: datetime = field(metadata=field_options(alias="targetDateTime"))


# SECTION
@dataclass
class FuelStatus(Base):
    range_status: FuelRangeStatus | None = None


@dataclass
class FuelRangeStatus(Base):
    car_type: str | None = None
    primary_engine: PrimaryEngine | None = None
    secondary_engine: SecondaryEngine | None = None
    total_range_km: int | None = None


@dataclass
class PrimaryEngine(Base):
    type: str | None = None
    current_soc_pct: str | None = None
    remaining_range_km: int | None = None
    current_fuel_level_pct: int | None = None


@dataclass
class SecondaryEngine(Base):
    type: str | None = None
    current_soc_pct: str = None
    remaining_range_km: int | None = None
    current_fuel_level_pct: int | None = None


# SECTION
@dataclass
class OilLevel(Base):
    oil_level_status: OilLevelStatus | None = None


@dataclass
class OilLevelStatus(Base):
    value: bool


# SECTION
@dataclass
class VehicleLights(Base):
    lights_status: LightsStatus | None = None


@dataclass
class LightsStatus(Base):
    lights: dict[str, Any] | None = field(
        metadata=field_options(deserialize=lights_status), default=None
    )


# SECTION
@dataclass
class VehicleHealthInspection(Base):
    maintenance_status: MaintenanceStatus | None = None


@dataclass
class MaintenanceStatus(Base):
    inspection_due_days: int | None = None
    inspection_due_km: int | None = None
    mileage_km: int | None = None
    oil_service_due_days: int | None = None
    oil_service_due_km: int | None = None


# SECTION
@dataclass
class Measurements(Base):
    range_status: RangeStatus | None = None
    odometer_status: OdometerStatus | None = None
    fuel_level_status: FuelLevelStatus | None = None
    temperature_battery_status: TemperatureBatteryStatus | None = None


@dataclass
class RangeStatus(Base):
    electric_range: int | None = None
    gasoline_range: int | None = None
    total_range_km: int | None = None


@dataclass
class OdometerStatus(Base):
    odometer: int | None = None


@dataclass
class FuelLevelStatus(Base):
    current_soc_pct: int | None = None
    current_fuel_level_pct: int | None = None
    primary_engine_type: str | None = None
    secondary_engine_type: str | None = None
    car_type: str | None = None


@dataclass
class TemperatureBatteryStatus(Base):
    temperature_hv_battery_max_k: float
    temperature_hv_battery_min_k: float


# SECTION
@dataclass
class VehicleHealthWarnings(Base):
    warning_lights: WarningLights | None = None


@dataclass
class WarningLights(Base):
    lights: dict[str, Any] | None = field(
        metadata=field_options(deserialize=lights_status), default=None
    )


@dataclass
class UserCapabilities(Base):
    capabilities_status: list[dict[str, Any]] | None = None


# SECTION
@dataclass
class Model(Base):
    """Vehicle."""

    user_capabilities: UserCapabilities | None = None
    access: Access | None = None
    charging: Charging | None = None
    climatisation_timers: ClimatisationTimers | None = None
    climatisation: Climatisation | None = None
    fuel_status: FuelStatus | None = None
    vehicle_health_inspection: VehicleHealthInspection | None = None
    vehicle_lights: VehicleLights | None = None
    measurements: Measurements | None = None
    oil_level: OilLevel | None = None
    vehicle_health_warnings: VehicleHealthWarnings | None = None
