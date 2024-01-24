import sys
import difflib

# Add logging?

def mis_util_diff(old_data, new_data, kidx, from_file = None, to_file = None):

    '''
    Take a difference two lists(rows) with key mappings(faster/accurate). The data in the rows must be the same format. Prints diff to std out...

    :param dict old_data_dict: Original Data to Compare

    :param dict new_data_dict: New Data to Compare

    :rtype: None

    '''

    KEY_DELIM = '_'

    # https://stackoverflow.com/questions/6612769/is-there-a-more-elegant-way-for-unpacking-keys-and-values-of-a-dictionary-into-t
    data = [] # better way to unpack?

    # if data is list of dicts make it a list
    if new_data and len(new_data) > 0:

        if type(new_data[0]) == dict:

            for row in new_data:

                data.append( list(row.values()) )

            new_data = data

    else: # error no dooters
        print('Bad new data format...[[],[],...] or [{},{},...] with at least 1 inner []/{}')
        return


    if type(kidx) != list:
        kidx = [kidx]

    new_data_dict = {}
    for row in new_data: # elements need to be the same to be diffed so handle formatting here...the diff will convert to str

        str_idx = ''
        for idx in kidx:
            str_idx += KEY_DELIM + row[idx]

        new_data_dict[str_idx] = row

    old_data_dict = {}
    for row in old_data:

        str_idx = ''
        for idx in kidx:
            str_idx += KEY_DELIM + row[idx]

        old_data_dict[str_idx] = row


    print('')
    print('Diff...')
    new_miss = []
    old_miss = []
    #cnt = 0
    for nk in new_data_dict: # inter diff /outer keys of new

        if old_data_dict.get(nk):

            old_data = [ ' ' + str(elem) + ' ' for elem in old_data_dict[nk] ]
            new_data = [ ' ' + str(elem) + ' ' for elem in new_data_dict[nk] ]
            #print(nk)
            #print(old_data)
            #print(new_data)
            sys.stdout.writelines( difflib.context_diff(old_data, new_data, fromfile=from_file, tofile=to_file) )

        else:

            new_miss = new_data_dict[nk]

        #cnt+=1
        #if cnt == 15:
        #    break

    for ok in old_data_dict: # outer keys of old

        if not new_data_dict.get(ok):

            old_miss = old_data_dict[ok]

    print('')
    print('Old Data Misses...')
    print(old_miss)
    print('')
    print('New Data Misses...')
    print(new_miss)
    print('')
