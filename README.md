This is a small script to automate sending emails to workshop participants with attachments (confirmation of participation).

Disclaimer: This small program is not very versatile, it expects `mutt` to be configured for sending out mails. It has only been tested with a mutt configuration that makes it possible to send mail without any manual interaction, e.g. entering a password. 

## Installation

The script expects `mutt` for sending out emails, plus several Python packages. In order to install, clone the repository, install the Python packages, make sure to put the `serienmail` script into a folder that is in your PATH, and make it executable. 

## Usage

Run `serienmail --init` to write a plain configuration file in the working directory. Then define the variables given in the config file (see defaults in the config file comments). Write all participant information into a csv file with the columns: Name, Email, TN-Bestätigung (this is the filename). Then run the program again without the --init flag => Mails should be sent through the given mutt account. 
