import sys
from cx_Freeze import setup, Executable

build_exe_options = {
    "packages": ["os", "PyQt5", "pandas", "jinja2", "docxtpl", "requests"],
    "include_files": ["data", "templates"],
    "excludes": []
}

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="AutoStudentDocs",
    version="1.0",
    description="AutoStudentDocs Application",
    options={"build_exe": build_exe_options},
    executables=[Executable("main.py", base=base)]
)

# import sys
# from cx_Freeze import setup, Executable

# # Опции для сборки exe
# build_exe_options = {
#     "packages": ["os", "PyQt5", "pandas", "jinja2", "docxtpl", "requests"],
#     "include_files": ["data/", "templates/"],
#     "excludes": ["tkinter"],
#     "include_msvcr": True,
# }

# base = None
# if sys.platform == "win32":
#     base = "Win32GUI"

# setup(
#     name="AutoStudentDocs",
#     version="1.0",
#     description="AutoStudentDocs Application",
#     options={"build_exe": build_exe_options},
#     executables=[Executable("main.py", base=base)]
# )