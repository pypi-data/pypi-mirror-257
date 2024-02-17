import os
import sys
import heuf
from hews.templates.back_junior_core import back_junior_core
from hews.__constants__ import ROOT_DIR_NAME


class core(back_junior_core):
    def __init__(self):
        super().__init__(__file__, None, ROOT_DIR_NAME, os.path.dirname(os.path.abspath(sys.argv[0])))
        self._jun_projects_core = None

    ####################################################################################################

    @property
    def jun_projects_core(self):
        if self._jun_projects_core is None:
            from .projects.core import core
            self._jun_projects_core = core(self)
        return self._jun_projects_core

    def jun_project_core(self, name):
        return self.jun_projects_core.jun_project_core(name)

    ####################################################################################################
    def initialize(self, path) -> bool:
        main_py_path = heuf.dir.sub_path(path, 'main.py')
        root_path = heuf.dir.sub_path(path, ROOT_DIR_NAME)
        if heuf.file.is_exists(main_py_path) or heuf.file.is_exists(root_path):
            print("file.is_exists")
            return False
        initialize_path = heuf.dir.sub_path(heuf.dir.sir_dir_path(heuf.dir.sir_dir_path(__file__)), 'initialize')
        initialize_main_py_path = heuf.dir.sub_path(initialize_path, 'main.py')
        initialize_root_path = heuf.dir.sub_path(initialize_path, ROOT_DIR_NAME)
        print(main_py_path)
        print(root_path)
        print(initialize_main_py_path)
        print(initialize_root_path)
        if not heuf.file.copy(initialize_main_py_path, main_py_path):
            print("could not copy main")
            return False
        if not heuf.dir.copy(initialize_root_path, root_path):
            return False
        return True


    ####################################################################################################
    def http(self):
        return "Welcome to hews"

    def console(self):
        self._cmd.print_success("Welcome use hews")
        self._console_help()
        loop = True
        while loop:
            cmd = self._cmd.input("").split()
            if len(cmd) < 1 or cmd[0] == "":
                continue
            match cmd[0]:
                case "help":
                    self._console_help()
                case "install":
                    self._console_install(cmd)
                case "projects":
                    self._console_install(cmd)
                case "exit":
                    self._console_exit()
                    return

    def _console_help(self):
        self._cmd.print_info(" - help # list usage commands")
        self._cmd.print_info(" - install <path> # Install hews to the path")
        self._cmd.print_info(" - projects # Go to the projects directory")
        self._cmd.print_info(" - exit # Exit the current hews dialog")

    def _console_install(self, cmd):
        path = cmd[1] if len(cmd) > 1 else self._cmd.input("Path:")
        if not os.path.isdir(path):
            self._cmd.print_danger(f'Path "{path}" is not exists.')
            return
        if not os.path.isdir(path) or not os.access(path, os.W_OK):
            self._cmd.print_danger(f'Path "{path}" is not writable.')
            return
        if len(os.listdir(path)) == 0:
            self._cmd.print_danger(f'Path "{path}" is not empty.')
            return

    def _console_projects(self):
        self.jun_projects_core.console()

    def _console_exit(self):
        self._cmd.print_warning("You have exited the dialog")
        self._cmd.print_warning('Restarting dialog by execute command "hews"')
