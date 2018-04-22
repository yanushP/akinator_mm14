from cx_Freeze import setup, Executable

setup(
    name = "akinator",
    version = "0.1",
    description = "akinator",
    executables = [Executable("akinator.py")]
)