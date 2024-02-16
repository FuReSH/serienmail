#!/usr/bin/python
# coding:utf8

# a small script that reads a csv file and uses the columns Name, Adress and File to send a message to each Adress, using the Name for Hello Name in the message, and attach the file from the File column. the message is sent with mutt. this is pretty much idiosyncratic for my own system. in oder to use, variables would have to be defined externally through a config file.
import argparse
import os
import pandas as pd
import pathlib as p
import shlex
import subprocess
import sys
import yaml
# pseudocode

# define command line arguments (working directory and csv table)
parser = argparse.ArgumentParser()

parser.add_argument('-c', '--config',
                    help = 'Path to config file, has to be a yaml file as defined in config.example.yml. Defaults to config.yml in the current working directory.')

parser.add_argument('-i', '--init',
                    action = 'store_true',
                    help = 'Initialize the workspace: Checks if a configuration file namend config.yml is present. Writes default configuration file if not.')
args = parser.parse_args()

# define variables
    # base path can be provided on command line, otherwise it's set to the current working directory.

# define base variables
basedir = p.Path().absolute()

# process arguments from command line
if args.init == True:
    if (basedir / 'config.yml').is_file():
        print('Configuration file is present. To send mails, please run the program without the init flag.')
        sys.exit()
    elif (basedir / 'config.yml').is_dir():
        print('It seems that config.yml is a directory. Please rename this directory to initialize a configuration file or set the config file by using the -c flag.')
        sys.exit()
    else:
        with open(basedir / 'config.yml', 'w') as f:
            f.write('workshop_title: \n')
            f.write('signature:              # Signature for message body (should be a name;)\n')
            f.write('mutt_account:         # path to mutt account that will be used for sending the mails\n')
            f.write('csv_file:             # filename of csv table (default: teilnehmende.csv)\n')
            f.write('filedir:              # path to pdf folder (default: teilnahmebestätigungen)')
        print('Configuration file has been written. Please open config.yml and fill in the missing values, then run the program again without the --init flag.')
        sys.exit()

if args.config:
    config_file = p.Path(args.config)
else:
    config_file = basedir / 'config.yml'

# load configuration from file
with open(config_file, 'r') as f:
    config = yaml.safe_load(f)

# set variables
basedir = p.Path().absolute()
csv_file = basedir / config['csv_file']
filedir = basedir / config['filedir']
workshop_title = config['workshop_title']
mutt_account = config['mutt_account']
signature = config['signature']
print(basedir)
print(filedir)

# templates 
message_subject = f'Workshop {workshop_title} -- Ihre Teilnahmebestätigung'

# main function: 
# read csv into dataframe
df = pd.read_csv(csv_file)
# iterate over dataframe, check every row and if checks go through send mail
# for each line
for index, row in df.iterrows():
    # check if we have a file
    if not p.Path(filedir / row['TN-Bestätigung']).is_file():
        print(f'Fehler bei {row["Name"]}, Datei {row["TN-Bestätigung"]} nicht gefunden.')
        continue
    else:
        tn_name = row['Name']
        tn_file = filedir / row['TN-Bestätigung']
        tn_address = row['Adresse']
        # write message body to file
        with open('message.txt', 'w') as f:
            f.write(f'Sehr geehrte*r {tn_name},\n\nanbei finden Sie Ihre Teilnahmebestätigung für den Workshop {workshop_title}.\n\nMit freundlichem Gruß\n{signature} \n\n\nDiese Mail wurde automatisch erstellt. Auf Rückfragen antworten wir wieder persönlich.')
        # mutt command
        mutt_command = f'mutt -e "source {mutt_account}" -s "{message_subject}" -a {tn_file} -- {tn_address} < message.txt'
#        print(mutt_command)
#        print(shlex.split(mutt_command, posix=True))
#        subprocess.run(shlex.split(mutt_command), capture_output=True)
        os.system(mutt_command)
        #subprocess.run(['mutt', '-e', 'source /home/cms/.mutt/account.hub', '-s', f'{message_subject}', '-a', f'{tn_file}', '--', f'{tn_address}', '<', 'message.txt'])
        print(f'Mail to {tn_name} has been sent.')
print('Done.')

# ['mutt', '-e', 'source /home/cms/.mutt/account.hub', '-s', 'Workshop Automatische Texterkennung mit OCR4all -- Ihre Teilnahmebestätigung', '-a', '/home/cms/python/programme/serienmail/teilnahmebestätigungen/schlesinger2.pdf', '--', 'cms@dock.in-berlin.de', '<', 'message.txt']

# working command:
# mutt -e "source ~/.mutt/account.hub" -s "test" -f ~/.mutt/hub -a ~/tmp/test.txt -- claus-michael.schlesinger@hu-berlin.de < message.txt
