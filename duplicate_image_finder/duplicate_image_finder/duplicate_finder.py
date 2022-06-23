import concurrent.futures
import argparse
import re
import shutil
import os
from typing import List
from venv import create
import magic
from termcolor import cprint
from pprint import pprint
import imagehash
import argparse
import json
from PIL import Image, ExifTags
import sqlite3

# code inspired from https://github.com/philipbl/duplicate-images.git
# doing this because,
# 1) learning poetry
# 2) original does not work / can not make it work
# 3) don't want mongo
# 4) just so

# data = {}
# file, hashes, file_size, image_size, capture_time
# cols = ["file",
#         "hashes",
#         "file_size",
#         "image_size",
#         "capture_time"]


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


def _add_to_database(file_, hash_, file_size, image_size, capture_time, db):
    #
    # TODO
    # try:
    #     db.insert_one({"_id": file_,
    #                    "hash": hash_,
    #                    "file_size": file_size,
    #                    "image_size": image_size,
    #                    "capture_time": capture_time})
    # except pymongo.errors.DuplicateKeyError:
    #     cprint("Duplicate key: {}".format(file_), "red")
    pass


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


def list_all(cursor: sqlite3.Cursor):
    query = '''
    select hashes, id from images
    order by hashes desc
    ;'''
    cursor.execute(query)
    hashes: List = cursor.fetchall()
    for hash in hashes:
        print(hash)


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


def remove(paths, db):
    for path in paths:
        files = get_image_files(path)

        # TODO: Can I do a bulk delete?
        # TODO
        # for file in files:
        #     remove_image(file, db)


def remove_image(file, db):
    # TODO
    # db.delete_one({'_id': file})
    pass


def clear(db):
    # db.drop()
    # TODO
    pass


def show(db):
    # TODO
    # total = db.count()
    # pprint(list(db.find()))
    # print("Total: {}".format(total))
    pass


def same_time(dup):
    # TODO
    pass
    # items = dup['items']
    # if "Time unknown" in items:
    #     # Since we can't know for sure, better safe than sorry
    #     return True

    # if len(set([i['capture_time'] for i in items])) > 1:
    #     return False

    # return True


def find_groups(hashes: List, threshold: int = 4) -> List:
    groups: List = []
    if len(hashes) <= 1:
        return []
    print(str(hashes))
    m = 0
    n = 1
    for i in range(0, len(hashes)):
        print(m, n, len(hashes))
        diff: int = abs(hashes[m] - hashes[n])
        if diff > threshold:
            groups.append((m, n-1))
            m = n
        n += 1
        if n >= len(hashes):
            if m != n-1:
                last_group_diff: int = abs(hashes[m] - hashes[n-1])
                if last_group_diff <= threshold:
                    groups.append((m, n-1))
            break
    return groups


def find(db, match_time=False):
    # TODO
    pass
    # dups = db.aggregate([{
    #     "$group": {
    #         "_id": "$hash",
    #         "total": {"$sum": 1},
    #         "items": {
    #             "$push": {
    #                 "file_name": "$_id",
    #                 "file_size": "$file_size",
    #                 "image_size": "$image_size",
    #                 "capture_time": "$capture_time"
    #             }
    #         }
    #     }
    # },
    #     {
    #         "$match": {
    #             "total": {"$gt": 1}
    #         }
    #     }])

    # if match_time:
    #     dups = (d for d in dups if same_time(d))

    # return list(dups)


def delete_picture(file_name, db, trash="./Trash/"):
    cprint("Moving {} to {}".format(file_name, trash), 'yellow')
    if not os.path.exists(trash):
        os.makedirs(trash)
    try:
        shutil.move(file_name, trash + os.path.basename(file_name))
        remove_image(file_name, db)
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


def display_duplicates(duplicates, db, trash="./Trash/"):
    # TODO
    pass
    # from werkzeug.routing import PathConverter
    # class EverythingConverter(PathConverter):
    #     regex = '.*?'

    # app = Flask(__name__)
    # CORS(app)
    # app.url_map.converters['everything'] = EverythingConverter

    # def render(duplicates, current, total):
    #     env = Environment(loader=FileSystemLoader('template'))
    #     template = env.get_template('index.html')
    #     return template.render(duplicates=duplicates,
    #                            current=current,
    #                            total=total)

    # with TemporaryDirectory() as folder:
    #     # Generate all of the HTML files
    #     chunk_size = 25
    #     for i, dups in enumerate(chunked(duplicates, chunk_size)):
    #         with open('{}/{}.html'.format(folder, i), 'w') as f:
    #             f.write(render(dups,
    #                            current=i,
    #                            total=math.ceil(len(duplicates) / chunk_size)))

    #     webbrowser.open("file://{}/{}".format(folder, '0.html'))

    #     @app.route('/picture/<everything:file_name>', methods=['DELETE'])
    #     def delete_picture_(file_name, trash=trash):
    #         return str(delete_picture(file_name, db, trash))

    #     app.run()


def cleanup_db(db):
    # TODO
    pass
    # images = list(db.find())
    # for image in images:
    #     image_path: str = image['_id']
    #     if not os.path.exists(image_path):
    #         print("removing: " + str(image['_id']))
    #         remove_image(image_path, db)


def connect_to_db(db_conn_string: str) -> sqlite3.Connection:
    connect = sqlite3.connect(db_conn_string)
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


if __name__ == '__main__':
    # pprint(hash_file("/Users/amitseal/pics/test/2020-05-01.jpg"))
    # from docopt import docopt

    # args = docopt(__doc__)

    parser = argparse.ArgumentParser(description='duplicate image finder')

    # parser.add_argument('integers', metavar='N', type=int, nargs='+',
    #                 help='an integer for the accumulator')
    # parser.add_argument('--sum', dest='accumulate', action='store_const',
    #                 const=sum, default=max,
    #                 help='sum the integers (default: find the max)')

    # parser.add_argument('add')
    # parser.add_argument('remove')
    # parser.add_argument('clear')
    # parser.add_argument('show')
    # parser.add_argument('find')
    # parser.add_argument('--delete')
    # parser.add_argument('--print')
    parser.add_argument('--db')
    # parser.add_argument('--parallel')
    # parser.add_argument('cleanup')
    # parser.add_argument('--match_time')
    args = parser.parse_args()

    # print(args.accumulate(args.integers))

    # if args['--trash']:
    #     TRASH = args['--trash']
    # else:
    #     TRASH = "./Trash/"

    if args.db:
        DB_PATH = args.db
    else:
        DB_PATH = "./duplicate.sqlite"
    cursor = connect_to_db(DB_PATH).cursor()
    create_table(cursor)
    # _in_database('/Users/amitseal/pics/test/2020-05-01.jpg', connect)
    add(["/Users/amitseal/pics/test/"], cursor)
    find_exact_duplicate_image_hashes(cursor)
    list_all(cursor)
    cursor.connection.close()
    print(type(imagehash_diff('f2c34972aace9670', 'eee4853a6087f686')))
    # if args.parallel:
    #     NUM_PROCESSES = int(args.parallel)
    # else:
    #     NUM_PROCESSES = 0

    # with connect_to_db(db_conn_string=DB_PATH) as db:
    # if args.add:
    #     # add(args['<path>'], db, NUM_PROCESSES)
    #     pass
    # elif args.remove:
    #     # remove(args['<path>'], db)
    #     pass
    # elif args.clear:
    #     clear(db)
    # elif args.show:
    #     show(db)
    # elif args.find:
    #     dups = find(db, args.match_time)

    #     if args.delete:
    #         delete_duplicates(dups, db)
    #     elif args.print:
    #         pprint(dups)
    #         print("Number of duplicates: {}".format(len(dups)))
    #     else:
    #         display_duplicates(dups, db=db)
    # elif args.cleanup:
    #     cleanup_db(db)
