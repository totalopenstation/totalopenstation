#! /usr/bin/env python
# -*- coding: utf-8 -*-
# filename: models.py
# Copyright 2008 Luca Bianconi <luxetluc@yahoo.it>
# Copyright 2008 Stefano Costa <steko@iosa.it>
# Under the GNU GPL 3 License

models = {
    'Leica TCR 1205' : 'leica_tcr_1205',
    'Zeiss Elta R55' : 'zeiss_elta_r55',
    'Custom' : 'generic'
    }

if __name__ == '__main__':
    print("List of supported models:\n------------------------")
    for k in models.keys():
        print k
    print("")

