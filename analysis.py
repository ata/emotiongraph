from models import *
from datetime import datetime

import re

def get_trainning_static():
    return {
            'total':Status.all().filter('category != ',None).count(),
            'senang':Status.all().filter('category = ','senang').count(),
            'sedih':Status.all().filter('category = ','sedih').count(),
            'marah':Status.all().filter('category = ','marah').count(),
            'malu':Status.all().filter('category = ','malu').count(),
            'bersalah':Status.all().filter('category = ','bersalah').count(),
            'jijik':Status.all().filter('category = ','jijik').count(),
            'takut':Status.all().filter('category = ','takut').count(),
            'uncategory':Status.all().filter('category = ','uncategory').count()
            }


chart = 'http://chart.apis.google.com/chart?'\
        'cht=lc&chd=t:20,10,40,30,60,50,70&'\
        'chs=500x500&'\
        'chxt=x,y&'\
        'chxl='\
        '0:|januari|febuari|maret|april|mei|juni|juli|agustus|'\
        '1:||sedih|marah|senang|malu|bersalah|jijik|takut|||'

def get_trainning_chart():
    base_url = 'http://chart.apis.google.com/chart?cht=p3'
    static = get_trainning_static()
    data = '&chd=t:%d,%d,%d,%d,%d,%d,%d&chs=500x200' % (\
            static['senang'],static['sedih'],static['marah'],\
            static['malu'],static['bersalah'],static['jijik'],\
            static['takut'])
            
    label = '&chl=senang(%d)|sedih(%d)|marah(%d)|malu(%d)|bersalah(%d)|jijik(%d)|takut(%d)'% (\
            static['senang'],static['sedih'],static['marah'],\
            static['malu'],static['bersalah'],static['jijik'],\
            static['takut'])
            
    return base_url + data + label

def get_trainning_chart_all():
    base_url = 'http://chart.apis.google.com/chart?cht=p3'
    static = get_trainning_static()
    data = '&chd=t:%d,%d,%d,%d,%d,%d,%d,%d&chs=500x200' % (\
            static['senang'],static['sedih'],static['marah'],\
            static['malu'],static['bersalah'],static['jijik'],\
            static['takut'],static['uncategory'])
            
    label = '&chl=senang|sedih|marah|malu|bersalah|jijik|takut|uncategory'
    
    label = '&chl=senang(%d)|sedih(%d)|marah(%d)|malu(%d)|bersalah(%d)|jijik(%d)|takut(%d)|uncategory(%d)'% (\
            static['senang'],static['sedih'],static['marah'],\
            static['malu'],static['bersalah'],static['jijik'],\
            static['takut'],static['uncategory'])
    
    return base_url + data + label
    
