# -*- coding: utf-8 -*-

import pandas as pd
import os
from logging import config as logger_config
from core_config import settings
import logging

logger_config.dictConfig(settings.LOGGER_CONF)
logger = logging.getLogger(__name__)

class ComputerCostReporting:
    def __init__(self, nb_filepath: str, pc_filepath: str, output_folder: str):
        """
        :param nb_filepath: csv file path of nb
        :param pc_filepath: csv file path of pc
        :param output_folder: the folder you want to save the report
        """
        self.nb_filepath = nb_filepath
        self.pc_filepath = pc_filepath
        self.output_folder = output_folder

    def _load_data(self):
        """
        :return df_nb: dataframe, the nb's cost data
        :return df_pc: dataframe, the pc's cost data
        """
        logger.info('Start loading all data.')
        df_nb = pd.read_csv(self.nb_filepath)
        logger.info(f'Finish loading nb data: {df_nb.shape}.')
        df_pc = pd.read_csv(self.pc_filepath)
        logger.info(f'Finish loading pc data: {df_pc.shape}.')
        df_nb.columns = [c.strip() for c in df_nb.columns]
        df_pc.columns = [c.strip() for c in df_pc.columns]
        logger.info('Finish loading all data.')
        return df_nb, df_pc

    def _find_isn_with_maxtc(self, df_nb, df_pc):
        """
        :param df_nb: dataframe, the nb's cost data
        :param df_pc: dataframe, the pc's cost data
        :return df_isn_with_maxtc: dataframe, the ISNs of both nb and pc with max total cost
        """
        logger.info('Start finding ISN with max total cost.')
        df_isn_with_maxtc = pd.DataFrame()
        df_nb_maxtc = df_nb.loc[[df_nb.query('Defective == True')['Total Cost'].idxmax()], ['Product Type', 'ISN', 'Total Cost']]
        logger.info(f"Finish finding ISN in nb. INS: {df_nb_maxtc['ISN'].values[0]}. Total Cost: {df_nb_maxtc['Total Cost'].values[0]}")
        df_isn_with_maxtc = pd.concat([df_isn_with_maxtc, df_nb_maxtc]).reset_index(drop=True)
        df_pc_maxtc = df_pc.loc[[df_pc.query('Defective == True')['Total Cost'].idxmax()], ['Product Type', 'ISN', 'Total Cost']]
        logger.info(f"Finish finding ISN in pc. INS: {df_pc_maxtc['ISN'].values[0]}. Total Cost: {df_pc_maxtc['Total Cost'].values[0]}")
        df_isn_with_maxtc = pd.concat([df_isn_with_maxtc, df_pc_maxtc]).reset_index(drop=True)
        logger.info('Finish finding ISN with max total cost.')
        return df_isn_with_maxtc

    def _total_cost_desc(self, df_nb, df_pc):
        """
        :param df_nb: dataframe, the nb's cost data
        :param df_pc: dataframe, the pc's cost data
        :df_cost_desc df_isn_with_maxtc: dataframe, total cost description of both nb and pc
        """
        logger.info('Start getting total cost description.')
        df_nb_sub = df_nb.query('Defective == True')
        df_pc_sub = df_pc.query('Defective == True')
        df_cost_desc = pd.DataFrame({
            'Product Type': ['NB', 'PC'],
            'total_cost_max': [df_nb_sub['Total Cost'].max(), df_pc_sub['Total Cost'].max()],
            'total_cost_min': [df_nb_sub['Total Cost'].min(), df_pc_sub['Total Cost'].min()],
            'total_cost_avg': [round(df_nb_sub['Total Cost'].mean(), 2), round(df_pc_sub['Total Cost'].mean(), 2)]
        })
        logger.info('Finish getting total cost description.')
        return df_cost_desc

    def _battery_cost_desc(self, df_nb):
        logger.info('Start getting battery cost description.')
        df_nb_sub = df_nb.query('Defective == True')
        df_bat_cost_desc = pd.DataFrame({
            'Product Type': ['NB'],
            'battery_cost_max': [df_nb_sub['Battery Cost'].max()],
            'battery_cost_min': [df_nb_sub['Battery Cost'].min()],
            'battery_cost_avg': [round(df_nb_sub['Battery Cost'].mean(), 2)]
        })
        logger.info('Finish getting battery cost description.')
        return df_bat_cost_desc

    def _save_in_local(self, df_isn_with_maxtc, df_cost_desc, df_bat_cost_desc):
        logger.info('Start saving into result.xlsx.')
        output_filepath = os.path.join(self.output_folder, 'result.xlsx')
        logger.info(f'File path is: {output_filepath}')
        with pd.ExcelWriter(output_filepath) as writer:
            df_isn_with_maxtc.to_excel(writer, sheet_name='result 1', index=0)
            df_cost_desc.to_excel(writer, sheet_name='result 2', index=0)
            df_bat_cost_desc.to_excel(writer, sheet_name='result 3', index=0)
        logger.info('Finish saving into result.xlsx.')

    def execute(self):
        df_nb, df_pc = self._load_data()
        df_isn_with_maxtc = self._find_isn_with_maxtc(df_nb=df_nb, df_pc=df_pc)
        df_cost_desc = self._total_cost_desc(df_nb=df_nb, df_pc=df_pc)
        df_bat_cost_desc = self._battery_cost_desc(df_nb=df_nb)
        self._save_in_local(df_isn_with_maxtc=df_isn_with_maxtc,
                        df_cost_desc=df_cost_desc,
                        df_bat_cost_desc=df_bat_cost_desc)

if __name__ == '__main__':
    BASIC_FORMAT = "%(asctime)s-%(levelname)s-%(message)s"
    chlr = logging.StreamHandler()
    chlr.setFormatter(logging.Formatter(BASIC_FORMAT))
    logger.setLevel('DEBUG')
    logger.addHandler(chlr)

    # ComputerCostReporting
    op = ComputerCostReporting(nb_filepath='./data/NB.csv',
                                pc_filepath='./data/PC.csv',
                                output_folder='./')
    op.execute()
