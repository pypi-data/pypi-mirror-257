#  Copyright (C) 2023 Y Hsu <yh202109@gmail.com>
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public license as published by
#  the Free software Foundation, either version 3 of the License, or
#  any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU General Public License for more details
#
#  You should have received a copy of the GNU General Public license
#  along with this program. If not, see <https://www.gnu.org/license/>


import os
from mtbp3.util.lsr import LsrTree
import re
import glob
import csv
import mtbp3
import pandas as pd

class Emt:
    """A class representing MedDRA terms.

    This class provides methods to interact with the Emt object,
    including listing files associated with the Emt.

    Attributes:
        folder_name (str): The folder name associated with the Emt.
        lsr (LsrTree): An instance of the LsrTree class for listing files.
        month (str): The month of the version published.
        year (str): The year of the version published.
    """


    def __init__(self, folder_name=''):
        """
        Initialize a new Emt object.

        Args:
            folder_name (str, optional): The folder name associated with the Emt.
                If not provided, the default folder name will be used.
        """
        if folder_name:
            self.folder_name = folder_name
        else:
            self.folder_name = mtbp3.get_data('test_emt/MedDRA')
        
        self.version_number = "00.0"
        self.version_number_us = "00_0"
        self.readme_file = None
        self.year = ""
        self.month = ""
        self.language = ""
        self.mdhier = None

        meddra_release_file = os.path.join(self.folder_name, 'MedAscii', 'meddra_release.asc')
        if os.path.isfile(meddra_release_file):
            with open(meddra_release_file, 'r') as file:
                reader = csv.reader(file, delimiter='$')
                header = next(reader)
                self.version_number = header[0]
                self.version_number_us = self.version_number.replace(".", "_")
                self.language = header[1]
        else:
            raise FileNotFoundError("meddra_release.asc file not found.")

        pattern = os.path.join(self.folder_name, '!!readme_[1-3][0-9]_[0-1]_English.txt')
        files = glob.glob(pattern, recursive=False)
        if len(files) == 1:
            self.readme_file = files[0]
        else:
            raise ValueError("Readme file not found or multiple files found.")

        with open(self.readme_file, 'r') as file:
            lines = file.readlines()[-3:]
            for line in lines:
                match = re.search(r'\b(January|February|March|April|May|June|July|August|September|October|November|December)\b \d{4}', line)
                if match:
                    self.month, self.year = match.group().split()
                    break


    def expected_file_lists(self):
        """
        Get the three lists of files associated with the Emt.

        Returns:
            tuple: A tuple containing three lists of file names.
        """
        support_doc_files = [
            f"!!readme_{self.version_number_us}_English.txt",
            f"detail_report_{self.version_number_us}_English.pdf",
            f"dist_file_format_{self.version_number_us}_English.pdf",
            f"intguide_{self.version_number_us}_English.pdf",
            f"SMQ_intguide_{self.version_number_us}_English.pdf",
            f"SMQ_spreadsheet_{self.version_number_us}_English.xlsx",
            f"version_report_{self.version_number_us}_English.xlsx",
            f"whatsnew_{self.version_number_us}_English.pdf",
        ]
        med_ascii_files = [
            "hlgt.asc", "hlgt_hlt.asc", "hlt.asc", "hlt_pt.asc", "intl_ord.asc",
            "llt.asc", "mdhier.asc", "meddra_history_english.asc", "meddra_release.asc", 
            "pt.asc", "smq_content.asc", "smq_list.asc", "soc.asc", "soc_hlgt.asc"
        ]
        med_ascii_files = ["/MedAscii/" + file for file in med_ascii_files] 
        seq_ascii_files = [
            "hlgt.seq", "hlgt_hlt.seq", "hlt.seq", "hlt_pt.seq", "intl_ord.seq",
            "llt.seq", "mdhier.seq", "pt.seq", "soc.seq", "soc_hlgt.seq"
        ]
        seq_ascii_files = ["/SeqAscii/" + file for file in seq_ascii_files] 
        return support_doc_files, med_ascii_files, seq_ascii_files

    def find_files(self, load_if_all_found=True):
        """
        Find all expected files associated with the Emt.

        Returns:
            list: A list of missing file names.
        """
        lsr = LsrTree(self.folder_name, outfmt="list")
        lsr_files = lsr.list_files()
        support_doc_files, med_ascii_files, seq_ascii_files = self.expected_file_lists()

        missing_files = []
        for file in support_doc_files + med_ascii_files + seq_ascii_files:
            if file not in lsr_files:
                missing_files.append(file)

        if not missing_files:
            mdhierasc = os.path.join(self.folder_name, 'MedAscii', 'mdhier.asc')
            self.mdhier = pd.read_csv(mdhierasc, delimiter='$', header=None, dtype=str)
            nsoc = len(self.mdhier[7].unique())
            return [], f"All files found. Version: {self.version_number}; Year: {self.year}; Month: {self.month}; Language: {self.language}. N_SOC: {nsoc}."
        else:
            return missing_files, f"{len(missing_files)} files not found."

    def list_files(self):
        """
        List all files associated with the Emt.

        Returns:
            list: A list of file names.
        """
        lsr = LsrTree(self.folder_name, outfmt="tree", with_counts=True)
        lsr_files = lsr.list_files()
        return lsr_files

    def find_soc(self, soc_name=[]):
        """
        Find all unique SOC (System Organ Class) names.

        Args:
            soc_name (str, optional): The specific SOC name to filter the results. Defaults to "".

        Returns:
            list: A list of unique SOC names. If soc_name is provided, it returns id.
        """
        subset = self.mdhier[[3, 7]].drop_duplicates()
        if soc_name:
            assert isinstance(soc_name, list), "soc_name must be a list"
            if all(isinstance(elem, str) and elem.isdigit() for elem in soc_name):
                assert all(elem in subset[3].tolist() for elem in soc_name), "All elements of soc_name must be present in subset[3]"
                out = pd.merge(pd.DataFrame(soc_name), subset, left_on=0, right_on=3)[7].tolist()
            else:
                assert all(elem in subset[7].tolist() for elem in soc_name), "All elements of soc_name must be present in subset[3]"
                out = pd.merge(pd.DataFrame(soc_name), subset, left_on=0, right_on=7)[3].tolist()
        else:
            out = subset[7].tolist()
        return out

    def find_pt_given_soc(self, soc_name, primary_soc_only=False):
        """
        Find all PTs (Preferred Terms) given a SOC (System Organ Class) name.

        Args:
            soc_name (str): The name of the SOC.
            primary_soc_only (bool, optional): If True, only return PTs associated with the primary SOC. 
                                                Defaults to False.

        Returns:
            pandas.DataFrame: A DataFrame containing the PTs associated with the given SOC. 
                                Each row represents a PT and contains the PT code and PT name.
        """
        meddra_mdhier = os.path.join(self.folder_name, 'MedAscii', 'mdhier.asc')

        df = pd.read_csv(meddra_mdhier, delimiter='$', header=None, dtype=str)
        if primary_soc_only:
            subset_df = df[(df[7] == soc_name) & (df[11] == 'Y')][[0, 4]].reset_index(drop=True)
            subset_df.columns = ['Id', 'Name']
        else:
            subset_df = df[df[7] == soc_name][[0, 4, 11]].reset_index(drop=True)
            subset_df.columns = ['Id', 'Name', 'Primary']
            
        return subset_df

if __name__ == "__main__":
    emt = Emt()
    print(emt.find_files())
    soc_names = emt.find_soc()
    print(soc_names)
    id=emt.find_soc(soc_names)
    print(id)
    print(emt.find_soc(id))
    #print(emt.find_pt_given_soc(soc_names[0]).head())
    #pass



