import os
from tkinter import filedialog
from developer_functions_2 import *


def browse_folder():
    row_column = []

    m = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'eleven', 'twelve',
         'thirteen', 'fourteen', 'fifteen', 'sixteen', 'seventeen', 'eighteen', 'nineteen']

    folder_name = filedialog.askdirectory()
    folder_name = os.path.basename(folder_name)
    directory = folder_name + '/'

    list_subfolder = [f.name for f in os.scandir(directory) if f.is_dir()]

    row_column.append(len(folder_name))
    row_column.append(len(list_subfolder))

    for i in list_subfolder[:]:
        if i == 'RESULT': continue
        location = directory + i + '/'
        file_list = os.listdir(location)

        for j in file_list[:]:
            path = location + j
            file_name = j.split('.jpg')[0]
            mcq_evaluate(m, path, folder_name, i, file_name)

