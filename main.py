# -*- coding: utf-8 -*-

from logging import config as logger_config
from core_config import settings
import logging
from tasks.report_computer_cost import ComputerCostReporting

logger_config.dictConfig(settings.LOGGER_CONF)
logger = logging.getLogger(__name__)

etl = ComputerCostReporting(nb_filepath='./data/NB.csv',
                            pc_filepath='./data/PC.csv',
                            output_folder='./')
etl.execute()
