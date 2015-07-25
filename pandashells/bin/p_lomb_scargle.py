#! /usr/bin/env python

# standard library imports
import argparse

from pandashells.lib import arg_lib, io_lib, outlier_lib, lomb_scargle_lib


def main():
    msg = 'Need to write this'

    # read command line arguments
    parser = argparse.ArgumentParser(description=msg)

    arg_lib.add_args(parser, 'io_in', 'io_out')

    parser.add_argument('-t', '--time_col', help='Time Column',
                        nargs=1, required=True, type=str)

    parser.add_argument('-y', '--observation_col', help='Observation column',
                        nargs=1, dest='val_col', required=True, type=str)

    parser.add_argument('--interp_exp', help='Interpolate by this power of 2',
                        nargs=1, type=int, default=[1])
    parser.add_argument(
        '--freq_order', action='store_true', dest='freq_order', default=False,
        help='Order output by freqency instead of period')

    # parse arguments
    args = parser.parse_args()

    # get the input dataframe
    df = io_lib.df_from_input(args)
    df = lomb_scargle_lib.lomb_scargle(
        df, args.time_col[0], args.val_col[0], args.interp_exp[0],
        not args.freq_order)

    # write dataframe to output
    io_lib.df_to_output(args, df)

if __name__ == '__main__':  # pragma: no cover
    main()
