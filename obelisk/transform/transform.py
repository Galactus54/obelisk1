import logging
import os
from pathlib import Path
from zipfile import ZipFile
from typing import List, Dict, Union

import pandas as pd

import obelisk.config as c

logger = logging.getLogger(__name__)


class FileSplitter(object):
    """
    A object to store and convert optical information

    >> import obelisk
    >> splitter = obelisk.FileSplitter('path_to_file', 'desired_output_dir')
    >> splitter.process_input()
    """
    def __init__(self, file: Union[str, Path], output_dir: Union[str, Path]):
        self.c = c
        self.file = file
        self.output_dir = output_dir
        self.is_valid = self.validate_format()

    def process_input(self):
        """

        """
        self.read_file_to_dataframe()
        self.read_footer()
        self.create_object_handles()
        self.export()

    def convert_wavelength_labels(self, wavelength: str) -> str:
        """

        """
        lbl = wavelength
        w_tokens = lbl.split(' ')

        try:
            lbl = "{:.6e}".format(int(w_tokens[0]))
        except ValueError as e:
            pass

        return lbl

    def read_file_to_dataframe(self):

        # read in data
        skiprows = self.c.HEADER_ROWS + self.c.HEADER_SKIP_ROWS
        df = pd.read_csv(
            self.file,
            sep='\t',
            skiprows=skiprows,
        )

        # clean column labels
        cols = df.columns
        cols = [self.convert_wavelength_labels(col.strip()) for col in cols]
        df.columns = cols

        # discard rows in footer
        df.dropna(thresh=12, inplace=True)

        # transform some data
        self.data_cols = sorted([col for col in cols if 'e+02' in col])
        df['isProtected'] = df['Site Type'].apply(lambda x: str(int(x == 'Protected')))
        df['replicate'] = df['Subsite'].apply(self.subsite_split)

        self.df = df
        self.df_len = len(df)
        self.unique_subjects = df['Subject ID'].dropna().nunique()

    def subsite_split(self, subsite: str):
        try:
            return subsite.split(' ')[1]
        except:
            pass

    def create_object_handles(self):

        handles = {}
        self.df = self.df.merge(self.footer, on='Subject ID', how='left')

        for i, row in self.df.iterrows():
            subject_id = str(int(row.loc['Subject Index'])).zfill(4)
            protection = row.loc['isProtected']
            product_id = row.loc['Site Label'] # .split('_')[0]
            replicate = row.loc['replicate']

            data_df = row.loc[self.data_cols].to_frame()
            this_handle = subject_id + protection + product_id + '_' + replicate
            handles[this_handle] = data_df

            try:
                assert len(handles) == i + 1
            except:
                logger.error('Data integrity issue on line {} of main data'.format(i))
                # TODO
                return None

        self.handles = handles

    def read_header(self):
        header = pd.read_csv(self.file, sep='\t', nrows=self.c.HEADER_ROWS)
        self.header = header

    def read_footer(self):
        skips = (
            self.c.HEADER_ROWS + self.c.HEADER_SKIP_ROWS +
            1 + self.df_len + self.c.FOOTER_SKIP_ROWS
        )

        footer = pd.read_csv(self.file, sep='\t', skiprows=skips)
        footer = footer[['Subject Index', 'Subject ID']]
        self.footer = footer

    def validate_format(self):
        return None

    def export(self):

        Path(self.output_dir).mkdir(parents=True, exist_ok=True)

        for k, v in self.handles.items():
            v.to_csv(os.path.join(self.output_dir, k),
                     sep='\t', index=True, header=False)
