from typing import List


class LogBody:
    def str_to_bool(self, value: str) -> bool:
        if value == "True":
            return True
        else:
            return False

    # def __init__(self, id,
    #              apk_id: str, processed: str,
    #              downloaded: str, multidex: str, sha1: str):
    #     self.id: int = id
    #     self.apk_id: str = apk_id
    #     self.processed: bool = self.str_to_bool(processed)
    #     self.downloaded: bool = self.str_to_bool(downloaded)
    #     self.multidex: bool = self.str_to_bool(multidex)
    #     self.sha1: str = sha1

    def __init__(self, log_content: List[str]):
        self.id: int = int(log_content[0])
        self.apk_id: str = log_content[1]
        self.processed: bool = self.str_to_bool(log_content[2])
        self.downloaded: bool = self.str_to_bool(log_content[3])
        self.multidex: bool = self.str_to_bool(log_content[4])
        self.sha1: str = log_content[5]

    def __str__(self):
        return "{},{},{},{},{},{}".format(self.id,
                                          self.apk_id,
                                          self.processed,
                                          self.downloaded,
                                          self.multidex,
                                          self.sha1)


class FullLog():

    def __init__(self, log_file_path: str):
        self.log_file_path: str = log_file_path
        with open(self.log_file_path, "r") as log_file:
            self.raw_lines: List[str] = log_file.readlines()
        log_file.close()
        self.logs: List[LogBody] = []
        for line in self.raw_lines:
            current = line.strip()
            logBody = LogBody(current.split(","))
            self.logs.append(logBody)
        self.size = len(self.logs)
        self.__find_total_downloaded_apps()
        self.__count_multidex_apps()

    def __find_total_downloaded_apps(self):
        count: int = 0
        for log in self.logs:
            if log.downloaded:
                count += 1
        self.count_downloaded = count

    def find_total_downloaded_apps(self):
        return self.count_downloaded

    def __count_multidex_apps(self):
        count: int = 0
        for log in self.logs:
            if log.downloaded and log.multidex:
                count += 1
        self.count_multidex = count

    def count_multidex_apps(self):
        return self.count_multidex
    # def find_multidex(self):
    #     for log in self.logs:

    def __str__(self):
        output = "total apps in list: {}\n"
        output += "downloaded from list: {}\n"
        output += "multidex from downloaded: {}\n"
        output += "percentage of multidex/downloaded: {}\n"
        return output.format(self.size,
                             self.count_downloaded,
                             self.count_multidex,
                             round(
                                 self.count_multidex /
                                 self.count_downloaded * 100, 2))


if __name__ == "__main__":
    fullLog = FullLog("LOG.csv")
    # print(fullLog.find_total_downloaded_apps())
    # print(fullLog.count_multidex_apps())
    print(fullLog)
    # OUTPUT_CSV_HEADER = "Index,ID,Processed,Downloaded,Multidex,SHA1"
