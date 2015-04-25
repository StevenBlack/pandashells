#! /usr/bin/env python


# standard library imports
import os
import sys
import argparse
import textwrap
import re

from pandashells.lib import module_checker_lib, arg_lib, io_lib

# import required dependencies
module_checker_lib.check_for_modules(['pandas', 'numpy'])

import pandas as pd
import numpy as np

## this dict holds info on all valid distribution types
#TYPE_LIST = [{
#    'name': 'uniform',
#    'param_list': [
#        {'name': 'low', 'val': 0},
#        {'name': 'high', 'val': 1}, ]},
#    {
#    'name': 'normal',
#    'param_list': [
#        {'name': 'loc', 'val': 0},
#        {'name': 'scale', 'val': 1}]},
#    {
#    'name': 'binomial',
#    'param_list': [
#        {'name': 'n', 'val': 1},
#        {'name': 'p', 'val': .5}]},
#    {
#    'name': 'beta',
#    'param_list': [
#        {'name': 'a', 'val': 1},
#        {'name': 'b', 'val': 1},
#    ],
#    },
#    {
#    'name': 'gamma',
#    'param_list': [
#        {'name': 'shape', 'val': 1},
#        {'name': 'scale', 'val': 1},
#    ],
#    },
#    {
#    'name': 'poisson',
#    'param_list': [{'name': 'lam', 'val': 1}],
#    },
#    {
#    'name': 'standard_t',
#    'param_list': [{'name': 'df', 'val': 1}],
#    }]


def fill_default_mu(args):
    if args.type[0] == 'normal':
        args.mu = [0.] if args.mu is None else args.mu
    elif args.type[0] == 'poisson':
        args.mu = [1.] if args.mu is None else args.mu
    return args



def get_samples(args):
    distribution_for = {
        'uniform': {
            'function': np.random.uniform,
            'kwargs': {
                'low': args.min[0],
                'high': args.max[0],
                'size': (args.num_samples[0], args.columns[0]),
            },
        },
        'normal': {
            'function': np.random.normal,
            'kwargs': {
                'loc': args.mu[0] if args.mu else None,
                'scale': args.sigma[0],
                'size': (args.num_samples[0], args.columns[0]),
            },
        },
        'poisson': {
            'function': np.random.poisson,
            'kwargs': {
                'lam': args.mu[0] if args.mu else None,
                'size': (args.num_samples[0], args.columns[0]),
            },
        },
        'beta': {
            'function': np.random.beta,
            'kwargs': {
                'a': args.alpha[0],
                'b': args.beta[0],
                'size': (args.num_samples[0], args.columns[0]),
            },
        },
        'gamma': {
            'function': np.random.gamma,
            'kwargs': {
                'shape': args.alpha[0],
                'scale': 1. / args.beta[0],
                'size': (args.num_samples[0], args.columns[0]),
            },
        },

    }

    dist = distribution_for[args.type[0]]
    values = dist['function'](**dist['kwargs'])
    columns = ['c{}'.format(c) for c in range(args.columns[0])]
    return pd.DataFrame(values, columns=columns)


def main():
    #TODO: write docs for this
    msg = textwrap.dedent(
    """
        Return random samples from common probability distrubtions.

        Examples:
            uniform:  p.rand -n 1000 -t uniform  --min=0    --max=1   | p.hist
            normal:   p.rand -n 1000 -t normal   --mu=0     --sigma=1 | p.hist
            poisson:  p.rand -n 1000 -t poisson  --mu=1               | p.hist
            beta:     p.rand -n 1000 -t beta     --alpha=2  --beta=6  | p.hist
            gamma:    p.rand -n 1000 -t gamma    --alpha=1  --beta=1  | p.hist
            binomial: p.rand -n 1000 -t binomial --N=10     --p=0.4   | p.hist
    """)

    # read command line arguments
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter, description=msg)

    #options = {}
    parser.add_argument(
        '-t', '--type', nargs=1, type=str, default=['uniform'],
        choices=['uniform', 'normal', 'beta', 'gamma', 'binomial', 'poisson'],
        help='type of distribution (default=\'uniform\')')
    parser.add_argument(
        '-n', '--num_samples', nargs=1, default=[10], type=int,
        help='The number of rows to generate (default=10)')
    parser.add_argument(
        '-c', '--columns', nargs=1, default=[1], type=int,
        help='The number of columns to generate per row (default=1)')
    parser.add_argument(
        '--N', nargs=1, default=[10], type=int,
        help=(
            '(Binomial Dist) Largest possible value for random variable. '
            '(default=10)'
        )
    )
    parser.add_argument(
        '--mu', nargs=1, type=float,
        help='(Normal, Poisson) Mean (defaults: normal:0, poisson:1')
    parser.add_argument(
        '--sigma', nargs=1, default=[1.], type=float,
        help='(Normal) standard deviation, (default: 1)')
    parser.add_argument(
        '--min', nargs=1, default=[0.], type=float,
        help='(Uniform) Minimum value of range, (default: 0)')
    parser.add_argument(
        '--max', nargs=1, default=[1.], type=float,
        help='(Uniform) Maximum value of range, (default: 1)')
    parser.add_argument(
        '--alpha', nargs=1, default=[2.], type=float,
        help='(Beta, Gamma)  (default: 2)')
    parser.add_argument(
        '--beta', nargs=1, default=[2.], type=float,
        help='(Beta, Gamma)  (default: 2)')


    arg_lib.add_args(parser, 'io_out', 'example')

    # parse arguments
    args = parser.parse_args()

    # set some defaults
    args = fill_default_mu(args)

    # get the samples
    df = get_samples(args)

    # write dataframe to output
    io_lib.df_to_output(args, df)

if __name__ == '__main__':  # pragma: no cover
    main()

