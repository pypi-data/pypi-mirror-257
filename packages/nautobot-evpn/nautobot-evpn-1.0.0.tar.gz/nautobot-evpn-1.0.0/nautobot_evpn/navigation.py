from nautobot.apps.ui import NavMenuTab, NavMenuItem, NavMenuButton, NavMenuGroup
from nautobot.core.choices import ButtonColorChoices


menu_items = (
    NavMenuTab(
        name="Plugins",
        groups=[
            NavMenuGroup(name="EVPN", items=[
                NavMenuItem(
                    link='plugins:nautobot_evpn:ethernetsegment_list',
                    name="Ethernet Segments",
                    permissions=["dcim.view_ethernet_segment"],
                    buttons=[
                        NavMenuButton(
                            link='plugins:nautobot_evpn:ethernetsegment_add',
                            title="Add Ethernet Segment",
                            icon_class="mdi mdi-plus-thick",
                            button_class=ButtonColorChoices.GREEN
                        ),
                        NavMenuButton(
                            link='plugins:nautobot_evpn:ethernetsegment_import',
                            title="Import Ethernet Segments",
                            icon_class="mdi mdi-database-import-outline",
                            button_class=ButtonColorChoices.BLUE
                        ),
                        NavMenuButton(
                            link='plugins:nautobot_evpn:esm-import',
                            title="Import Ethernet Segment Membership",
                            icon_class="mdi mdi-database-import-outline",
                            button_class=ButtonColorChoices.YELLOW
                        ),
                    ]
                ),
            ]),
        ],
    ),
)
