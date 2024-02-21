import os

import pymel.core as pm
import pymel.core.uitypes as gui
from cwmaya.lib import persist_ui

CMD_TEMPLATE = 'nuke -x myscript.nk <sequence>'

class CompTab(gui.FormLayout):
    def __init__(self):
        """
        Create the UI.
        """
        self.setNumberOfDivisions(100)
        pm.setParent(self)
        self.column = pm.columnLayout()
        self.column.adjustableColumn(True)

        self.export_frame = self.create_export_frame()

   
        # pm.setParent(self)
        # self.create_action_buttons()
        pm.setParent(self)

        prefix = "storm_comp"
        self.persistentWidgets = [
            persist_ui.factory(self, "chunk_if", prefix, default_value=1),
            persist_ui.factory(
                self, "cmd_tf", prefix, default_value=CMD_TEMPLATE
            ),
        ]

        self.populate()
        self.on_ops_change()

    def create_export_frame(self):
        """
        Create the frame that contains the export options.
        """
        frame = pm.frameLayout(label="Export", bv=True)

        self.chunk_if = pm.intFieldGrp(
            height=30,
            label="Chunk Size",
            annotation="Max number of frames to export",
            numberOfFields=1,
        )

        self.cmd_tf = pm.textFieldGrp(label="Command", adjustableColumn=2)

        pm.setParent("..")
        return frame


    def on_ops_change(self):
        """
        Manage the UI state based on the current options.
        """
        pass

    def on_go(self):
        self.save()

        chunk_size = pm.intFieldGrp(self.chunk_if, query=True, value1=True)
        cmd = pm.textFieldGrp(self.cmd_tf, query=True, text=True)
        print("chunk_size", chunk_size)
        print("cmd", cmd)

    def populate(self):
        for persister in self.persistentWidgets:
            persister.populate()

    def save(self):
        for persister in self.persistentWidgets:
            persister.save()

    def reset(self):
        for persister in self.persistentWidgets:
            persister.reset()
