# Moon Phase Custom Component for Home Assistant

This Home Assistant custom component provides moon phase information including visibility, distance, altitude, next full moon, next new moon, moonrise, moonset, phase, illumination, and age in days, based on your location set in Home Assistant.

## Installation

To use this custom component, you need to have Home Assistant installed. If you haven't installed Home Assistant, follow the [installation guide](https://www.home-assistant.io/getting-started/) before proceeding.

1. Copy the `moon_phase` directory into your Home Assistant's `custom_components` directory. If the `custom_components` directory does not exist, you will need to create it.

    ```
   /custom_components/moon_phase
    ```

2. Restart Home Assistant to apply the changes.

## Configuration

To enable the Moon Phase custom component, add the following to your `configuration.yaml` file:

```yaml
sensor:
  - platform: moon_phase
```

## Usage
Once installed and configured, the Moon Phase custom component will create `moon_phase` sensor that you can use in Home Assistant automations, scripts, or display on the user interface.

## Sensor Attributes
- `latitude`: Latitude of the location.
- `longitude`: Longitude of the location.
- `phase`: Current moon phase represented as a float value ranging from 0 to 1.
- `visible`: Percentage of moon's elongation, indicating its visibility.
- `distance`: Distance from Earth to the moon in kilometers.
- `altitude`: Altitude of the moon in degrees.
- `next_full_moon`: Date and time of the next full moon.
- `next_new_moon`: Date and time of the next new moon.
- `days_to_full_moon`: Number of days until the next full moon.
- `days_to_new_moon`: Number of days until the next new moon.
- `today_moonrise`: Date and time of today's moonrise.
- `today_moonset`: Date and time of today's moonset.
- `illumination`: Percentage of moon's illumination.
- `age_days`: Age of the moon in days.
