import os
import csv
import re
from datetime import datetime
import time

INCOMING = '/var/spool/sms/incoming'
OUTGOING = '/var/spool/sms/outgoing'
LOG_FILE = '/home/bayo/code/scripts/log.csv'
PATTERN = re.compile('^From:')

class Message(object):
    def __init__(self, sender, text):
        if sender[0] != '+' and sender[:3] == '234':
            self.sender = '+%s' % sender
        else:
            self.sender = sender
        self.text = text

class Driver(object):
    def __init__(self, *args, **kwargs):
        pass

    def next_message(self):
        '''read the files in incoming and see if there are any new ones
        then construct a message object and return it
        '''
        all_files = get_newfilenames()
        old_files = get_oldfilenames()
        new_files = diff_filenames(all_files, old_files)
        if new_files:
            #save and return only the first message
            new_file = new_files.pop()
            file_info = get_fileinfo(new_file)
            save_fileinfo([file_info])
            #make Message objects 
            msg = Message(file_info[1], file_info[2])
            return msg

    def send_sms(self, number, msg):
        'make a file with reply message and dump in outgoing...'
        file_name = '%s' % time.time()
        #check if file exists, then append '_'
        while True:
            if os.path.exists(os.path.join(OUTGOING, file_name)):
                file_name = file_name + '_'
            else:
                break
        f = open(os.path.join(OUTGOING, file_name), 'w')
        #make sure number is in international format
        if number[0] == '0':
            number = '+234%s' % number[1:]
        elif number[0] != '+' and number[:3] == '234':
            number = '+%s' % number
        f.write('To: %s \n\n' % number)
        f.write(msg)
        f.close()

    def disconnect(self):
        pass

def get_oldfilenames():
    try:
        f = open(LOG_FILE,'r')
    except:
        f = open(LOG_FILE,'w')
        filenames = []
    else:
        reader = csv.reader(f)
        filenames = [line[0] for line in reader]
    f.close()
    return filenames

def get_newfilenames():
    return os.listdir(INCOMING)

def diff_filenames(newfiles, oldfiles):
    return set(newfiles).difference(oldfiles)

def get_fileinfo(f):
    filepath = os.path.join(INCOMING, f)
    fp = open(filepath)
    lines = [line for line in fp]
    from_no = PATTERN.sub('',lines[0]).strip()
    return [f] + [from_no, lines[-1]]

def save_fileinfo(file_info):
    f = open(LOG_FILE, 'a')
    writer = csv.writer(f)
    writer.writerows(file_info)
    f.close()

def get_message(file_info):
    return 'thank you for your sms'

def send_reply(file_info):    
    #make a file with reply message and dump in outgoing...
    msg = get_message(file_info)
    print 'message: ' + msg
    file_name = file_info[0]
    f = open(os.path.join(OUTGOING, file_name), 'w')
    f.write('To: +%s \n\n' % file_info[1])
    f.write(msg)
    f.close()
    print os.listdir(OUTGOING)

def process_files():
    #get file names
    filenames = get_newfilenames()
    #check if there is any new sms file
    old_filenames = get_oldfilenames()
    new_files = diff_filenames(filenames, old_filenames)
    file_info = map(get_fileinfo, new_files)#file info is a dict of 
    save_fileinfo(file_info)#save the files
    map(send_reply, file_info)
    return file_info

#open the files, grab the messages, store in a csv

if __name__ == "__main__":
    import time
    #run every 10 seconds
    while True:
        process_files()
        time.sleep(5)
