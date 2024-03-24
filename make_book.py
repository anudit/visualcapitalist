import os
from PyPDF2 import PdfReader, PdfWriter
from tqdm import tqdm
pdf_dir = './pdfs'

output_pdf_path = 'visualcapitalist_book.pdf'

writer = PdfWriter()

for filename in tqdm(os.listdir(pdf_dir)):
    if filename.endswith('.pdf'):
        filepath = os.path.join(pdf_dir, filename)
        
        reader = PdfReader(filepath)
        
        for page in reader.pages:
            writer.add_page(page)

print('Saving Combined PDF')
with open(output_pdf_path, 'wb') as out:
    writer.write(out)

print(f"Combined PDF created at {output_pdf_path}")
