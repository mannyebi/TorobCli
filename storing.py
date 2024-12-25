import openpyxl


path = "./results.xlsx"


wb_obj = openpyxl.load_workbook(path)

sheet_obj = wb_obj.active

data = [
        ["نام محصول", "قیمت", "لینک"],
       ]

## appending row by row to the sheet
#for row in data:
    ## append method is used to append the data to a cell
    #sheet_obj.append(row)


def add_record(product_name, product_price, product_link):
    new_record = [product_name, product_price, product_link]
    sheet_obj.append(new_record)
    wb_obj.save(path)


