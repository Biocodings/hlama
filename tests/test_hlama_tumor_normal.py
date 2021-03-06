#!/usr/bin/env python3
"""Test for hlama tumor/normal app"""

import os.path
import pytest
from hlama import app

__author__ = 'Clemens Messerschmidt <clemens.messerschmidt@bihealth.de>'


@pytest.fixture
def report():
    """Report path"""
    return os.path.join(os.path.dirname(__file__),
                        'data/tumor_normal/report.txt')


@pytest.fixture
def tsv_file():
    """Path of tsv that describes donors and samples"""
    return os.path.join(os.path.dirname(__file__),
                        'data/tumor_normal/donors.tsv')


@pytest.fixture
def data_dir():
    """Path of sequencing data, i.e. fastq files"""
    return os.path.join(os.path.dirname(__file__),
                        'data/tumor_normal')


def test_app(tmpdir, report, tsv_file, data_dir):
    work_dir = str(tmpdir.mkdir('hlama_tumor_normal'))
    args = ['--tumor-normal', tsv_file, '--reads-base-dir', data_dir,
            '--work-dir', work_dir]
    app.main(args)

    with open(os.path.join(os.path.dirname(__file__), work_dir,
                           'report.txt')) as f:
        result = f.read().splitlines()
    with open(report, 'r') as f:
        solution = f.read().splitlines()

    assert set(result) == set(solution)

    with open(os.path.join(work_dir, 'donor1_normal.d/hla_types.txt')) as f:
        result = f.read().splitlines()
        assert result == ['A*02:01', 'A*02:74', 'B*15:01', 'B*53:01',
                          'C*04:01', 'C*07:02']

    with open(os.path.join(work_dir, 'donor1_tumor.d/hla_types.txt')) as f:
        result = f.read().splitlines()
        assert result == ['A*02:01', 'A*02:74', 'B*15:01', 'B*53:01',
                          'C*04:01', 'C*07:02']

    with open(os.path.join(work_dir,
                           'donor1_tumor_rna.d/hla_types.txt')) as f:
        result = f.read().splitlines()
        assert result == ['A*02:01', 'A*02:01', 'B*15:01', 'B*53:01',
                          'C*04:01', 'C*07:02']

    with open(os.path.join(work_dir, 'donor2_normal.d/hla_types.txt')) as f:
        result = f.read().splitlines()
        assert result == ['A*01:01', 'A*24:02', 'B*27:04', 'B*27:05',
                          'C*02:02', 'C*18:01']

    with open(os.path.join(work_dir, 'donor2_tumor.d/hla_types.txt')) as f:
        result = f.read().splitlines()
        assert result == ['A*01:01', 'A*24:02', 'B*27:04', 'B*27:05',
                          'C*02:02', 'C*18:01']
