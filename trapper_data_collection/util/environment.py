# -------------------------------------------------------------------------------
# Name:        environment
# Purpose:
#
# Author:      gshevche
#
# Created:     05/02/2020
# Copyright:   (c) gshevche 2020
# Licence:     <your licence>
# -------------------------------------------------------------------------------

import os
import sys
import logging
import ctypes
import zipfile

from ctypes import wintypes
from xml.etree import ElementTree as eT
from datetime import datetime as dt


class Environment:
    """
    ------------------------------------------------------------------------------------------------------------
        CLASS: Contains general environment functions and processes that can be used in python scripts
    ------------------------------------------------------------------------------------------------------------
    """

    def __init__(self):
        pass

    # Set up variables for getting UNC paths
    mpr = ctypes.WinDLL('mpr')

    ERROR_SUCCESS = 0x0000
    ERROR_MORE_DATA = 0x00EA

    wintypes.LPDWORD = ctypes.POINTER(wintypes.DWORD)
    mpr.WNetGetConnectionW.restype = wintypes.DWORD
    mpr.WNetGetConnectionW.argtypes = (wintypes.LPCWSTR,
                                       wintypes.LPWSTR,
                                       wintypes.LPDWORD)

    @staticmethod
    def setup_logger(args):
        """
        ------------------------------------------------------------------------------------------------------------
            FUNCTION: Set up the logging object for message output

            Parameters:
                args: system arguments

            Return: logger object
        ------------------------------------------------------------------------------------------------------------
        """
        log_name = 'main_logger'
        logger = logging.getLogger(log_name)
        logger.handlers = []

        log_fmt = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        log_file_base_name = os.path.basename(sys.argv[0])
        log_file_extension = 'log'
        timestamp = dt.now().strftime('%Y-%m-%d_%H-%M-%S')
        log_file = '{}_{}.{}'.format(timestamp, log_file_base_name, log_file_extension)

        logger.setLevel(args.log_level)

        sh = logging.StreamHandler()
        sh.setLevel(args.log_level)
        sh.setFormatter(log_fmt)
        logger.addHandler(sh)

        if args.log_dir:
            try:
                os.makedirs(args.log_dir)
            except OSError:
                pass

            fh = logging.FileHandler(os.path.join(args.log_dir, log_file))
            fh.setLevel(args.log_level)
            fh.setFormatter(log_fmt)
            logger.addHandler(fh)

        return logger
