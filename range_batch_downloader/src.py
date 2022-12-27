import argparse


def setup_arguments():
    parser = argparse.ArgumentParser(prog="Range Batch Downloader",
                                     description="Downloads a range of URLs")
    parser.add_argument("--us", type=str, required=True)
    parser.add_argument("--ue", type=str, required=False)
    parser.add_argument("--ns", type=int, required=True)
    parser.add_argument("--ne", type=int, required=True)
    return parser


def main():
    parser = setup_arguments()
    args = parser.parse_args()
    number_start = args.ns
    number_end = args.ne
    url_start = args.us
    url_end = None
    if args.ue:
        url_end = args.ue
    download_string = 'wget "{url_start}{current}{url_end}"'
    for i in range(number_start, number_end+1):
        formatted_string = download_string.format(url_start=url_start,
                                                  current=str(i), url_end=url_end)
        print(formatted_string)


if __name__ == "__main__":
    main()
