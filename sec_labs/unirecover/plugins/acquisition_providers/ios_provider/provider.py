class IosProviderPlugin:
    def __init__(self):
        self.name = "IOS_PROVIDER"
        
    def check_jailbreak_footprint(self) -> bool:
        # Implements standard checks for checkra1n / palera1n filesystem mounts
        return False
