import os, sys
import argparse
from histogrammer.main_operator import MainOperator

def getArguments(artificialArgs=None):
    """
    Gets arguments 
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', help="Your data file name", nargs='+')
    parser.add_argument('-c', '--selection_cut', help='Selection cut to use',
                    default=None)
    parser.add_argument('-sc', '--scheme', help='Contruction scheme to use', 
                    default='belle', type=str, choices=['belle', 'none'])
    parser.add_argument('-by', '--split_by', help='Split all by a cut', 
                    default=None, type=str)
    parser.add_argument('-n', '--n_bins', help='Number of bins for all plots', 
                    default=50, type=int)   
    parser.add_argument('-t', '--table_name', help='Name of the table in the datafile', 
                    default=None, type=str)  
    parser.add_argument('-v', '--versus_dataframe', help='Load another dataframe and compare them', 
                    default=None, nargs='+')  
    args = {}
    if artificialArgs is not None:
        args = parser.parse_args([artificialArgs])
    else:
        args = parser.parse_args()

    return vars(args)

def main(args:dict) -> None:
    """
    Main function
    """
    inputPath = None

    if not 'filenames' in args or not args['filenames']:
        sys.exit('File name argument not found! Please provide a valid analysis file names!')
    for filename in args['filenames']:
        if not os.path.isfile(filename):
            sys.exit(f'File {filename} does not exist!')
    main_operator = MainOperator(args)
    main_operator.main_loop()


if __name__ == "__main__":
    args = getArguments()
    main(args)