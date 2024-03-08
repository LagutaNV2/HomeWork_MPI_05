'''2. Доработать параметризованный декоратор logger в коде ниже.
Должен получиться декоратор, который записывает в файл дату и время вызова функции,
имя функции, аргументы, с которыми вызвалась, и возвращаемое значение.
Путь к файлу должен передаваться в аргументах декоратора

3. Применить написанный логгер к приложению из любого предыдущего д/з.'''

import os
from _datetime import datetime
from functools import wraps


def logger(path):
    def __logger(old_function):
        @wraps(old_function)
        def new_function(*args, **kwargs):
            call_time = datetime.now().strftime('%d-%m-%Y время %H:%M:%S')
            old_func_name = old_function.__name__
            
            result = old_function(*args, **kwargs)
            
            file_path = os.path.join(f'{os.getcwd()}\log_files\{path}')
            print(file_path)
            with open(file_path, 'a', encoding='utf-8') as f:
                f.write(f'Время вызова функции - {call_time}, '
                        f'имя функции - {old_func_name}, '
                        f'аргументы функции - {args} {kwargs}, '
                        f'значение функции - {result}\n')
            return result
        
        return new_function
    
    return __logger


def test_2():
    paths = ('log_1.log', 'log_2.log', 'log_3.log')
    
    for path in paths:
        if os.path.exists(path):
            os.remove(path)
        
        @logger(path)
        def hello_world():
            return 'Hello World'
        
        @logger(path)
        def summator(a, b=0):
            return a + b
        
        @logger(path)
        def div(a, b):
            return a / b
        
        assert 'Hello World' == hello_world(), "Функция возвращает 'Hello World'"
        result = summator(2, 2)
        assert isinstance(result, int), 'Должно вернуться целое число'
        assert result == 4, '2 + 2 = 4'
        result = div(6, 2)
        assert result == 3, '6 / 2 = 3'
        summator(4.3, b=2.2)
    
    for path in paths:
        
        assert os.path.exists(f'log_files/{path}'), f'файл {path} должен существовать'
        
        with open(f'log_files/{path}') as log_file:
            log_file_content = log_file.read()
        
        assert 'summator' in log_file_content, 'должно записаться имя функции'
        
        for item in (4.3, 2.2, 6.5):
            assert str(item) in log_file_content, f'{item} должен быть записан в файл'


if __name__ == '__main__':
    test_2()
