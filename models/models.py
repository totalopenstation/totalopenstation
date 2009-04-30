#! /usr/bin/env python
# -*- coding: utf-8 -*-
# filename: models.py
# Copyright 2008 Luca Bianconi <luxetluc@yahoo.it>
# Copyright 2008 Stefano Costa <steko@iosa.it>
# Under the GNU GPL 3 License

models = {
    'Leica TCR 1205' : 'leica_tcr_1205',
    'Zeiss Elta R55' : 'zeiss_elta_r55',
    'Nikon Npl 350' : 'nikon_npl_350',
    'Trimble .are' : 'trimble',
    'Custom' : 'generic'
    }

def list_models():
    mod_string = ''
    mod_string = mod_string + "List of supported models:\n------------------------\n"
    for k,v in models.items():
        mod_string = mod_string + k.ljust(20) + v + "\n"
    mod_string = mod_string + "\n"
    return mod_string

if __name__ == '__main__':
    print list_models()
