
import os


def check(cmd, mf):

    print(f'**************************************')
    print(f'In Albow check:  {cmd=} {mf=}')
    print(f'**************************************')
    m = mf.findNode("albow")
    print(f'{m=}')
    if m is None or m.filename is None:
        return None

    def addPath(f):
        return os.path.join(os.path.dirname(m.filename), f)

    RESOURCES = ["themes/resources/default-theme.ini", "themes/resources/Vera.ttf", "themes/resources/VeraBd.ttf"]

    returnedDictionary = {"loader_files": [("albow/themes/resources", map(addPath, RESOURCES))]}
    print(f'returning: {returnedDictionary=}')
    return returnedDictionary
