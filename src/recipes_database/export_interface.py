from abc import ABC, abstractmethod

import load_interface

class ExportInterface(ABC):

    @abstractmethod
    def __init__(self, path: str, module_load: load_interface.LoadInterface):
        pass

    @abstractmethod
    def export(self):
        pass

