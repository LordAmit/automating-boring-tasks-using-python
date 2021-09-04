from selenium import webdriver
import os
import sys

# dependencies
# selenium geckodriver for firefox - https://github.com/mozilla/geckodriver/releases
# geckodriver in PATH
# firefox installed and accessible in PATH
#


def download_apk(package_name):

    # remove spaces in between in the URL
    # also, f before " is important. don't remove.
    url = f"https://a p k p u r e .com/device-id/{package_name}/download?from=details"

    options = webdriver.FirefoxOptions()
    # commented in case you want to see what's going on
    # options.headless = True
    # set up profile
    fp = webdriver.FirefoxProfile()
    fp.set_preference("browser.download.folderList", 2)
    fp.set_preference("browser.download.manager.showWhenStarting", False)
    fp.set_preference("browser.download.dir", os.getcwd())
    fp.set_preference("browser.helperApps.neverAsk.saveToDisk",
                      "application/vnd.android.package-archive")

    driver = webdriver.Firefox(options=options, firefox_profile=fp)

    driver.get(url)

    driver.close()


if __name__ == '__main__':
    download_apk(sys.argv[1])
