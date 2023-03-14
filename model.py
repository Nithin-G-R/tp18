import view
from flask import render_template

webpage_view = view.View()


def HomePage():
    return webpage_view("HomePage")


def InfoPage(section=None, title=None, content=None):
    base_menus = [
        ["News", 0, "/InfoHome/0"],
        ["Reuse Methods", 0, "/InfoHome/1"],
        ["analysis", 0, "/InfoHome/2"],
    ]

    menus = base_menus.copy()
    if section:
        menus[section][1] = "active"
    else:
        menus[0][1] = "active"

    return webpage_view("InfoHome", section=section, title=title, content=content, menus=menus)



def sortingPage():
    return webpage_view("SortingPage")

def AboutPage():
    return webpage_view('about')

def MapPage():
    return webpage_view('Map')

def resultPage(cls=None):
    return webpage_view("result", cls=cls)
