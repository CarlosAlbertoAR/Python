import os
import pathlib

#dirname = "D:\Test\src\ACBr\Fontes"

def fast_scandir(dirname):
    subfolders = [f.path for f in os.scandir(dirname) if f.is_dir()]
    
    for dirname in list(subfolders):
        subfolders.extend(fast_scandir(dirname))
    return subfolders  

def save_list_to_file():
    dirname = input("Insira o diretóio:")

    dirlines = fast_scandir(dirname)
    dirlines = ";".join(dirlines)

    filename = f'{pathlib.Path(__file__).parent.resolve()}\directorylist.txt'
    file = open(filename, 'w')
    file.writelines(dirlines)
    file.close

save_list_to_file()


