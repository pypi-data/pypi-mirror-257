# -*- coding: utf-8 -*-
import pymel.core.uitypes as gui
import pymel.core as pm

from cwmaya.lib import reloader
from cwmaya.lib import const as k
import importlib

from cwmaya.lib.ui import (
    export_tab,
    render_tab,
    job_tab,
)
from cwmaya.lib import tools_menu

importlib.reload(reloader)

SUBMISSION_NODE = "cwAssSubmission"

# from uprising import pov


class StormWindow(gui.Window):
    def __init__(self):

        others = pm.lsUI(windows=True)
        for win in others:
            if pm.window(win, q=True, title=True) == k.WINDOW_TITLE:
                pm.deleteUI(win)

        self.node = None
        self.setTitle(k.WINDOW_TITLE)
        self.setIconName(k.WINDOW_TITLE)
        self.setWidthHeight(k.WINDOW_DIMENSIONS)

        self.menuBarLayout = pm.menuBarLayout()
        self.tabLayout = pm.tabLayout(changeCommand=pm.Callback(self.on_tab_changed))

        # TABLayout
        pm.setParent(self.tabLayout)
        self.tabs = {}
        self.tabs["job_tab"] = job_tab.JobTab()
        pm.setParent(self.tabLayout)
        self.tabs["export_tab"] = export_tab.ExportTab()
        pm.setParent(self.tabLayout)
        self.tabs["render_tab"] = render_tab.RenderTab()
        pm.setParent(self.tabLayout)

        self.tabLayout.setTabLabel((self.tabs["job_tab"], "Job"))
        self.tabLayout.setTabLabel((self.tabs["export_tab"], "Export Tasks"))
        self.tabLayout.setTabLabel((self.tabs["render_tab"], "Render Tasks"))

        # MENUS
        pm.setParent(self.menuBarLayout)
        self.tools_menu = tools_menu.create()

        self.show()
        self.setResizeToFitChildren()

        self.bind_node()

    def on_tab_changed(self):
        print("on_tab_changed")

    def bind_node(self):
        """
        Find or create a node and bind the UI to it.
        """
        nodes = pm.ls(type=SUBMISSION_NODE)
        if not nodes:
            nodes = [pm.createNode(SUBMISSION_NODE)]
        self.node = nodes[0]
        pm.select(self.node)

        for tab in self.tabs.values():
            tab.bind(self.node)
        self.tabLayout.setSelectTabIndex(3)
