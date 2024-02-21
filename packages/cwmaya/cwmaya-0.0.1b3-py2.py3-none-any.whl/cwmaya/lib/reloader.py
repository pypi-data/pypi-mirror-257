# -*- coding: utf-8 -*-

from cwmaya.lib import (
    const,
    tools_menu,
    persist_ui,
    window_utils,
    node_utils,
    layer_utils,
    about_window,
    window,
)

from cwmaya.lib.ui import base_tab, job_tab, export_tab, render_tab, slack_tab, comp_tab

from cwmaya.lib.ui.widgets import (
    integer_field,
    kv_pairs,
    commands,
    text_area,
    hidable_text_field,
    dual_option_menu,
    single_option_menu,
    single_option_menu_array,
    text_field,
    asset_list,
)


import importlib

importlib.reload(const)

importlib.reload(hidable_text_field)
importlib.reload(text_field)
importlib.reload(integer_field)
importlib.reload(text_area)
importlib.reload(kv_pairs)
importlib.reload(commands)
importlib.reload(dual_option_menu)
importlib.reload(single_option_menu)
importlib.reload(single_option_menu_array)
importlib.reload(asset_list)

# Tabs
importlib.reload(base_tab)
importlib.reload(job_tab)
importlib.reload(export_tab)
importlib.reload(render_tab)
importlib.reload(comp_tab)
importlib.reload(slack_tab)

importlib.reload(tools_menu)
importlib.reload(node_utils)
importlib.reload(layer_utils)
importlib.reload(window_utils)
importlib.reload(persist_ui)
importlib.reload(about_window)
importlib.reload(window)
