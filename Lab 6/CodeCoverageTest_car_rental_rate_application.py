# Lab 6 - Code (Line) Coverage test cases
# Target: >=90% line coverage for car_rental_rate.py
import pytest
from car_rental_rate import process_rental_fleet, check_fleet_telematics


def test_invalid_rentals_not_a_list():
    with pytest.raises(ValueError):
        process_rental_fleet("not-a-list", 10.0)


def test_invalid_negative_admin_fee():
    with pytest.raises(ValueError):
        process_rental_fleet([], -5.0)


def test_unconfirmed_rentals_give_empty_batch():
    result = process_rental_fleet([{"is_confirmed": False}], 10.0)
    assert result["status"] == "EMPTY_BATCH"
    assert result["total_revenue"] == 0.0


def test_zero_days_is_flagged_and_skipped():
    result = process_rental_fleet([{"is_confirmed": True, "days": 0}], 10.0)
    assert result["status"] == "EMPTY_BATCH"


def test_luxury_young_driver():
    rentals = [{"is_confirmed": True, "vehicle_type": "luxury",
                "driver_age": 20, "days": 1, "trip_segments": []}]
    assert process_rental_fleet(rentals, 10.0)["total_revenue"] == 180.0


def test_suv_short_trip():
    rentals = [{"is_confirmed": True, "vehicle_type": "suv",
                "driver_age": 24, "days": 3, "trip_segments": [200]}]
    assert process_rental_fleet(rentals, 10.0)["total_revenue"] == 320.0


def test_economy_small_miles():
    rentals = [{"is_confirmed": True, "vehicle_type": "economy",
                "driver_age": 24, "days": 2, "trip_segments": [50]}]
    assert process_rental_fleet(rentals, 10.0)["total_revenue"] == 140.0


def test_negative_miles_flagged():
    rentals = [{"is_confirmed": True, "vehicle_type": "economy",
                "driver_age": 22, "days": 1, "trip_segments": [-10, 50]}]
    assert process_rental_fleet(rentals, 10.0)["total_revenue"] == 80.0


def test_long_trip_young_driver_surcharge():
    rentals = [{"is_confirmed": True, "vehicle_type": "economy",
                "driver_age": 20, "days": 1, "trip_segments": [400, 50]}]
    assert process_rental_fleet(rentals, 10.0)["total_revenue"] == 320.0


def test_long_trip_per_mile_rate():
    rentals = [{"is_confirmed": True, "vehicle_type": "economy",
                "driver_age": 22, "days": 1, "trip_segments": [400]}]
    assert process_rental_fleet(rentals, 10.0)["total_revenue"] == 230.0


def test_high_risk_audit():
    rentals = [{"is_confirmed": True, "vehicle_type": "economy",
                "driver_age": 22, "days": 1, "trip_segments": [-1, -1, -1, -1, -1]}]
    assert process_rental_fleet(rentals, 10.0)["status"] == "HIGH_RISK_AUDIT"


def test_telematics_no_data():
    assert check_fleet_telematics([]) == "NO_DATA"


def test_telematics_ground_vehicle():
    assert check_fleet_telematics([[101, 102]]) == "GROUND_VEHICLE"


def test_telematics_safe_with_reset():
    assert check_fleet_telematics([[101, 50, 101]]) == "SAFE"
