import sys
import os

import maya.api.OpenMaya as om
CIODIR = os.environ.get("CWMAYA_CIODIR")
sys.path.append(CIODIR)

from cwmaya.nodes.cw_submission import cwSubmission
from cwmaya.nodes.cw_ass_submission import cwAssSubmission
from cwmaya.lib import coreweave_menu

def maya_useNewAPI():
    pass

def initializePlugin(obj):
 
    plugin = om.MFnPlugin(obj, "CoreWeave", "0.0.1-beta.3", "Any")
 
    try:
        plugin.registerNode(
            "cwSubmission",
            cwSubmission.id,
            cwSubmission.creator,
            cwSubmission.initialize,
            om.MPxNode.kDependNode,
        )
        plugin.registerNode(
            "cwAssSubmission",
            cwAssSubmission.id,
            cwAssSubmission.creator,
            cwAssSubmission.initialize,
            om.MPxNode.kDependNode,
        )
                
    except:
        sys.stderr.write("Failed to register cwSubmission\n")
        raise


    coreweave_menu.load()

    # coredata.init("maya-io")


def uninitializePlugin(obj):
    plugin = om.MFnPlugin(obj)

    try:
        plugin.deregisterNode(cwAssSubmission.id)
        plugin.deregisterNode(cwSubmission.id)
    except:
        sys.stderr.write("Failed to deregister cwSubmission\n")
        raise

    coreweave_menu.unload()
