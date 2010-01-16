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
            'uncategory':Status.count_all(category = 'uncategory')
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
    
def get_states_with_emotion(states):
    new_states = states[:]
    for status in new_states:
        status['emotion'] = Status.check_emotion(status['message'])
    return new_states

def get_chart(states_with_emotion,size='600x400'):
    chart_data = states_with_emotion[:]
    chart_data.reverse()
    
    emo_values =   {'marah':10,'bersalah':20, 'jijik':30, 'sedih':40,
                    'takut':50, 'malu':60, 'senang':70,'uncategory':0}
    
    data = '0,'
    label = '0|'
    i = 0
    for c in chart_data:
        label += '%d|' % (i + 1)
        data += '%d,' % (emo_values[c['emotion']])
        i += 1
    
    
    label = label.strip('|')
    data = data.strip(',')
    x_size = float(100)/float(len(chart_data))
    
    
    chart = 'http://chart.apis.google.com/chart?'\
            'cht=lc'\
            '&chd=t:%s'\
            '&chs=%s'\
            '&chxt=x,y'\
            '&chxl='\
            '0:|%s|'\
            '1:|uncategory|marah|bersalah|jijik|sedih|takut|malu|senang|||'\
            '&chg=%f,10' % (data,size,label,x_size)
    return chart

def trainning_smiley():
    last_key = memcache.get('last_key_trainning_smiley')
    count = memcache.get('count_trainning_smiley')
    
    if last_key is None:
        last_status = Status.all().order('__key__').get()
        Keyword.update_custome(last_status)
        memcache.set('last_key_trainning_smiley',last_status.key())
        memcache.set('count_trainning_smiley',1)
        last_key = last_status.key()
        count = 1
    
    print 'Count First : %d' % count
    
    query = Status.all()
    query.filter('__key__ > ',last_key)
    query.order('__key__')
    
    for status in query.fetch(1000):
        if status.category != 'uncategory':
            Keyword.update_custome(status)
            count += 1
            memcache.set('last_key_trainning_smiley',status.key())
            memcache.set('count_trainning_smiley',count)
    
    print 'Count Last : %d' % count
    


def trainning_word():
    last_key = memcache.get('last_key_trainning_word')
    count = memcache.get('count_trainning_word')
    
    if last_key is None:
        last_status = Status.all().order('__key__').get()
        Keyword.update(last_status)
        memcache.set('last_key_trainning_word',last_status.key())
        memcache.set('count_trainning_word',1)
        
        last_key = last_status.key()
        count = 1
        
        
    print 'Count First : %d' % count
    
    query = Status.all()
    query.filter('__key__ > ',last_key)
    query.order('__key__')
    
    for status in query.fetch(1000):
        if status.category != 'uncategory':
            Keyword.update(status)
            count += 1
            memcache.set('last_key_trainning_word',status.key())
            memcache.set('count_trainning_word',count)
    
    print 'Count Last : %d' % count


def get_fbfriends_cache(fbapi, count = 30):
    friends = memcache.get('guest_friends_%d' % int(fbapi.uid))
    if friends is not None:
        return friends
    else:
        fql =   'SELECT uid,name,pic_square FROM user WHERE  uid IN '\
                '(SELECT uid2 FROM friend WHERE uid1 = %d) '\
                'order by name limit 0,%d' % (int(fbapi.uid), count)
        friends = friends = fbapi.fql.query(fql)
        memcache.set('guest_friends_%d' % int(fbapi.uid),friends,3600)
        return friends

def get_fbstates_cache(fbapi,uid, count = 20):
    states = memcache.get('guest_states_%d' % uid)
    if states is not None:
        return states
    else:
        states = get_states_with_emotion(fbapi.status.get(uid,count))
        memcache.set('guest_states_%d' % uid,states,3600)
        return states
