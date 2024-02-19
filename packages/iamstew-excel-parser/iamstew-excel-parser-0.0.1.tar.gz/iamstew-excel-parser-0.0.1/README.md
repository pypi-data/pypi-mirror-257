# Библиотека `iamstew-excel-parser`

### Что она делает?
Библиотека открывает xls/xlsx файл по ссылке, и возвращает двумерный массива со значениями ячеек.

### Быстрый гайд
```python
from iamstew_excel_parser import XlsxParser # если вам нужно парсить xlsx файл
from iamstew_excel_parser import XlsParser # если вам нужно парсить xls файл

...

path = "/your/absolute/path/to/excel/file"
excel_parser.open_book(file_path=path)
result = excel_parser.parse_sheet(
    sheet_name=sheet_name, # передаем название листа книги, если не указан, будет парсить 1 лист книги
    row_start=row_start, # передаем номер строки с которой начинать парсинг, если не указан, то начнется с 1 строки
    columns_letters=columns_letters # передаем массив со строковыми буквами колонок, например ["a","b","ac"]
)
```

```python
print(result)
# пример выходных данных
{ "Название листа": [
    ["Имя", "Фамилия", "Отчество"],
    ["Иван", "Иванов", "Иванович"],
    ["Петр", "Петров", "Петрович"],
    ["Алексей", "Алексеев", "Алексеевич"]
  ]
}

# если ячейка пустая - возвращает None
[
    ["Иван", "Иванов", None]
]
```