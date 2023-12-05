class FileReader:
    def __init__(self, file_path):
        self.file_path = file_path
    def __iter__(self):
        self.file = open(file=self.file_path)
        return self
    def __next__(self):
        line  = self.file.readline()
        if not line:
            self.file.close()
            raise StopIteration
        return line.strip()


# if __name__ == '__main__':

#     for line in FileReader("descriptions/001.txt"):
#         print(line)
import zipfile
import csv
import os

class FileReader:
    def __init__(self, zip_path, folder_inside_zip):
        self.zip_path = zip_path
        self.folder_inside_zip = folder_inside_zip
        self.file_list = []
        self.current_index = 0

        # Fayllarni olish
        self._get_file_list()

    def _get_file_list(self):
        with zipfile.ZipFile(self.zip_path, 'r') as zip_file:
            # Zip fayli ichidagi barcha fayllarni olish
            files = zip_file.namelist()
            
            # Zip fayli ichidagi fayllar orasida faqat belgilangan papkadagi fayllarni tanlash
            self.file_list = [file for file in files if file.startswith(self.folder_inside_zip) and file.endswith('.txt')]

    def __iter__(self):
        return self

    def __next__(self):
        if self.current_index < len(self.file_list):
            file_name = os.path.basename(self.file_list[self.current_index])
            file_path_inside_zip = self.file_list[self.current_index]
            
            with zipfile.ZipFile(self.zip_path, 'r') as zip_file:
                with zip_file.open(file_path_inside_zip) as file:
                    content = file.read().decode('utf-8')
            
            # Fayl nomi va o'qilgan ma'lumotni biriktirib o'tamiz
            result = {'name': file_name, 'price': len(content), 'description': content}
            
            self.current_index += 1
            return result
        else:
            # Barcha fayllar tugaguncha StopIteration qaytarib, iteratsiya tugaydi
            raise StopIteration

# FileReader obyekti yaratish va papkadan ma'lumotlarni olish
zip_path = 'D:\\n_23\\vazifa.zip'
folder_inside_zip = 'dars2/descriptions'

file_reader = FileReader(zip_path, folder_inside_zip)

# CSV faylga yozish
csv_header = ['name', 'price', 'description']
csv_file_path = 'output.csv'

with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
    csv_writer = csv.DictWriter(csv_file, fieldnames=csv_header)
    csv_writer.writeheader()

    # Iteratsiya orqali fayllardan ma'lumotlarni olish va CSV faylga yozish
    for file_info in file_reader:
        csv_writer.writerow(file_info)

print('CSV faylga ma\'lumotlar yozildi.')
