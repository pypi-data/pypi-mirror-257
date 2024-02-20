import os
import re
import sys
import shutil


def sort(path):
        
    def normalize(name: str) -> str:
        name, *extension = name.split('.')
        new_name = name.translate(TRANS)
        new_name = re.sub(r'\W', '_', new_name)
        return f"{new_name}.{'.'.join(extension)}"

    def getExtension(name: str) -> str:
        name, extension = name.split('.')
        return extension

    def makeDir(name):
        if not os.path.exists(name):
            os.mkdir(name)

    def walkSortDir(path, level=1, list_of_use_extensions=[], list_other_extensions=[]):
        for i in os.listdir(path):
            if os.path.isdir(path + separator + i):
                walkSortDir(path + separator + i, level + 1,
                            list_of_use_extensions, list_other_extensions)
            if not os.path.isdir(path + separator + i):
                extension = getExtension(i)
                unsorted = True
                for type in LIST_OF_TYPES:
                    if extension in type:
                        makeDir(os.path.abspath(PATH) + separator + type[0])
                        os.replace(os.path.abspath(path + separator + i),
                                os.path.abspath(PATH + separator + type[0] + separator + (normalize(i))))
                        unsorted = False
                        list_of_use_extensions.append(extension)
                if unsorted:
                    makeDir(os.path.abspath(PATH) + separator + OTHERS)
                    os.replace(os.path.abspath(
                        path + separator + i), os.path.abspath(PATH + separator + OTHERS + separator + (normalize(i))))
                    list_other_extensions.append(extension)
        return (set(list_of_use_extensions), set(list_other_extensions))

    def removeSortedDir(name):
        for i in os.listdir(name):
            if os.path.isdir(name + separator + i) and i not in LIST_OF_DIRS:
                shutil.rmtree(name + separator + i)

    def unpackSortedArchives(arc_path):
        if os.path.exists(arc_path + separator + ARCHIVES[0]):
            for i in os.listdir(arc_path + separator + ARCHIVES[0]):
                if not os.path.isdir(arc_path + separator + ARCHIVES[0] + separator + i):
                    try:
                        shutil.unpack_archive(
                            arc_path + separator + ARCHIVES[0] + separator + i, arc_path + separator + ARCHIVES[0] + separator + i.replace("." + getExtension(i), ""))
                        os.remove(arc_path + separator +
                                ARCHIVES[0] + separator + i)
                    except shutil.ReadError:
                        os.remove(arc_path + separator +
                                ARCHIVES[0] + separator + i)


    PATH = path

    IMAGES = ("images", "jpeg", "png", "jpg", "svg")
    VIDEO = ("video", "avi", "mp4", "mov", "mkv")
    DOCUMENTS = ("documents", "doc", "docx", "txt", "pdf", "xlsx", "pptx")
    AUDIO = ("audio", "mp3", "ogg", "wav", "amr")
    ARCHIVES = ("archives", "zip", "gz", "tar")
    OTHERS = ("others")

    LIST_OF_TYPES = (IMAGES, VIDEO, DOCUMENTS, AUDIO, ARCHIVES)

    LIST_OF_DIRS = (IMAGES[0], VIDEO[0], DOCUMENTS[0],
                    AUDIO[0], ARCHIVES[0], OTHERS)

    TRANS = {}
    UKRAINIAN_SYMBOLS = 'абвгдеєжзиіїйклмнопрстуфхцчшщьюя'
    TRANSLATION = ("a", "b", "v", "g", "d", "e", "je", "zh", "z", "y", "i", "ji", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
                "f", "h", "ts", "ch", "sh", "sch", "", "ju", "ja")

    for key, value in zip(UKRAINIAN_SYMBOLS, TRANSLATION):
        TRANS[ord(key)] = value
        TRANS[ord(key.upper())] = value.upper()

    if sys.platform in ("linux", "darwin"):
        separator = "/"
    elif sys.platform in ("win32", "cygwin"):
        separator = '\\'

    list_of_use_extensions, list_other_extensions = walkSortDir(PATH)

    removeSortedDir(PATH)

    unpackSortedArchives(PATH)

    for sort_dir in os.listdir(PATH):
        if os.path.isdir(PATH + separator + sort_dir):
            if sort_dir != ARCHIVES[0]:
                print(
                    f"\nThese files have been moved to {PATH + separator + sort_dir}")
            else:
                print(
                    f"\nThese archives have been moved and unpacked to {PATH + separator + sort_dir}")
            for file_name in os.listdir(PATH + separator + sort_dir):
                print(file_name)
    if len(list_of_use_extensions) > 0:
        print(
            f"\nIidentified file types")
        for type in list_of_use_extensions:
            print(type)

    if len(list_other_extensions) > 0:
        print(
            f"\nUnidentified file types")
        for type in list_other_extensions:
            print(type)
