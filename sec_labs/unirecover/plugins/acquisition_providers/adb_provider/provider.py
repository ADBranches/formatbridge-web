import json

class AdbProviderPlugin:
    def __init__(self):
        self.name = "ADB_PROVIDER"

    def query_target_properties(self):
        return {
            "status": "online",
            "transport": "usb_bulk",
            "capabilities": ["partition_dump", "logcat_carve"]
        }
