#! /usr/bin/env python

# -*- coding: utf-8 -*-

import os
import platform
import sys
from datetime import datetime

import requests

from .utils import Colors, urls_dict, headers

PDFS = sys.argv[1]
XMLS_PATH_DOWNLOAD = sys.argv[2]


class Grobid(object):
    """
    Usage: ./pdf_to_grobid.py pdfs_dir grobid_output_dir grobid_url
    For example: ./pdf_to_grobid.py pdfs_data grobid_output_data grobid
    """

    def __init__(self, *args, **kwargs):
        self.pdfs_data = PDFS
        self.output_data = XMLS_PATH_DOWNLOAD

    def create_output_directory(self):
        """
        General method to create output directory.
        """

        try:
            if not os.path.isdir(XMLS_PATH_DOWNLOAD):
                return os.makedirs(XMLS_PATH_DOWNLOAD)
        except OSError as e:
            print(Colors.FAIL + 'Error during creating output directory --> {}'.format(e) + Colors.ENDC)

    def prepare_pdfs(self):
        """
        General method to find recursively PDFs.
        """

        return sorted(
            [os.path.join(root, filename) for root, dirnames, filenames in os.walk(self.pdfs_data) for filename in
             filenames if filename.endswith('.pdf') and os.path.getsize(os.path.join(root, filename)) > 0])

    def ping_host(self, host):
        """
        Returns True if host responds to a ping request.
        """

        ping_query = "-n 1" if platform.system().lower() == "windows" else "-c 1"

        return os.system("ping " + ping_query + " " + host) == 0

    def get_current_data(self):
        """
        General method to return current date.
        """

        return datetime.now().replace(microsecond=0)

    def process_pdfs_to_grobid(self):

        self.create_output_directory()

        files = self.prepare_pdfs()

        print(Colors.OKGREEN + '*** Started processing at {} ***\n'.format(self.get_current_data()) + Colors.ENDC)

        with requests.Session() as session:

            grobid_url = None

            if sys.argv[3] == 'grobid':
                grobid_url = urls_dict.get('grobid', None)

            print(Colors.OKGREEN + '*** Checking if at least a host is available for now... ***' + Colors.ENDC)

            if self.ping_host(grobid_url.split('/')[2].split(':')[0]) == 1:
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

                print('Attached PDF to be sent to grobid.')

                pdf = open(file, 'rb')

                pdf_file = {
                    'input': pdf
                }

                try:

                    grobid = session.post(
                        grobid_url,
                        files=pdf_file,
                        headers=headers,
                    )

                    if not grobid.status_code == 200:

                        print(Colors.FAIL + 'Status --> {status_code}'.format(
                            status_code=grobid.status_code) + Colors.ENDC)

                        print(Colors.BOLD + '________________________________________________' + Colors.ENDC)

                        with open('./grobid_errors.txt', 'a') as log:
                            log.write(u'\n{time}\n{file_name} --> {status_code}\n'.format(
                                time=self.get_current_data(),
                                file_name=file,
                                status_code=grobid.status_code,
                            ))
                    else:

                        print(Colors.WARNING + 'Status --> {status_code}'.format(
                            status_code=grobid.status_code) + Colors.ENDC)

                        print('Made POST request to grobid. ')

                        xml_file = grobid.content

                        print('Received XML from grobid.')

                        splitted_file_path = file.split('/')

                        dir_path = os.path.join(
                            self.output_data
                        )

                        os.makedirs(dir_path, exist_ok=True)

                        with open('{files_path}/{file_name}{file_ext}'.format(
                                files_path=dir_path,
                                file_name=os.path.splitext(splitted_file_path[-1])[0],
                                file_ext='.xml'), 'wb') as grobid_output:

                            if grobid.headers['content-type'] == 'application/xml':
                                grobid_output.write(xml_file)

                                print('Saved grobid XML output to file!')

                                print(Colors.BOLD + '________________________________________________' + Colors.ENDC)

                except requests.exceptions.HTTPError as e:
                    print('Error --> {}'.format(e))

            print('\nFinished processing at {}\n'.format(self.get_current_data()))


grobid_job = Grobid(pdfs_data=PDFS, output_data=XMLS_PATH_DOWNLOAD)
grobid_job.process_pdfs_to_grobid()
