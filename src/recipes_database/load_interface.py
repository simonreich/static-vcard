from abc import ABC, abstractmethod

class LoadInterface(ABC):

    @abstractmethod
    def __init__(self, path: str):
        pass

    @abstractmethod
    def get_recipies(self):
        pass

    @abstractmethod
    def get_recipies_by_name(self, name: str):
        pass

    @abstractmethod
    def get_names(self):
        pass

    @abstractmethod
    def get_recipies_by_category(self, category: str):
        pass

    @abstractmethod
    def get_categories(self):
        pass

    @abstractmethod
    def get_recipies_by_tag(self, tag: str):
        pass

    @abstractmethod
    def get_tags(self):
        pass

    @abstractmethod
    def get_tags_as_dict(self):
        pass
