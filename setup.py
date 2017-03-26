import cx_Freeze

executables = [cx_Freeze.Executable("race.py")]

cx_Freeze.setup(
    name = "A simple racing",
    options = {"build_exe":{"packages":["pygame"],
                            "include_files":["racecar.png"]}},
    executables = executables
)