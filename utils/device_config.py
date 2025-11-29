from typing import List, Dict, Any

class DeviceConfig:
    MOBILE = {'width': 375, 'height': 667, 'type': 'mobile'}
    TABLET = {'width': 768, 'height': 1024, 'type': 'tablet'}
    DESKTOP = {'width': 1920, 'height': 1080, 'type': 'desktop'}
    DESKTOP_HD = {'width': 1366, 'height': 768, 'type': 'desktop'}

    @classmethod
    def get_all_devices(cls):
        return [cls.MOBILE, cls.TABLET, cls.DESKTOP, cls.DESKTOP_HD]

    @classmethod
    def get_mobile_devices(cls):
        return [cls.MOBILE]

    @classmethod
    def get_desktop_devices(cls):
        return [cls.DESKTOP, cls.DESKTOP_HD]