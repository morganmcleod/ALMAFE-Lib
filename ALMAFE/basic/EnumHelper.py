from enum import Enum

class EnumHelper(Enum):
    '''
    Add matching and conversion helpers to Enum.
    '''
    @classmethod
    def exists(cls, value):
        '''
        True if the value str is a value in the Enum.
        :param cls:    derived from EnumHelper
        :param value:  str
        '''
        return value in cls.__members__
    
    @classmethod
    def from_str(cls, value):
        '''
        Convert from str value to Enum value.  Doesn't catch exceptions.        
        :param cls:    derived from EnumHelper
        :param value:  str
        '''
        return cls(value)