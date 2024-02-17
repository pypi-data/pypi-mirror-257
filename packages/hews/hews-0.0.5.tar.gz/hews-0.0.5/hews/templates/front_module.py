import os.path


class front_module:
    def __init__(self, x):
        from hews.system.projects.project.applications.application.modules.module.core import core
        self._x:core = x

    @property
    def x(self): return self._x
