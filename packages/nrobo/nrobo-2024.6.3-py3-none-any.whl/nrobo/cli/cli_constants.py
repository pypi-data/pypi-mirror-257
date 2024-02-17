"""
=====================CAUTION=======================
DO NOT DELETE THIS FILE SINCE IT IS PART OF NROBO
FRAMEWORK AND IT MAY CHANGE IN THE FUTURE UPGRADES
OF NROBO FRAMEWORK. THUS, TO BE ABLE TO SAFELY UPGRADE
TO LATEST NROBO VERSION, PLEASE DO NOT DELETE THIS
FILE OR ALTER ITS LOCATION OR ALTER ITS CONTENT!!!
===================================================

Constants module.

@author: Panchdev Singh Chauhan
@email: erpanchdev@gmail.com
"""
import os


class NREPORT:
    """nRoBo report related constants"""

    HTML = "html"
    ALLURE = "allure"
    REPORT_DIR = "results"
    HTML_REPORT_NAME = "report.html"
    HTML_REPORT_PATH = REPORT_DIR + os.sep + HTML_REPORT_NAME
    LOG_DIR_DRIVER = "driver-logs"
    LOG_EXTENTION = ".log"
    LOG_DIR_TEST = "test-logs"
    SCREENSHOTS_DIR = "screenshots"
    ALLURE_REPORT_PATH = REPORT_DIR + os.sep + ALLURE
    NROBO_FRAMEWORK_TESTS_DIR = "nrobo_framework_tests"


class nCLI:
    """List of nrobo defined cli options.

    NOTE:
        when you add/remove an option from nCLI class,
        Make sure that the same option is also removed from the
        nCLI.ARGS dictionary too!!!"""

    INSTALL = "install"
    APP = "app"
    URL = "url"
    USERNAME = "username"
    PASSWORD = "password"
    INSTANCES = "instances"
    RERUNS = "reruns"
    RERUNS_DELAY = "reruns-delay"
    REPORT = "report"
    TESTDIR = "testsdir"
    TARGET = "target"
    VERSION = "VERSION"
    SUPPRESS = "suppress"
    BROWSER = "browser"
    BROWSER_CONFIG = "browser-config"
    KEY = "key"
    PACKAGES = "packages"
    GRID = "grid"

    ARGS = {
        INSTALL: INSTALL,
        APP: APP,
        URL: URL,
        USERNAME: USERNAME,
        PASSWORD: PASSWORD,
        INSTANCES: INSTANCES,
        RERUNS: RERUNS,
        REPORT: REPORT,
        TESTDIR: TESTDIR,
        TARGET: TARGET,
        VERSION: VERSION,
        SUPPRESS: SUPPRESS,
        BROWSER: BROWSER,
        BROWSER_CONFIG: BROWSER_CONFIG,
        KEY: KEY,
        PACKAGES: PACKAGES,
        GRID: GRID
    }

    DEFAULT_ARGS = {
        '--cache-clear': ['--cache-clear'],
        '--color': ['--color', 'yes'],
        '-r': ['-r', 'fE'],
        '--code-highlight': ['--code-highlight', 'yes'],
        '--junit-xml': ['--junit-xml', NREPORT.REPORT_DIR + os.sep + f"junit-report.xml"]
    }


class PACKAGES:
    """nRoBo packages"""

    NROBO = "nrobo"
    CLI = "cli"