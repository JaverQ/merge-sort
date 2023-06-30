import os, shutil, sys


class File:
    def __init__(self, file):
        self.file = file

    def pop(self):
        line = self.file.readline()
        if not line:
            return None
        else:
            return int(line)


def slice_file(input_file, output_file):
    line_number = 0
    folder_name = 'files'
    if not os.path.isdir("files"):
        os.mkdir("files")
    input_file_opened = open(input_file, "r")
    out_file = None
    out_file_name = None
    for line in input_file_opened:
        if line_number % 100000 == 0:
            if out_file:
                out_file.close()
                sort_file(out_file_name)
                print(f'Sorted file is created: {out_file_name}')
            out_file_name = f"{folder_name}/{line_number // 100000}"
            out_file = open(out_file_name, "w")
        out_file.write(line)
        line_number += 1
    input_file_opened.close()
    if out_file:
        out_file.close()
        sort_file(out_file_name)
    input_file_opened.close()
    sort_directory(folder_name, output_file)


def sort_file(input_file):
    list = []
    input_file_opened = open(input_file, "r")
    for line in input_file_opened:
        list.append(int(line))
    input_file_opened.close()
    sorted_list = merge_sort(list)
    out_file_opened = open(f"{input_file}.sorted", "w")
    for line in sorted_list:
        out_file_opened.write(f"{line}\r")
    out_file_opened.close()


def sort_directory(folder, output_file):
    list_of_files = []
    final_file = open(output_file, 'w')
    for root, dirs, files in os.walk(f'{folder}'):
        for file in files:
            if '.sorted' in file:
                current_file1 = open(f'{folder}/{file}', 'r')
                current_file2 = File(current_file1)
                list_of_files.append(current_file2)
    count = merge_sort_files(list_of_files, final_file)
    final_file.close()
    print(f'Total entries written: {count}')


def merge_sort_files(list_of_list, final_file):
    first_lines_list = []
    count = 0
    for list in list_of_list:
        first_lines_list.append(list.pop())
    while len(first_lines_list) > 0:
        sorted_first_lines_list = merge_sort(first_lines_list)
        index = 0
        for item in first_lines_list:
            if item == sorted_first_lines_list[0]:
                final_file.write(f'{str(item)}\r')
                count += 1
                if count % 100000 == 0:
                    print('100000 entries written...')
                value = list_of_list[index].pop()
                if value:
                    first_lines_list[index] = value
                else:
                    first_lines_list.pop(index)
                    list_of_list.pop(index)
            index += 1
    return count


def merge_sort(list):
    if len(list) > 1:
        l_list = list[:len(list) // 2]
        r_list = list[len(list) // 2:]
        l_sorted = merge_sort(l_list)
        r_sorted = merge_sort(r_list)
        return merge(l_sorted, r_sorted)
    else:
        return list


def merge(l_list, r_list):
    list2 = []
    while True:
        if not l_list:
            list2 += r_list
            return list2
        elif not r_list:
            list2 += l_list
            return list2
        else:
            if l_list[0] < r_list[0]:
                list2.append(l_list.pop(0))
            elif l_list[0] > r_list[0]:
                list2.append(r_list.pop(0))
            else:
                list2.append(l_list.pop(0))
                list2.append(r_list.pop(0))


slice_file(sys.argv[1], sys.argv[2])
shutil.rmtree('files')