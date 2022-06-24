import concurrent.futures
import argparse
import shutil
import os
from typing import Dict, List
from flask import Flask
from flask_cors import CORS
import magic
from termcolor import cprint
from tempfile import TemporaryDirectory
import imagehash
from PIL import Image, ExifTags
import sqlite3
from jinja2 import FileSystemLoader, Environment
from more_itertools import chunked
import webbrowser
import math


# code inspired from https://github.com/philipbl/duplicate-images.git
# doing this because,
# 1) learning poetry
# 2) original does not work / can not make it work
# 3) don't want mongo
# 4) just so

class ImageHolder:
    def __init__(self,
                 file_path: str, hashes: str, file_size: str, image_size: str,
                 capture_time: str) -> None:
        self.file_path = file_path
        self.hashes = hashes
        self.file_size = file_size
        self.image_size = image_size
        self.capture_time = capture_time

    def __str__(self) -> str:
        return "{}, {}, {}, {}, {}".format(
            self.file_path, self.hashes, self.file_size,
            self.image_size, self.capture_time)

    def __repr__(self):
        return "\n"+str(self)

    def __sub__(self, other) -> int:
        if other is None:
            raise TypeError('Other hash must not be None.')
        return abs(
            imagehash.hex_to_hash(self.hashes) -
            imagehash.hex_to_hash(other.hashes))


def _get_file_size(file_name):
    try:
        return os.path.getsize(file_name)
    except FileNotFoundError:
        return 0


def _get_image_size(img):
    return "{} x {}".format(*img.size)


def _get_capture_time(img):
    try:
        exif = {
            ExifTags.TAGS[k]: v
            for k, v in img._getexif().items()
            if k in ExifTags.TAGS
        }
        return exif["DateTimeOriginal"]
    except:
        return "Time unknown"


def get_image_files(path):
    """
    Check path recursively for files. If any compatible file is found, it is
    yielded with its full path.

    :param path:
    :return: yield absolute path
    """

    def is_image(file_name):
        # List mime types fully supported by Pillow
        full_supported_formats = ['gif', 'jp2', 'jpeg', 'pcx', 'png', 'tiff',
                                  'x-ms-bmp',
                                  'x-portable-pixmap', 'x-xbitmap']
        try:
            mime = magic.from_file(file_name, mime=True)
            return mime.rsplit('/', 1)[1] in full_supported_formats
        except IndexError:
            return False

    path = os.path.abspath(path)
    for root, dirs, files in os.walk(path):
        for file in files:
            file = os.path.join(root, file)
            if is_image(file):
                yield file


def hash_file(file):
    try:
        hashes = []
        img = Image.open(file)

        file_size = _get_file_size(file)
        image_size = _get_image_size(img)
        capture_time = _get_capture_time(img)

        # hash the image 4 times and rotate it by 90 degrees each time
        # for angle in [0, 90, 180, 270]:
        #     if angle > 0:
        #         turned_img = img.rotate(angle, expand=True)
        #     else:
        #         turned_img = img
        #     hashes.append(str(imagehash.phash(turned_img)))

        # hashes = ''.join(sorted(hashes))

        hashes = str(imagehash.phash(img))

        cprint("\tHashed {}".format(file), "blue")
        return file, hashes, file_size, image_size, capture_time
    except OSError:
        cprint("\tUnable to open {}".format(file), "red")
        return None


def hash_files_parallel(files, num_processes=None):
    with concurrent.futures.ProcessPoolExecutor(
            max_workers=num_processes) as executor:
        for result in executor.map(hash_file, files):
            if result is not None:
                yield result


def _in_database(file: str, connect: sqlite3.Cursor):
    sql = '''
    select id from images
    where id = "{}"
    ;'''.format(file)
    result = connect.execute(sql).fetchone()
    return result


def new_image_files(files, connect: sqlite3.Cursor):
    for file in files:
        if _in_database(file, connect):
            cprint("\tAlready hashed {}".format(file), "green")
        else:
            yield file


def prepare_results(file_, hash_, file_size, image_size, capture_time):
    pass


def list_all_images(cursor: sqlite3.Cursor) -> List[ImageHolder]:
    image_holders: List[ImageHolder] = []
    query = '''
    select id, hashes, file_size, image_size, image_date from images
    order by hashes desc
    ;'''
    cursor.execute(query)
    hashes: List = cursor.fetchall()
    for hash in hashes:
        image_holders.append(
            ImageHolder(
                hash[0],
                hash[1],
                hash[2],
                hash[3],
                hash[4]))
    return image_holders


def find_exact_duplicate_image_hashes(cursor: sqlite3.Cursor):
    query = '''
    select hashes
    from images
    group by hashes
    having count(hashes)>=2
    order by count(hashes) desc
    ;'''
    cursor.execute(query)
    hashes: List = cursor.fetchall()
    cprint("found exact " + str(len(hashes)) + " images", "blue")
    return hashes


def add(paths, cursor: sqlite3.Cursor, num_processes=None):
    for path in paths:
        cprint("Hashing {}".format(path), "blue")
        files = get_image_files(path)
        files = new_image_files(files, cursor)
        results: List = []
        for result in hash_files_parallel(files, num_processes):
            results.append((
                result[0],
                result[1],
                result[2],
                result[3],
                result[4])
            )
        sql = 'INSERT into images values(?,?,?,?,?);'
        result = cursor.executemany(sql, results)

        cprint("...done inserting "+str(result.rowcount), "blue")
        cursor.connection.commit()


# def remove(paths, db):
#     for path in paths:
#         files = get_image_files(path)

#         # for file in files:
#         #     remove_image(file, db)


def remove_image(file, cursor: sqlite3.Cursor):
    cursor.execute("DELETE from IMAGES where id=?", (file,))
    cursor.connection.commit()


# def clear(db):
#     # db.drop()
#     # TODO
#     pass


def show(cursor: sqlite3.Cursor):
    cprint("showing duplicates", "blue")
    all_images: List[ImageHolder] = list_all_images(cursor)
    duplicate_group_indices = find_duplicate_groups_indices(
        all_images, simple_diff, 10)
    duplicates = package_duplicates(all_images, duplicate_group_indices)
    display_duplicates(duplicates, cursor)


def find_duplicate_groups_indices(entities: List, diff_method,
                                  threshold: int = 4) -> List:
    groups: List = []
    if len(entities) <= 1:
        return []
    m = 0
    n = m + 1
    flag = False
    for i in range(0, len(entities)):
        if n >= len(entities):
            # print("triggered last group condition")
            if m != n-1:
                last_group_diff: int = diff_method(
                    entities[m], entities[n-1])
                if last_group_diff <= threshold:
                    # print("adding last group diff: ", m, n-1)
                    groups.append((m, n-1))
            break
        if (
            (diff_method(entities[m], entities[n]) <= threshold)
                and (n < len(entities))):
            flag = True
            n = n+1
        else:
            if (flag):
                groups.append((m, n-1))
                flag = False
            m = n
            n = n + 1
    return groups


def print_duplicates(entities: List[ImageHolder], groups: List):
    cprint("printing duplicates now")
    for i in range(0, len(groups)):
        start, end = groups[i]
        cprint("group "+str(i), "blue")
        for j in range(start, end+1):
            cprint(entities[j], "yellow")


def package_duplicates(entities: List[ImageHolder], groups: List):
    duplicate_groups: List = []
    cprint("packaging duplicates now")
    for i in range(0, len(groups)):
        current_duplicate_group: Dict = {}

        start, end = groups[i]
        cprint("group "+str(i), "blue")

        current_duplicate_group['_id'] = i
        current_duplicate_group['items'] = []
        current_duplicate_group['total'] = (end-start+1)
        for j in range(start, end+1):
            cprint(entities[j], "yellow")
            current_duplicate_group['items'].append({
                "file_name": entities[j].file_path,
                "file_size": entities[j].file_size,
                "image_size": entities[j].image_size,
                "capture_time": entities[j].capture_time
            })
        duplicate_groups.append(current_duplicate_group)
    return duplicate_groups

def delete_picture(file_name, cursor: sqlite3.Cursor, trash="./Trash/"):
    cprint("Moving {} to {}".format(file_name, trash), 'yellow')
    if not os.path.exists(trash):
        os.makedirs(trash)
    try:

        shutil.move(file_name, trash + os.path.basename(file_name))
        remove_image(file_name, cursor)
    except FileNotFoundError:
        cprint("File not found {}".format(file_name), 'red')
        return False
    except Exception as e:
        cprint("Error: {}".format(str(e)), 'red')
        return False

    return True


def delete_duplicates(duplicates, db):
    results = [delete_picture(x['file_name'], db)
               for dup in duplicates for x in dup['items'][1:]]
    cprint("Deleted {}/{} files".format(results.count(True),
                                        len(results)), 'yellow')


def display_duplicates(duplicates, cursor: sqlite3.Cursor, trash="./Trash/"):
    from werkzeug.routing import PathConverter

    class EverythingConverter(PathConverter):
        regex = '.*?'

    app = Flask(__name__)
    CORS(app)
    app.url_map.converters['everything'] = EverythingConverter

    def render(duplicates, current, total):
        env = Environment(loader=FileSystemLoader('template'))
        template = env.get_template('index.html')
        return template.render(duplicates=duplicates,
                               current=current,
                               total=total)

    with TemporaryDirectory() as folder:
        # Generate all of the HTML files
        chunk_size = 25
        for i, dups in enumerate(chunked(duplicates, chunk_size)):
            with open('{}/{}.html'.format(folder, i), 'w') as f:
                f.write(render(dups,
                               current=i,
                               total=math.ceil(len(duplicates) / chunk_size)))

        webbrowser.open("file://{}/{}".format(folder, '0.html'))

        @app.route('/picture/<everything:file_name>', methods=['DELETE'])
        def delete_picture_(file_name, trash=trash):
            return str(delete_picture(file_name, cursor, trash))
            # print(file_name)
            pass

        app.run()


def cleanup_db(all_images: List[ImageHolder], cursor: sqlite3.Cursor):
    count = 0
    for image in all_images:
        if not os.path.exists(image.file_path):
            print("removing: " + str(image.file_path))
            remove_image(image.file_path, cursor)
            count += 1
    cprint("finished cleanup! removed {} images".format(str(count)), "blue")


def connect_to_db(db_conn_string: str) -> sqlite3.Connection:
    connect = sqlite3.connect(db_conn_string, check_same_thread=False)
    return connect


def imagehash_diff(hexstr1: str, hexstr2: str):
    return abs(imagehash.hex_to_hash(hexstr1) - imagehash.hex_to_hash(hexstr2))


def create_table(cursor: sqlite3.Cursor):
    cprint("creating table in db", "blue")
    sql = '''
    create table images
    (
        id TEXT Primary Key NOT NULL,
        hashes TEXT NOT NULL,
        file_size TEXT NOT NULL,
        image_size TEXT NOT NULL,
        image_date TEXT NOT NULL
    );
    '''
    try:
        cursor.execute(sql)
        cprint("Table created!", "green")
        cursor.connection.commit()
    except sqlite3.OperationalError:
        cprint("Table already exists", "red")


def simple_diff(i, j):
    return i-j


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='duplicate image finder')

    parser.add_argument('--add')

    group = parser.add_mutually_exclusive_group()
    group.add_argument('--show', action='store_true')
    group.add_argument('--cleanup', action='store_true')
    parser.add_argument('--db')
    parser.add_argument('--parallel')
    args = parser.parse_args()
    print(args)

    if args.db:
        DB_PATH = args.db
    else:
        DB_PATH = "./duplicate.sqlite"
    cursor: sqlite3.Cursor = connect_to_db(DB_PATH).cursor()
    create_table(cursor)

    if args.parallel:
        NUM_PROCESSES = int(args.parallel)
    else:
        NUM_PROCESSES = None

    if args.add:
        cprint("adding duplicates", "blue")
        add([args.add], cursor, num_processes=NUM_PROCESSES)
    elif args.show:
        show(cursor)
        cursor.connection.close()
    elif args.cleanup:
        cprint("cleaning up database of duplicates", "blue")
        all_images: List[ImageHolder] = list_all_images(cursor)
        cleanup_db(all_images, cursor)
