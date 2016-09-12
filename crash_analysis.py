#!/usr/bin/env python
#author Max

#usage:python crash_analysis.py crash_path dsym_path

import os, re, shutil

crash_core_list = {}
dsym_core_list = {}
pair_list = {}
uuid_lists = {}
dsym_uuid = {}
symbolicatecrash_path = ''

def downLoadSymbolicatecrash():
    search_symbolicatecrash = os.popen('find . -maxdepth 1 -name symbolicatecrash').readlines()
    if len(search_symbolicatecrash) > 0:
        symbolicatecrash_path = search_symbolicatecrash[0].strip('\n')
    else:
        print '------------------------------------'
        print 'search symbolicatecrash ing...\n'
        search_symbolicatecrash = os.popen('find /Applications/Xcode.app -name ''symbolicatecrash').readlines()
        if len(search_symbolicatecrash) > 0:
            symbolicatecrash_path = search_symbolicatecrash[0]
            shutil.copy2(symbolicatecrash_path.strip('\n'), './')

def analysis(dsym_path, crash_path, output_path= './'):
    print output_path
    uuid_lists = os.popen('grep --after-context=2 "Binary Images:" ' + crash_path).readlines()
    dsym_uuid = os.popen('dwarfdump --uuid ' + dsym_path)
    pair_list = {}
    for v in dsym_uuid:
        result = str.split(v)
        core = result[2][1:-1]
        uuid = result[1].replace('-', '')
        crash_core_list[core] = uuid
    for v in uuid_lists:
        pattern = re.compile(r'<.*>')
        match = re.search(pattern, v)
        if match:
            result = str.split(v)
            core = result[4]
            uuid = str.upper(result[5])[1:-1]
            dsym_core_list[core] = uuid
#
    for k in crash_core_list:
        for kk in dsym_core_list:
            if k == kk:
                pair_list[k] = dsym_core_list[k]

    os.putenv('DEVELOPER_DIR', '/Applications/Xcode.app/Contents/Developer')
    result_path = dsym_path.split('.')[0].split('/')[-1] + '_' + crash_path.split('.')[0].split('/')[-1] + '.crash'
    os.popen('./symbolicatecrash ' + crash_path + ' ' + dsym_path + '>' + output_path + '/' + result_path)
    return (result_path, pair_list)


