from abc import ABC, abstractmethod
import histogrammer.regex_helper as rh

def get_scheme(name: str):
    """
    Returns a scheme.
    """
    if name == 'belle':
        return BelleScheme()
    elif not name or name == 'none':
        return NoneScheme()
    raise Exception(f'Name {name} is unknown!')


class SchemeBase(ABC):
    """
    Base class for grouping columns.
    """
    def __init__(self):
        """
        Contructor method.
        """
        self.parent_group_name = 'Parent'
        self.groups = {self.parent_group_name:[]}
    
    @abstractmethod
    def initialize(self, columns: list) -> None:
        """
        Initializes scheme using the column list.
        """
        pass

    def get_group_names(self) -> list:
        """
        Returns all groups.
        """
        return list(self.groups.keys())
    
    @abstractmethod
    def get_short_column_names(self, group: str = None) -> list:
        """
        Initializes scheme using the column list.
        """
        pass

    @abstractmethod
    def get_full_column_name(self, group_name: str, short_name: str) -> str:
        """
        Returns a full column name.
        """
        pass


class NoneScheme(SchemeBase):
    """
    Class that addes everything to one group.
    """
    def __init__(self):
        """
        Contructor method.
        """
        super().__init__()
    
    def initialize(self, columns: list) -> None:
        """
        Initializes scheme using the column list.
        """  
        self.original_columns = list(columns)
        self.groups[self.parent_group_name] = self.original_columns

    def get_short_column_names(self, group: str = None) -> list:
        """
        Initializes scheme using the column list.
        """
        return self.groups[self.parent_group_name]

    def get_full_column_name(self, group_name: str, short_name: str) -> str:
        """
        Returns a full column name.
        """
        return short_name

class BelleScheme(SchemeBase):
    """
    Class that groups columns according to basf2 naming convention.
    """
    def __init__(self):
        """
        Contructor method.
        """
        super().__init__()
        self.prefixes = []
        self.original_columns = []

    def initialize(self, columns: list) -> None:
        """
        Initializes scheme using the column list.
        """
        self.original_columns = list(columns)
        #print(self.original_columns)
        for column in self.original_columns:
            group = rh.find_belle_group(column)
            #print(group)
            if group:
                self.prefixes += [group]
        #print(self.prefixes)
        self.prefixes.sort(key=len, reverse=True)
        #print(self.prefixes)
        for column in self.original_columns:
            added = False
            for prefix in self.prefixes:
                if column.startswith(prefix):
                    self.add_to_groups(prefix, column)
                    added = True
                    break
            if not added: 
                self.add_to_groups(None, column)

        #print(self.groups)
        # Count the groups:
        self.length = 0
        for group in self.groups:
            self.length += len(self.groups[group])
        print(f'{self.length} vs {len(self.original_columns)}')
        assert self.length == len(self.original_columns)

    def add_to_groups(self, group: str, value: str):
        """
        Adds a column to a group of columns, creates a 
        group if it does not exist.
        """
        if not group:
            if not value in self.groups[self.parent_group_name]:
                self.groups[self.parent_group_name] += [value]
                return
        if not group in self.groups:
            self.groups[group] = [value]
        elif not value in self.groups[group]:
            self.groups[group] += [value]

    def get_short_column_names(self, group_name: str = None) -> list:
        """
        Initializes scheme using the column list.
        """
        if not group_name or group_name == self.parent_group_name:
            return self.groups[self.parent_group_name]
        if not group_name in self.groups:
            raise Exception(f'Invalid column group name {group_name}!')
        columns = self.groups[group_name]
        return [column[len(group_name)+1:] for column in columns]

    def get_full_column_name(self, group_name: str, short_name: str) -> str:
        """
        Returns a full column name.
        """
        if not group_name or group_name == self.parent_group_name:
            return short_name
        if not group_name in self.groups:
            raise Exception(f'Invalid column group name {group_name}!')
        return f'{group_name}_{short_name}'