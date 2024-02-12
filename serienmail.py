#!/usr/bin/python
# coding:utf8

# a small script that reads a csv file and uses the columns Name, Adress and File to send a message to each Adress, using the Name for Hello Name in the message, and attach the file from the File column. the message is sent with mutt. this is pretty much idiosyncratic for my own system. in oder to use, variables would have to be defined externally through a config file.

import os
import subprocess
import argparse
import pathlib as p

# pseudocode

# define command line arguments (working directory and csv table)
parser = argparse.ArgumentParser()

parser.add_argument('-c', '--config',
                    help = 'Path to config file, has to be a yaml file as defined in config.example.yml. Defaults to config.yml in the current working directory.')

args = parser.parse_args()

# define variables
    # base path can be provided on command line, otherwise it's set to the current working directory.

if args.config:
    config_file = p.Path(args.config)
else:
    basedir = p.Path(os.getcwd())
    config_file = basedir / 'config.yml'

# load configuration from file
with open(config_file, 'r') as f:
    config = yaml.safe_load(f)

# set variables
basedir = config['basedir']
csv_file = config['csv_file']
filedir = config['filedir']
workshop_title = config['workshop_title']
mutt_account = config['mutt_account']
signature = config['signature']

# templates 
mutt_command = f'mutt -e "source {mutt_account}" -s "{message_subject}" -a {tn_file} -- {tn_address} < {message_body_file}'
message_subject = f'Workshop {workshop_title} -- Ihre Teilnahmebestätigung'
message_body = f'Sehr geehrte*r {tn_name}, \n\nanbei finden Sie Ihre Teilnahmebestätigung für den Workshop {workshop_title}.\n\nMit freundlichem Gruß\n{signature}'

# main function: 
# read csv into dataframe
df = pd.read_csv(csv_file)



# for each line
for index, row in df.iterrows():
    # check if we have a file matching the filename
    
# if not, throw error message, abort
        # if yes, keep going
    # construct message body from template and save to tmp file message.txt
    # send mail (mutt subprocess)
