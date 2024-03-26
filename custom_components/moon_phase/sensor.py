"""Platform for retrieving the moon phase."""
import logging
import math
from homeassistant.helpers.entity import Entity
import ephem
from datetime import datetime

_LOGGER = logging.getLogger(__name__)

MOON_PHASE_ICON = {
    "New Moon": "mdi:moon-new",
    "First Quarter": "mdi:moon-first-quarter",
    "Full Moon": "mdi:moon-full",
    "Last Quarter": "mdi:moon-last-quarter",
}

def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the Moon Phase sensor."""
    _LOGGER.debug("Setting up Moon Phase sensor")
    add_entities([MoonPhaseSensor()])


class MoonPhaseSensor(Entity):
    """Representation of a Moon Phase sensor."""

    def __init__(self):
        """Initialize the sensor."""
        _LOGGER.debug("Initializing Moon Phase sensor")
        self._state = None
        self._attr = {}
        self._icon = None

    @property
    def name(self):
        """Return the name of the sensor."""
        return "Moon Phase"

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def icon(self):
        """Return the icon of the sensor."""
        return self._icon

    @property
    def state_attributes(self):
        """Return the state attributes."""
        return self._attr

    async def async_update(self):
        """Calculate the current moon phase and additional attributes."""
        _LOGGER.debug("Updating Moon Phase sensor")

        # Get latitude and longitude from Home Assistant configuration
        latitude = self.hass.config.latitude
        longitude = self.hass.config.longitude

        observer = ephem.Observer()
        observer.lat = str(latitude)
        observer.lon = str(longitude)
        observer.date = datetime.utcnow()

        moon = ephem.Moon(observer)

        # Calculate moon visibility
        visible = moon.elong / ephem.pi * 100  # Calculate percentage of moon's elongation
        _LOGGER.debug("Moon is visible: %s%%", visible)

        # Calculate moon distance
        distance = moon.earth_distance * ephem.meters_per_au
        _LOGGER.debug("Moon distance (km): %s", distance)

        # Calculate moon altitude
        altitude = float(moon.alt) * 180 / ephem.pi
        _LOGGER.debug("Moon altitude (degrees): %s", altitude)

        # Calculate next full moon
        next_full_moon = ephem.next_full_moon(observer.date)
        next_full_moon_datetime = ephem.localtime(next_full_moon)
        days_to_full_moon = (next_full_moon_datetime.date() - datetime.utcnow().date()).days
        _LOGGER.debug("Next full moon: %s", next_full_moon_datetime)
        _LOGGER.debug("Days to full moon: %s", days_to_full_moon)

        # Calculate next new moon
        next_new_moon = ephem.next_new_moon(observer.date)
        next_new_moon_datetime = ephem.localtime(next_new_moon)
        days_to_new_moon = (next_new_moon_datetime.date() - datetime.utcnow().date()).days
        _LOGGER.debug("Next new moon: %s", next_new_moon_datetime)
        _LOGGER.debug("Days to new moon: %s", days_to_new_moon)


        # Calculate moonrise and moonset for today
        today_moonrise = observer.previous_rising(moon)
        today_moonrise_datetime = ephem.localtime(today_moonrise)
        today_moonset = observer.next_setting(moon)
        today_moonset_datetime = ephem.localtime(today_moonset)
        _LOGGER.debug("Today's moonrise: %s", today_moonrise_datetime)
        _LOGGER.debug("Today's moonset: %s", today_moonset_datetime)

        # Calculate moon phase
        phase = moon.phase / 100  # Convert phase from percentage to range (0, 1)
        _LOGGER.debug("Phase angle: %s", phase)
        if 0 < phase < 0.125:
            self._state = "New Moon"
        elif 0.125 <= phase < 0.375:
            self._state = "First Quarter"
        elif 0.375 <= phase < 0.625:
            self._state = "Full Moon"
        elif 0.625 <= phase < 0.875:
            self._state = "Last Quarter"
        else:
            self._state = "New Moon"

        # Calculate moon illumination
        illumination = (1 + math.cos(math.radians(phase * 360))) / 2 * 100
        _LOGGER.debug("Moon illumination: %s%%", illumination)

        # Calculate moon age in days
        age_days = observer.date - ephem.previous_new_moon(observer.date)
        _LOGGER.debug("Moon age (days): %s", age_days)

        # Update attributes
        self._attr.update({
            "latitude": latitude,
            "longitude": longitude,
            "phase": phase,
            "visible": visible,
            "distance": distance,
            "altitude": altitude,
            "next_full_moon": next_full_moon_datetime.isoformat(),
            "next_new_moon": next_new_moon_datetime.isoformat(),
            "days_to_full_moon": days_to_full_moon,
            "days_to_new_moon": days_to_new_moon,
            "today_moonrise": today_moonrise_datetime.isoformat(),
            "today_moonset": today_moonset_datetime.isoformat(),
            "illumination": illumination,
            "age_days": age_days,
        })

        # Update icon based on moon phase
        self._icon = MOON_PHASE_ICON.get(self._state, "mdi:moon-waning-crescent")

        _LOGGER.debug("Moon Phase sensor updated to: %s", self._state)
