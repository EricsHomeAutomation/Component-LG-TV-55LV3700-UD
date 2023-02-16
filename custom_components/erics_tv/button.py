from __future__ import annotations

from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.components.button import (PLATFORM_SCHEMA, ButtonEntity)

from homeassistant.const import CONF_NAME, CONF_IP_ADDRESS, CONF_CODE

import homeassistant.helpers.config_validation as cv

import requests
import logging

import voluptuous as vol
from pprint import pformat

_LOGGER = logging.getLogger(__name__)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Optional(CONF_NAME): cv.string,
    vol.Required(CONF_IP_ADDRESS): cv.string
})

BUTTONS = {
    "Status Bar": 35,
    "Quick Menu": 69,
    "Home Menu": 67,
    "Premium Menu": 89,
    "Installation Menu": 207,
    "Factory Advanced Menu #1": 251,
    "Factory Advanced Menu #2": 255,
    "Power Off": 8,
    "Sleep Timer": 14,
    "Left": 7,
    "Right": 6,
    "Up": 64,
    "Down": 65,
    "Select": 68,
    "Back": 40,
    "Exit": 91,
    "Red": 114,
    "Green": 113,
    "Yellow": 99,
    "Blue": 97,
    "0": 16,
    "1": 17,
    "2": 18,
    "3": 19,
    "4": 20,
    "5": 21,
    "6": 22,
    "7": 23,
    "8": 24,
    "9": 25,
    "Underscore": 76,
    "Play": 176,
    "Pause": 186,
    "Fast Forward": 142,
    "Rewind": 143,
    "Stop": 177,
    "Record": 189,
    "Tv Radio": 15,
    "Simplink": 126,
    "Input": 11,
    "Component Rgb Hdmi": 152,
    "Component": 191,
    "Rgb": 213,
    "Hdmi": 198,
    "Hdmi #1": 206,
    "Hdmi #2": 204,
    "Hdmi #3": 233,
    "Hdmi #4": 218,
    "Av #1": 90,
    "Av #2": 208,
    "Av #3": 209,
    "Usb": 124,
    "Slideshow Usb #1": 238,
    "Slideshow Usb #2": 168,
    "Channel Up": 0,
    "Channel Down": 1,
    "Channel Back": 26,
    "Favorites": 30,
    "Teletext": 32,
    "T Opt": 33,
    "Channel List": 83,
    "Greyed Out Add Button?": 85,
    "Guide": 169,
    "Info": 170,
    "Live Tv": 158,
    "Av Mode": 48,
    "Picture Mode": 77,
    "Ratio": 121,
    "Ratio 4 3": 118,
    "Ratio 16 9": 119,
    "Energy Saving": 149,
    "Cinema Zoom": 175,
    "3d": 220,
    "Factory Picture Check": 252,
    "Volume Up": 2,
    "Volume Down": 3,
    "Mute": 9,
    "Audio Language": 10,
    "Sound Mode": 82,
    "Factory Sound Check": 253,
    "Subtitle Language": 57,
    "Audio Description": 145
}

HEADER_CONTENT_TYPE = {'Content-Type': 'application/atom+xml'}
XML_HEADER = '<?xml version=\"1.0\" encoding=\"utf-8\"?>'

def setup_platform(hass: HomeAssistant, config: ConfigType, add_entities: AddEntitiesCallback, discovery_info: DiscoveryInfoType | None = None) -> None:
    _LOGGER.info(pformat(config))

    name = config[CONF_NAME]
    ip = config[CONF_IP_ADDRESS]
    
    for key in BUTTONS:
        value = BUTTONS[key]
        add_entities([WebRequestButton(name, ip, key, value)])

class WebRequestButton(ButtonEntity):
    # Implement one of these methods.

    def __init__(self, name, ip, btn_name, btn_code) -> None:
        self._name = name + "_" + btn_name
        self.url = 'http://' + ip + ':8080/hdcp/api/'
        self.btn_code = btn_code

    @property
    def name(self) -> str:
        """Return the display name of this light."""
        return self._name

    async def async_press(self) -> None:
        """Handle the button press."""
        body = XML_HEADER + '<command><session></session><type>HandleKeyInput</type><value>' + code + '</value></command>'
        request = requests.post(url=self.url + 'dtv_wifirc', headers=HEADER_CONTENT_TYPE, data=body)

        if request.resp_code != 200:
            _LOGGER.warning("We didn't get 200: " + request.text)