from constants import *

def loadFile(filename):
    with open(filename) as f:
        file = f.readlines()
        f.close()
        return file
        
def loadValueFromFile(file, key):
    keylen = len(key)
    for line in file:
        line = line.strip()
        if line[0] != "[" or line[-1] != "]":
            continue
        line = line[1:-1]
        if line[0:keylen] != key:
            continue
        return int(line[keylen+1:])
    return None

def loadValueFromTXT(filename, key):
    file = loadFile(filename)
    loadValueFromFile(file, key)

def convertColorStringToInt(string):
    if string == "BLACK":
        return BLACK
    elif string == "BLUE":
        return BLUE
    elif string == "GREEN":
        return GREEN
    elif string == "CYAN":
        return CYAN
    elif string == "RED":
        return RED
    elif string == "MAGENTA":
        return MAGENTA
    elif string == "BROWN":
        return BROWN
    elif string == "LGRAY":
        return LGRAY
    elif string == "DGRAY":
        return DGRAY
    elif string == "LBLUE":
        return LBLUE
    elif string == "LGREEN":
        return LGREEN
    elif string == "LCYAN":
        return LCYAN
    elif string == "LRED":
        return LRED
    elif string == "LMAGENTA":
        return LMAGENTA
    elif string == "YELLOW":
        return YELLOW
    elif string == "WHITE":
        return WHITE
    else: return -1

def loadRenderCodeFromJSONStructure(tileJSON):
    print(tileJSON)
    render = []
    render_code_flag_id = 0
    if "render" not in tileJSON.keys():
        return [0,]
    if "render_flags" not in tileJSON.keys():
        render.append(NO_FLAGS)
    else:
        render_flags = tileJSON["render_flags"].split("|")
        if "ENVIRONMENTAL" in render_flags:
            render_code_flag_id += (1<<ENVIRONMENTAL)
        if "DIRECTIONAL" in render_flags:
            render_code_flag_id += (1<<DIRECTIONAL)
        if "TRANSPARENT" in render_flags:
            render_code_flag_id += (1<<TRANSPARENT)
        if "HALFSCALED" in render_flags:
            render_code_flag_id += (1<<HALFSCALED)
        if "IODIRECTIONAL" in render_flags:
            render_code_flag_id += (1<<IODIRECTIONAL)
        if "ROTATIONAL" in render_flags:
            render_code_flag_id += (1<<ROTATIONAL)
        render.append(render_code_flag_id)
    if isRenderFlagInCode(IODIRECTIONAL, render[0]):
        render.append(getRenderSequence(render[0], tileJSON["render"]["NS"]))
        render.append(getRenderSequence(render[0], tileJSON["render"]["NE"]))
        render.append(getRenderSequence(render[0], tileJSON["render"]["NW"]))
        render.append(getRenderSequence(render[0], tileJSON["render"]["SN"]))
        render.append(getRenderSequence(render[0], tileJSON["render"]["SE"]))
        render.append(getRenderSequence(render[0], tileJSON["render"]["SW"]))
        render.append(getRenderSequence(render[0], tileJSON["render"]["EN"]))
        render.append(getRenderSequence(render[0], tileJSON["render"]["ES"]))
        render.append(getRenderSequence(render[0], tileJSON["render"]["EW"]))
        render.append(getRenderSequence(render[0], tileJSON["render"]["WN"]))
        render.append(getRenderSequence(render[0], tileJSON["render"]["WS"]))
        render.append(getRenderSequence(render[0], tileJSON["render"]["WE"]))
        print(render)
        return render
    if isRenderFlagInCode(DIRECTIONAL, render[0]):
        return render
    render.append(getRenderSequence(NO_FLAGS, tileJSON["render"]))
    print(render)
    return render

def getRenderSequence(flags, sequence):
    n = 2
    if isRenderFlagInCode(HALFSCALED, flags): n += 3
    if isRenderFlagInCode(ROTATIONAL, flags): n += 1
    newrenderlist = []
    for i in range(int(len(sequence)/n)):
        oneSequence = []
        oneSequence.append(sequence[i*n]),
        oneSequence.append(convertColorStringToInt(sequence[1+i*n])),
        if n == 2: 
            newrenderlist.append(oneSequence)
            continue
        for j in range(2, n):
            oneSequence.append(sequence[i*n+j])
        newrenderlist.append(oneSequence)    
    return newrenderlist

def isRenderFlagInCode(flag, code):
    if (code >> flag) % 2 == 1:
        return True
    return False

def loadNames(data, key):
    names = []
    for i in data:
        names.append(i[key])
    return names
    
if __name__ == "__main__":
    import main