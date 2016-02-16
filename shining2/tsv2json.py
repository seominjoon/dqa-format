import sys
import csv
import json

def main(tsv_file_path, json_file_path, delimiter='\t'):
    x = []
    with open(tsv_file_path, 'rb') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=delimiter)
        for row in reader:
            for key in row:
                row[key] = row[key].decode('utf8').replace(u'\u00a0', ' ')
            x.append(row)
    print(len(x))
    json.dump(x, open(json_file_path, 'wb'))

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
