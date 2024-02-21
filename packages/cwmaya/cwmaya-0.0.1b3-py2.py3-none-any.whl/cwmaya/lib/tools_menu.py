import pymel.core as pm

def create():
    menu = pm.menu(label="Tools", tearOff=True)
    pm.menuItem(label="Find something", command=pm.Callback(on_find_something))
    return menu

def on_find_something():
    print("Run Find Something")
