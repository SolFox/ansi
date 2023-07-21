""" Toolage for use with AnsiColors used for various 
datatypes and meant to add that missing visual spice 
to terminal/command prompt.

Author: AERivas
Data: 07/11/2023
"""
from dataclasses import dataclass
from ansi import Ansi
from typing import Dict, Generic, Set, Tuple, TypeVar, List

T = TypeVar('T')

@dataclass
class DataContainer(Generic[T]):
    collection_type: List[T] | Dict[T, T] | Set[T] | Tuple[T, ...]
    
    def __iter__(self):
        return iter(self.collection_type)
    
@dataclass
class AnsiTools(Ansi):
    
    def list_available_colors(self) -> list[str]:
        """Return all attribute names found inside AnsiColors
        as strings in a list.
        
        Usage Example:
            >>> give_color = AnsiTools()
            >>> list_colors = give_colors.list_available_colors()
            >>> print(*list_colors)
            
        Author: AERivas
        Date: 07/11/2023
        """
        return list(vars(self).keys())
    
    def display_all_colors(self) -> None:
        """Output all colors onto screen found inside AnsiColors
        
        Usage Example:
            >>> give_color = AnsiColors()
            >>> display_colors = give_color.display_all_colors()
            >>> print(display_colors)
        
        Author: AERivas
        Date: 07/11/2023
        """
        for key in self.list_available_colors():
            print(self.__dict__[key] + key + self.END_COLOR)
    
    def to_this_string(self, astring: str, color: str) -> str:
        """Returns a given string with added color
        
        Parameter color: lowercased color of choice example: bright_green.
        Parameter astring: a string data type used to add color to
        Usage Example: 
            >>> give_color = AnsiTools()
            >>> colored_message = give_color.to_this_string("this entire string !", "bright_green")
            >>> print(colored_message)

        Author: AERivas
        Date: 07/11/2023
        """
        return " ".join([self.__dict__[key] + astring + self.END_COLOR for key in self.__dict__.keys() if color == key.lower()])
        
    def to_this_collection(self, data: DataContainer[T],  color: str, color_2: str="bright_green") -> DataContainer[T]:
        data:  List[T] | Dict[T, T] | Set[T] | Tuple[T, ...]
        if isinstance(data.collection_type, list):
            for i, item in enumerate(data.collection_type):
                data.collection_type[i] = self.to_this_string(item, color)
        elif isinstance(data.collection_type, dict):
            update_dict = {}
            for key, value in data.collection_type.items():
                colored_key = self.to_this_string(key, color)
                colored_value = self.to_this_string(value, color_2)
                update_dict[colored_key] = colored_value
            data.collection_type = update_dict
        elif isinstance(data.collection_type, set):
            copy_set = data.collection_type.copy()
            for item in copy_set:
                data.collection_type.remove(item)
                item = self.to_this_string(item, color)
                data.collection_type.add(item)
        elif isinstance(data.collection_type, tuple):
            colored_items = []
            for item in data.collection_type:
                color_item = self.to_this_string(item, color)
                colored_items.append(color_item)
            data.collection_type = tuple(colored_items)
        return data
   
    def set_custom_foreground(self, astring: str, R: int, G: int, B: int) -> str:
        """Returns a given string with customized foreground RGB color
        
        Parameter astring: the string used to changed its foreground color
        Parameter R: RED, a number ranging from 0-255
        Parameter G: GREEN, a number ranging from 0-255
        Parameter B: BLUE, a number ranging from 0-255
        Usage Example:
            >>> give_color = AnsiTools()
            >>> foreground = give_color.set_custom_foreground("change the foreground color of a string", R=212, G=245, B=7)
            >>> print(foreground)
        
        Author: AERivas
        Date: 07/11/2023
        """
        assert 0 <= R <= 255, f"R must be in the range of 0-255 not ~-> {R}."
        assert 0 <= G <= 255, f"G must be in the range of 0-255 not ~-> {G}."
        assert 0 <= B <= 255, f"B must be in the range of 0-255 not ~-> {B}."
        return f"\033[38;2;{R};{G};{B}m" + astring + self.END_COLOR

    def set_custom_background(self, astring: str, R: int, G: int, B: int) -> str:
        """Returns a given string with the provided customized background RGB color
        
        Parameter R: RED, a number ranging from 0-255 
        Parameter G: GREEN, a number ranging from 0-255 
        Parameter B: BLUE, a number ranging from 0-255
        Usage Example:
            >>> give_color = AnsiTools()
            >>> background = give_color.set_custom_background("change the background color to this string", R=212, G=245, B=7)
            >>> print(background)
            
        Author: AERivas
        Date: 07/11/2023
        """
        assert 0 <= R <= 255, f"R must be in the range of 0-255 not ~-> {R}."
        assert 0 <= G <= 255, f"G must be in the range of 0-255 not ~-> {G}."
        assert 0 <= B <= 255, f"B must be in the range of 0-255 not ~-> {B}."
        return f"\033[48;2;{R};{G};{B}m" + astring + self.END_COLOR