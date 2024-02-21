

import os , colorama , subprocess , colorama , collections , importlib
from io import StringIO  


def remotePip(name , pkg = None  ,cmd = "pip install" , env = dict() ) : 
    _pkg = name if pkg is None else pkg 
    try:
        imported_module = importlib.import_module(name)
        return imported_module
    except ImportError:
        printerror(f"remotePip : {_pkg} is not installed -->> installing it using {cmd}")
        assert bash(f"{cmd} {_pkg}", env = env ).ok ,""
        return importlib.import_module(name)




def bash(cmd , cwd  = "." , shell = True , text = True , throw = False , env = dict()) : 
    colorama.init()
    print(colorama.Back.GREEN + colorama.Style.BRIGHT + f" $ {cmd.strip()}" + " "*10  +  colorama.Style.RESET_ALL , end = "", flush = True)
    process = None 
    if len(env.keys()) > 0  : 
        process = subprocess.Popen(cmd, shell=shell, stdout=subprocess.PIPE, stderr=subprocess.PIPE , text = text , env = env, cwd = cwd)
    else : 
        process = subprocess.Popen(cmd, shell=shell, stdout=subprocess.PIPE, stderr=subprocess.PIPE , text = text , cwd = cwd)
    stdout, stderr = process.communicate()
    return_code = process.returncode
    if return_code == 0:
        print("\n" + stdout)
        print(colorama.Style.RESET_ALL + colorama.Style.BRIGHT + colorama.Fore.GREEN + "\n\t==> Job succeeded" +  colorama.Style.RESET_ALL )
        
    else : 
        print(colorama.Style.BRIGHT + colorama.Fore.RED + f" ==> code {return_code}" +  colorama.Style.RESET_ALL  + colorama.Fore.RED + "\n" + f"{stderr.strip()})" +  colorama.Style.RESET_ALL)
        print(colorama.Style.RESET_ALL  + colorama.Style.BRIGHT + colorama.Fore.RED + "\n\t==> Job Failed" +  colorama.Style.RESET_ALL )
    return collections.namedtuple('ibash', ['code', 'stdout', 'stderr' , "ok"])(code = return_code ,stdout = stdout , stderr = stderr  , ok  = return_code == 0)



def clear() : 
    c = bash("clear")
    assert c.ok , c.stderr

def printok(*args , **kwargs) : 
    string_io = StringIO()  
    print(*args , **kwargs , file = string_io)
    print(colorama.Style.RESET_ALL + colorama.Style.BRIGHT + colorama.Fore.GREEN + f">> <OK>\t:{string_io.getvalue()}" +  colorama.Style.RESET_ALL   )
    string_io.close()

def printerror(*args , **kwargs) : 
    string_io = StringIO()  
    print(*args , **kwargs , file = string_io)
    print(colorama.Style.RESET_ALL + colorama.Style.BRIGHT + colorama.Fore.RED + f">> <ERROR>\t:{string_io.getvalue()}" +  colorama.Style.RESET_ALL   )
    string_io.close()


def remotePip(name , pkg = None  ,cmd = "pip install") : 
    _pkg = name if pkg is None else pkg 
    try:
        imported_module = importlib.import_module(name)
        return imported_module
    except ImportError:
        printerror(f"remotePip : {_pkg} is not installed -->> installing it using {cmd}")
        assert bash(f"{cmd} {_pkg}").ok ,""
        return importlib.import_module(name)



