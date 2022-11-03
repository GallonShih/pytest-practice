from tasks.report_computer_cost import ComputerCostReporting

etl = ComputerCostReporting(nb_filepath='./data/NB.csv',
                            pc_filepath='./data/PC.csv',
                            output_folder='./')
etl.execute()
