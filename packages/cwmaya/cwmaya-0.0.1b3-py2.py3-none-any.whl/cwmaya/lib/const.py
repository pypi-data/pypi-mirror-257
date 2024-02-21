import re
import os

LABEL_WIDTH = 145
TRASH_COLUMN_WIDTH = 36
FORM_SPACING_X = 4
FORM_SPACING_Y = 2
WINDOW_DIMENSIONS = [600, 800]
WINDOW_TITLE = "Storm Tools"


CURRENT_LAYER = 0
LAYERS_ONE_JOB = 1
JOB_PER_LAYER = 2


DEFAULT_TEMPLATE = 'Render -r <Renderer> -s <start> -e <end> -b <step> -rl "<RenderLayer>" -rd "<OutputPath>"  -proj "<WorkspacePath>" "<SceneFile>"'
DEFAULT_DESTINATION_DIR_TEMPLATE = "<ImagesPath>"
OTHER_TEMPLATES = [
    'Render -r <Renderer>  -ai:lve 3 -s <start> -e <end> -b <step> -rl "<RenderLayer>" -rd "<OutputPath>"  -proj "<WorkspacePath>" "<SceneFile>"'
]


DEFAULT_TITLE = "Maya:<Renderer> - <Scene> <RenderLayer>"
DEFAULT_AUTOSAVE_TEMPLATE = "cio_<Scene>"

DEFAULT_INSTANCE_TYPE = "n1-standard-4"
MAX_TASKS = int(os.environ.get("CONDUCTOR_MAX_TASKS", 1000))
LIST_HEADER_BG = (0.35, 0.35, 0.35)

INSTANCE_TYPES = {
    "cpu": {
        "display": "CPU",
        "content": {
            "c5.large": {
                "display": "C5 Large",
            },
            "c5.xlarge": {
                "display": "C5 Extra Large",
            },
            "c5.2xlarge": {
                "display": "C5 Double Extra Large",
            },
            "c5.4xlarge": {
                "display": "C5 Quadruple Extra Large",
            },
            "c5.9xlarge": {
                "display": "C5 Ninetuple Extra Large",
            },
            "c5.18xlarge": {
                "display": "C5 Eighteenfold Extra Large",
            },
        },
    },
    "gpu": {
        "display": "GPU",
        "content": {
            "g4dn.xlarge": {
                "display": "G4DN Extra Large",
            },
            "g4dn.2xlarge": {
                "display": "G4DN Double Extra Large",
            },
            "g4dn.4xlarge": {
                "display": "G4DN Quadruple Extra Large",
            },
            "g4dn.8xlarge": {
                "display": "G4DN Eightfold Extra Large",
            },
            "g4dn.16xlarge": {
                "display": "G4DN Sixteenfold Extra Large",
            },
        },
    },
}

SOFTWARE = {
    "maya-2019": {"display": "Maya 2019"},
    "maya-2020": {"display": "Maya 2020"},
    "maya-2021": {"display": "Maya 2021"},
    "kick-6.4.4.2": {"display": "Kick 6.4.4.2"},
    "kick-6.5.0.0": {"display": "Kick 6.5.0.0"},
    "kick-7.1.0.1": {"display": "Kick 7.1.0.1"},
}


PROJECTS = {
    "corelli": {"display": "Captain Corelli's Mandolin"},
    "troy": {"display": "Troy"},
    "borrowers": {"display": "The Borrowers"},
    "montecristo": {"display": "The Count of Monte Cristo"},
    "hours": {"display": "The Hours"},
    "potter2": {"display": "Harry Potter and the Chamber of Secrets"},
    "fishtank": {"display": "Fish Tank"},
    "pitchblack": {"display": "Pitch Black"},
}
