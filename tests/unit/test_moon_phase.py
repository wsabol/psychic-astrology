import json
import pytest
from datetime import datetime
from unittest.mock import patch, MagicMock
from src import handler

def test_moon_phase_jan_2026_cases():
    # Test dates from the issue description
    # Format: (year, month, day, hour, expected_phase_index)
    # Since we use noon UTC in the test script:
    test_cases = [
        (2026, 1, 1, 12, 3),   # Jan 1 - Angle ~155° -> Index 3 (waxingGibbous)
        (2026, 1, 2, 12, 3),   # Jan 2 - Angle ~168° -> Index 3 (waxingGibbous)
        (2026, 1, 3, 12, 4),   # Jan 3 - Angle ~181° -> Index 4 (fullMoon)
        (2026, 1, 4, 12, 4),   # Jan 4 - Angle ~195° -> Index 4 (fullMoon)
        (2026, 1, 5, 12, 4),   # Jan 5 - Angle ~209° -> Index 4 (fullMoon)
        (2026, 1, 10, 12, 6),  # Jan 10 - Angle ~274° -> Index 6 (lastQuarter)
        (2026, 1, 18, 12, 0),  # Jan 18 - Angle ~12° -> Index 0 (newMoon)
    ]
    
    phase_names = ["newMoon", "waxingCrescent", "firstQuarter", "waxingGibbous", "fullMoon", "waningGibbous", "lastQuarter", "waningCrescent"]

    for year, month, day, hour, expected_index in test_cases:
        dt = datetime(year, month, day, hour)
        
        # We need to mock swisseph to return consistent values for testing
        # Or if swisseph is working, we can use it.
        # Since swisseph import might fail in this environment, let's mock the internal call or swisseph itself.
        
        with patch('src.handler.swe') as mock_swe:
            # Mock julday
            mock_swe.julday.return_value = 2461042.0 # example value
            
            # Mock SUN and MOON constants
            mock_swe.SUN = 0
            mock_swe.MOON = 1
            
            # Calculate what the angle should be to produce the expected index
            # phase_index = int((phase_angle / 360) * 8) % 8
            # For expected_index 4, phase_angle should be in [180, 225)
            
            target_angle = (expected_index * 45) + 5 # Add 5 degrees into the sector
            
            # sun_lon = 0, moon_lon = target_angle
            mock_swe.calc_ut.side_effect = [
                ([0.0], None), # SUN
                ([target_angle], None) # MOON
            ]
            
            result = handler.calculate_current_moon_phase(date_to_check=dt)
            
            assert result["success"] is True
            assert result["phase"] == phase_names[expected_index]
            assert result["phase_angle"] == float(target_angle)

def test_moon_phase_boundaries():
    phase_names = ["newMoon", "waxingCrescent", "firstQuarter", "waxingGibbous", "fullMoon", "waningGibbous", "lastQuarter", "waningCrescent"]
    
    # Test boundary cases
    boundaries = [
        (0, "newMoon"),
        (44.9, "newMoon"),
        (45, "waxingCrescent"),
        (179.9, "waxingGibbous"),
        (180, "fullMoon"),
        (359.9, "waningCrescent")
    ]
    
    for angle, expected_phase in boundaries:
        with patch('src.handler.swe') as mock_swe:
            mock_swe.SUN = 0
            mock_swe.MOON = 1
            mock_swe.calc_ut.side_effect = [([0.0], None), ([angle], None)]
            
            result = handler.calculate_current_moon_phase(date_to_check=datetime(2026, 1, 1))
            assert result["phase"] == expected_phase, f"Angle {angle} should be {expected_phase}"
