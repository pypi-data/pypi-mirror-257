from nautobot.extras.plugins import PluginConfig


class EVPNConfig(PluginConfig):
    name = 'nautobot_evpn'
    verbose_name = 'EVPN'
    description = 'A plugin for evpn management'
    version = '1.0.0'
    author = "Gesellschaft für wissenschaftliche Datenverarbeitung mbH Göttingen"
    author_email = "netzadmin@gwdg.de"
    base_url = 'nautobot_evpn'


config = EVPNConfig
