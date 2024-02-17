from hews.templates.back_senior_core import back_senior_core
from ...__constants__ import PROJECTS_DIR_NAME


class core(back_senior_core):
    def __init__(self, senior):
        super().__init__(__file__, senior, PROJECTS_DIR_NAME)
        from ..core import core as system_core_class
        self._sir_system_core: system_core_class = senior
        self._jun_project_cores = {}

    ####################################################################################################

    @property
    def sir_system_core(self):
        return self._sir_system_core

    ####################################################################################################

    def jun_project_core(self, name):
        if name not in self._jun_project_cores:
            from .project.core import core
            self._jun_project_cores[name] = core(self, name)
        return self._jun_project_cores[name]

    ####################################################################################################

    def console(self):
        self._cmd.print_success("You are now in projects directory")
        self._console_help()
        loop = True
        while loop:
            cmd = self._cmd.input("").split()
            if len(cmd) < 1 or cmd[0] == "":
                continue
            match cmd[0]:
                case "help":
                    self._console_help()

    def _console_help(self):
        self._cmd.print_info(" - help # list usage commands")
        self._cmd.print_info(" - project <name> # Go to the projects directory")
        self._cmd.print_info(" - return # Return to the Root directory")
