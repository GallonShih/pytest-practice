# -*- coding: utf-8 -*-

import pytest
import pandas as pd
from tasks.report_computer_cost import ComputerCostReporting

etl = ComputerCostReporting(nb_filepath='NB.csv', pc_filepath='PC.csv', output_folder='./')

@pytest.fixture(scope="module")
def nb_data():
    nb_data = pd.DataFrame({
        'Product Type': ['NB', 'NB', 'NB', 'NB', 'NB'],
        'ISN': ['NB1', 'NB2', 'NB3', 'NB4', 'NB5'],
        'Defective': [False, False, True, True, True],
        'CPU Cost': [2, 4, 6, 8, 10],
        'Network Card Cost': [4, 6, 8, 10, 12],
        'Battery Cost': [6, 8, 10, 12, 14],
        'Total Cost': [8, 10, 12, 14, 16]
    })
    return nb_data

@pytest.fixture(scope="module")
def pc_data():
    pc_data = pd.DataFrame({
        'Product Type': ['PC', 'PC', 'PC', 'PC', 'PC'],
        'ISN': ['PC1', 'PC2', 'PC3', 'PC4', 'PC5'],
        'Defective': [False, False, True, True, True],
        'CPU Cost': [8, 10, 12, 14, 16],
        'Network Card Cost': [6, 8, 10, 12, 14],
        'Total Cost': [4, 6, 8, 10, 12]
    })
    return pc_data

def test_find_isn_with_maxtc(nb_data, pc_data):
    df_isn_with_maxtc = pd.DataFrame({
        'Product Type': ['NB', 'PC'],
        'ISN': ['NB5', 'PC5'],
        'Total Cost': [16, 12]
    })
    pd.testing.assert_frame_equal(etl._find_isn_with_maxtc(df_nb=nb_data, df_pc=pc_data), df_isn_with_maxtc)

def test_total_cost_desc(nb_data, pc_data):
    df_cost_desc = pd.DataFrame({
        'Product Type': ['NB', 'PC'],
        'total_cost_max': [16, 12],
        'total_cost_min': [12, 8],
        'total_cost_avg': [14., 10.]
    })
    pd.testing.assert_frame_equal(etl._total_cost_desc(df_nb=nb_data, df_pc=pc_data), df_cost_desc)

def test_battery_cost_desc(nb_data):
    df_bat_cost_desc = pd.DataFrame({
        'Product Type': ['NB'],
        'battery_cost_max': [14],
        'battery_cost_min': [10],
        'battery_cost_avg': [12.]
    })
    pd.testing.assert_frame_equal(etl._battery_cost_desc(df_nb=nb_data), df_bat_cost_desc)

def test_execute(mocker, tmp_path, nb_data, pc_data):
    d = tmp_path / "sub"
    d.mkdir()
    etl = ComputerCostReporting(nb_filepath='NB.csv', pc_filepath='PC.csv', output_folder=d)
    mocker.patch("tasks.report_computer_cost.ComputerCostReporting._load_data", return_value=(nb_data, pc_data))
    etl.execute()
    assert len(list(d.iterdir())) == 1
