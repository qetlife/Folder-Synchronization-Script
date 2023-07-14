# Veeam-Software

This is my take on the Synchronization Test for Veeam-Software.

The software is simple, using 5 internal libraries: os, shutil, logging, threading, argparse. 
Also the program uses 1 external library: schedule. (pip install schedule) is required if the library isn't already installed.

The software can be launched either in an IDE or on the command line. You can add 4 arguments:
  - Path to the source folder
  - Path to the replica folder
  - Path to the output log file
  - Synchronization interval in seconds

Here are some examples:
No arguments (this way the default arguments are used)

<img width="362" alt="image" src="https://github.com/qetlife/Veeam-Software/assets/120670346/a28cf3db-f66e-46a8-a5c4-115050194d82">




With arguments:

<img width="567" alt="image" src="https://github.com/qetlife/Veeam-Software/assets/120670346/a7a7227f-c1da-41c8-b82b-2e47e74ba7f4">


After the program starts, the message "Started Synchronization." appears.
The user can use "?" or "help" to acess the command list:

<img width="354" alt="image" src="https://github.com/qetlife/Veeam-Software/assets/120670346/c80d989d-50d7-46e5-996a-7060f01d0d68">


The algorithm runs on a Thread, and uses the schedule to periodically synchronize the folders. The schedule library adds a sleep method that doesn't consume CPU when sleeping.
