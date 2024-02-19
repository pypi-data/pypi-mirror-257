import xlrd

class XlsParser:
    def __init__(self) -> None:
        self.__letters = "abcdefghijklmnopqrstuvwxyz"
    
    def open_book(self, file_path) -> None:
        if file_path:
            self.workbook = xlrd.open_workbook_xls(f"{file_path}")

    def parse_sheet(self, sheet_name: str, columns_letters: list = None, row_start: int = None) -> dict:
        return {
            sheet_name: self.__parse_rows(
                self.workbook.sheet_by_name(sheet_name),
                columns_letters, row_start
            )
        }

    def __parse_rows(self, sheet, columns_letters, row_start) -> list:
        rows = []
        
        for row_number in range(row_start - 1 if row_start else 0, sheet.nrows):
            rows.append(
                self.__parse_cells(
                    sheet.row(row_number),
                    columns_letters
                )
            )
            
        return rows
    
    def __parse_cells(self, row, columns_letters) -> list:
        row_cells = []
        if columns_letters:
            for column in columns_letters:
                row_cells.append(row[
                    self.__letters.index(column[-1]) + (len(column)-1)*(len(column)+1)
                ].value)
        else:
            for cell in row: row_cells.append(cell.value)
        
        return row_cells
        