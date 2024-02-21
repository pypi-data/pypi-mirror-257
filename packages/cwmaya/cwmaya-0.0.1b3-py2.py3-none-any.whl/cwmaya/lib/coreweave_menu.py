
from __future__ import unicode_literals
import pymel.core as pm
from cwmaya.lib import window

import webbrowser
import importlib


from cwmaya.lib import about_window
from cwmaya.lib import const as k

MAYA_PARENT_WINDOW = "MayaWindow"
COREWEAVE_MENU = "CoreWeaveMenu"
CONDUCTOR_DOCS = "https://docs.conductortech.com/"
COREWEAVE_SUBMISSION_NODE = "cwSubmission"
COREWEAVE_AEX_SUBMISSION_NODE = "cwAssSubmission"

def unload():

    if pm.menu(COREWEAVE_MENU, q=True, exists=True):
        pm.menu(COREWEAVE_MENU, e=True, deleteAllItems=True)
        pm.deleteUI(COREWEAVE_MENU)


def load():
    unload()
    CoreWeaveMenu()

class CoreWeaveMenu(object):
    def __init__(self):
        if not pm.about(batch=True):
            pm.setParent(MAYA_PARENT_WINDOW)

            self.menu = pm.menu(
                COREWEAVE_MENU,
                label="CoreWeave",
                tearOff=True,
                # pmc=pm.Callback(self.post_menu_command),
            )
            
            pm.menuItem(label="Storm Window", command=pm.Callback(show_storm_window))
            
            
            # self.submitter_menu = pm.menuItem(label="Submitter", subMenu=True)

            # pm.setParent(self.menu, menu=True)

            pm.menuItem(divider=True)
            
            pm.setParent(self.menu, menu=True)

            pm.menuItem(divider=True)

            self.help_menu = pm.menuItem(
                label="Help", command=pm.Callback(webbrowser.open, CONDUCTOR_DOCS, new=2)
            )
            self.about_menu = pm.menuItem(label="About", command=pm.Callback(about_window.show))
 
    # def post_menu_command(self):
    #     """
    #     Build the Select/Create submenu just before the menu is opened.
    #     """
    #     pm.setParent(self.submitter_menu, menu=True)
    #     pm.menu(self.submitter_menu, edit=True, deleteAllItems=True)
    #     for j in pm.ls(type=COREWEAVE_SUBMISSION_NODE):
    #         pm.menuItem(label="Select {}".format(str(j)), command=pm.Callback(select_and_show, j))
            
    #     pm.menuItem(divider=True)

    #     pm.menuItem(label="Create", command=pm.Callback(create_submission_node))
    #     pm.setParent(self.menu, menu=True)

def show_storm_window():
    importlib.reload(window)
    window.StormWindow()

# def create_submission_node():
#     node = pm.createNode(COREWEAVE_AEX_SUBMISSION_NODE)
#     select_and_show(node)


def select_and_show(node):
    pm.select(node)

    if not pm.mel.isAttributeEditorRaised():
        pm.mel.openAEWindow()

