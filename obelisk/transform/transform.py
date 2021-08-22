import logging
from zipfile import ZipFile
from tempfile import TemporaryDirectory, TemporaryFile
from typing import List, Dict, Union

from pandas import pd

import obelisk.config as c

logger = logging.getLogger(__name__)


class FileSplitter(object):
    """
    """
    def __init__(self, file):
        self.c = c
        self.file = file
        self.is_valid = self.validate_format()

    def process_input(self):
        self.read_file_to_dataframe()
        self.read_footer()
        self.create_object_handles()
        self.export()

    def convert_wavelength_labels(self, wavelength: str) -> str:

        lbl = wavelength
        w_tokens = wavelength.split(' ')

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
        df.dropna(thresh=5, inplace=True)

        # transform some data
        self.data_cols = sorted([col for col in cols if 'E+2' in col])
        df['isProtected'] = df['Site Type'].apply(lambda x: str(int(x == 'Protected')))
        df['replicate'] = df['Subsite'].apply(lambda x: x.split(' ')[1])

        self.df = df
        self.df_len = len(df)
        self.unique_subjects = df['Subject ID'].dropna().nunique()

    def create_object_handles(self):

        handles = {}
        df = self.df.merge(self.footer, on='Subject ID')

        for i, row in self.df.iterrows():
            subject_id = str(int(row['Subject Index'])).zfill(4)
            protection = row['isProtected']
            product_id = row['Site Label'].split('_')[0]
            replicate = row['replicate']

            data_df = row[self.data_cols].to_frame()
            this_handle = subject_id + protection + product_id + '_' + replicate
            handles[this_handle] = df

            try:
                assert len(handles) == i + 1
            except:
                logger.error('Data integrity issue on line {} of main data').format(i)
                return

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
        pass

    def export(self):

        with TemporaryDirectory as temp:
            for k, v in self.handles:
                v.to_csv(os.path.join(temp, k), sep='\t', index=False, header=False)

