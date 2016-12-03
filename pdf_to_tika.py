#! /usr/bin/env python

# -*- coding: utf-8 -*-

import os
import platform
import sys
from datetime import datetime

import requests

from .utils import Colors, urls_dict

PDFS = sys.argv[1]
TXT_PATH_DOWNLOAD = sys.argv[2]


class Tika(object):
    """
    Usage: ./pdf_file_to_tika.py pdfs_dir tika_output_dir tika_url
    For example: ./pdf_file_to_grobid.py pdfs_data tika_output_data rs
    """

    def __init__(self, *args, **kwargs):
        self.pdfs_data = PDFS
        self.output_data = TXT_PATH_DOWNLOAD

    def create_output_directory(self):
        """
        General method to create output directory.
        """

        try:
            if not os.path.isdir(TXT_PATH_DOWNLOAD):
                return os.makedirs(TXT_PATH_DOWNLOAD)
        except OSError as e:
            print(Colors.FAIL + 'Error during creating output directory --> {}'.format(e) + Colors.ENDC)

    def prepare_pdfs(self):
        """
        General method to find recursively PDFs.
        """

        return sorted(
            [os.path.join(root, filename) for root, dirnames, filenames in os.walk(PDFS) for filename in filenames if
             filename.endswith('.pdf') and os.path.getsize(os.path.join(root, filename)) > 0])

    def get_current_data(self):
        """
        General method to return current date.
        """

        return datetime.now().replace(microsecond=0)

    def ping_host(self, host):
        """
        Returns True if host responds to a ping request.
        """

        ping_query = "-n 1" if platform.system().lower() == "windows" else "-c 1"

        return os.system("ping " + ping_query + " " + host) == 0

    def process_pdfs_to_tika(self):

        files = self.prepare_pdfs()

        print(Colors.OKGREEN + '*** Started processing at {} ***\n'.format(self.get_current_data()) + Colors.ENDC)

        with requests.Session() as session:

            tika_url = None

            if sys.argv[3] == 'tika':
                tika_url = urls_dict.get('tika', None)

            print(Colors.OKGREEN + '*** Checking if at least a host is available for now... ***' + Colors.ENDC)

            if self.ping_host(tika_url.split('/')[2].split(':')[0]) == 1:
                print(Colors.OKGREEN + '\n*** Host is working. Lets do some calculations! ***' + Colors.ENDC)

            else:
                print(Colors.FAIL + '*** Host is currently down. Please try again later... ***' + Colors.ENDC)
                return 1

            for i, file in enumerate(files):

                print(Colors.OKGREEN + "\nFile ID --> {index}/{n}".format(
                    index=i + 1,
                    n=len(files),
                ) + Colors.ENDC)

                print('File taken from --> ' + Colors.BOLD + '{}'.format(file) + Colors.ENDC)

                print('Attached PDF to be sent to TIKA.')

                pdf_file = open(file, 'rb')

                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
                }

                try:

                    tika = session.put(
                        tika_url,
                        data=pdf_file,
                        headers=headers,
                    )

                    if not tika.status_code == 200:

                        print(Colors.FAIL + 'Status --> {status_code}'.format(
                            status_code=tika.status_code) + Colors.ENDC)

                        print(Colors.BOLD + '________________________________________________' + Colors.ENDC)

                        with open('./tika_errors.txt', 'a') as log:
                            log.write(u'\n{time}\n{file_name} --> {status_code}\n'.format(
                                time=self.get_current_data(),
                                file_name=file,
                                status_code=tika.status_code,
                            ))
                    else:

                        print(Colors.WARNING + 'Status --> {status_code}'.format(
                            status_code=tika.status_code) + Colors.ENDC)

                        tika.encoding = 'utf-8'

                        print('Made PUT request to TIKA. ')

                        txt_file = tika.text

                        print('Received TXT from TIKA.')

                        splitted_file_path = file.split('/')

                        dir_path = os.path.join(
                            self.output_data
                        )

                        os.makedirs(dir_path, exist_ok=True)

                        with open('{files_path}/{file_name}{file_ext}'.format(
                                files_path=dir_path,
                                file_name=(os.path.splitext(splitted_file_path[-1])[0]),
                                file_ext='.txt'), 'w') as tika_output:
                            tika_output.write(txt_file)

                            print('Saved grobid TXT output to file!')

                            print(Colors.BOLD + '________________________________________________' + Colors.ENDC)

                except requests.exceptions.HTTPError as e:
                    print('Error --> {}'.format(e))

            print('\nFinished processing at {}\n'.format(self.get_current_data()))


tika_job = Tika(pdfs_data=PDFS, output_data=TXT_PATH_DOWNLOAD)
tika_job.process_pdfs_to_tika()