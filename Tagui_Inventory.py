import rpa as r
import PyPDF2 
import re
import glob

def data_extract(pdfpath):
    r.keyboard('[win]r')
    r.clipboard(pdfpath)
    r.keyboard('[clear][ctrl]v [enter]')
    r.wait(5)

    r.keyboard('[ctrl]a')
    r.keyboard('[ctrl]c')
    #print(r.clipboard())
    r.keyboard('[ctrl]q')
    data=r.clipboard()
    
    

    product_name=re.findall('(?<=Product Name : ).*',data)[0].strip()
    seller=re.findall('(?<=Seller : ).*',data)[0].replace("\n","").strip()
    price=re.findall('(?<=Price : ).*',data)[0].strip()


    return [product_name,seller,price]

r.init(visual_automation = True, chrome_browser = True)
r.url('https://excelcult.com/inventorymanagement/')
r.click('//button[@id="btn-delete"]')

insert_files=glob.glob('insert\\*.pdf')

for f in insert_files:
    data= data_extract(f)
    r.type('//input[@id="proname"]',data[0])
    r.type('//input[@id="seller"]',data[1])
    r.type('//input[@id="price"]',data[2])
    r.click('//button[@id="btn-create"]')

update_files=glob.glob('update\\*.pdf')

for f in update_files:
    data= data_extract(f)
    xpath='//tr[td[2][text()="'+data[0]+'"] and td[3][text()="'+data[1]+'"]]/td[5]/img'
    r.click(xpath)
    r.type('//input[@id="price"]','[clear]'+data[2])
    r.click('//button[@id="btn-update"]')


delete_files=glob.glob('delete\\*.pdf')

for f in delete_files:
    data= data_extract(f)
    xpath='//tr[td[2][text()="'+data[0]+'"] and td[3][text()="'+data[1]+'"]]/td[6]/img'
    r.click(xpath)


r.click('//button[@id="btn-read"]')

r.snap('//table[@class="table table-striped"]','results.png')

r.close()
r.run('start results.png')



    




    
