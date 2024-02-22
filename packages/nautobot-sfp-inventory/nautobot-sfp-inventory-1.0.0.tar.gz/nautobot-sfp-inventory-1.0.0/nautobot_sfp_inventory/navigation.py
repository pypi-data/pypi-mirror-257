from nautobot.core.apps import NavMenuGroup, NavMenuItem, NavMenuTab, NavMenuButton
from nautobot.core.choices import ButtonColorChoices

menu_items = (
    NavMenuTab(
        name="Plugins",
        groups=[
            NavMenuGroup(name="SFP Inventory", items=[
                NavMenuItem(
                    link='plugins:nautobot_sfp_inventory:sfptype_list',
                    name="SFP Types",
                    permissions=["dcim.view_sfps"],
                    buttons=[
                        NavMenuButton(
                            link='plugins:nautobot_sfp_inventory:sfptype_add',
                            title="Add SFP Type",
                            icon_class="mdi mdi-plus-thick",
                            button_class=ButtonColorChoices.GREEN
                        ),
                        NavMenuButton(
                            link='plugins:nautobot_sfp_inventory:sfptype_import',
                            title="Import SFP Types",
                            icon_class="mdi mdi-database-import-outline",
                            button_class=ButtonColorChoices.BLUE
                        ),
                    ]
                ),
                NavMenuItem(
                    link='plugins:nautobot_sfp_inventory:sfp_list',
                    name="SFPs",
                    permissions=["dcim.view_sfps"],
                    buttons=[
                        NavMenuButton(
                            link='plugins:nautobot_sfp_inventory:sfp_add',
                            title="Add SFP",
                            icon_class="mdi mdi-plus-thick",
                            button_class=ButtonColorChoices.GREEN
                        ),
                        NavMenuButton(
                            link='plugins:nautobot_sfp_inventory:sfp_import',
                            title="Import SFP",
                            icon_class="mdi mdi-database-import-outline",
                            button_class=ButtonColorChoices.BLUE
                        ),
                    ]
                ),
            ]),
        ],
    ),
)
