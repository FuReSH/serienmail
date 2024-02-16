This is a small script to automate sending emails to workshop participants with attachments (confirmation of participation).

## Installation

The script expects `mutt` for sending out emails, plus several Python packages. In order to install, clone the repository, make sure to put the `serienmail` script into a folder that is in your PATH, and make it executable.

## Usage

Run `serienmail --init` to write a plain configuration file in the working directory. Then define the variables given in the config file (see defaults in the config file comments). Write all participant information into a csv file with the columns: Name, Email, TN-Bestätigung (this is the filename). Then run the program again without the --init flag => Mails should be sent through the given mutt account. 
