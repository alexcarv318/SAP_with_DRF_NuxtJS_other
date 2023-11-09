from functools import total_ordering

@total_ordering
class RomanNumeral:
    
    def __init__(self, number):
        self.number = number
        self.roman_exceptions = {'CM': 900, 'CD': 400, 'XC': 90, 'XL': 40, 'IX': 9, 'IV': 4}
        self.roman_dictionary = {'M': 1000, 'D': 500, 'C' : 100, 'L': 50 , 'X': 10, 'V': 5, 'III': 3, 'II': 2, 'I': 1}
    
    def __str__(self):
        return self.number
    
    def __int__(self):
        result = 0
        number_copy = self.number
        for key, value in self.roman_exceptions.items():
            while key in number_copy:
                number_copy = str(number_copy).replace(key, '', 1)
                result += value
        result += sum(self.roman_dictionary.get(char, 0) for char in number_copy)
        return result
 
    def __eq__(self, other):
        if isinstance(other, RomanNumeral):
            return self.__int__() == other.__int__()
        else:
            return NotImplemented
    
    def __ge__(self, other):
        if isinstance(other, RomanNumeral):
            return self.__int__() >= other.__int__()
        else:
            return NotImplemented
           
    def to_roman(self, number):
        self.roman_dictionary.update(self.roman_exceptions)
        result = ''
        for numeral, value in sorted(self.roman_dictionary.items(), key=lambda x: x[1], reverse=True):
            while number >= value:
                result += numeral
                number -= value
        return result
    
    def __add__(self, other):
        if isinstance(other, RomanNumeral):
            return RomanNumeral(self.to_roman(int(self) + int(other)))
        else:
            return NotImplemented
        
    def __sub__(self, other):
        if isinstance(other, RomanNumeral):
            return RomanNumeral(self.to_roman(int(self) - int(other)))
        else:
            return NotImplemented
    
num1 = RomanNumeral('MCMXCIV')
num2 = RomanNumeral('MCMXCI')

number = RomanNumeral('MCMXCIV') + RomanNumeral('MCMXCI')

print(number, int(number))