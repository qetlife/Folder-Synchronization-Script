import os
import shutil
import logging
import schedule
import threading
import argparse

def sync_folders(source, replica):

    # Remove extra files and directories from the replica folder that aren't on the source folder
    for item in os.listdir(replica):
        replica_item = os.path.join(replica, item)
        source_item = os.path.join(source, item)

        if not os.path.exists(source_item):
            if os.path.isdir(replica_item):
                shutil.rmtree(replica_item)
                logger.info("Removing the " + item + " folder from the replica directory.")
            else:
                os.remove(replica_item)
                logger.info("Removing the " + item + " item from the replica directory.")
    
    # Iterate over all the files and directories in the source folder
    for item in os.listdir(source):
        source_item = os.path.join(source, item)
        replica_item = os.path.join(replica, item)

        if os.path.isdir(source_item):
            # If the item is a directory, call sync_folders again (recursivity)
            if not os.path.exists(replica_item):
                os.makedirs(replica_item)
                logger.info("Creating the folder " + item + " to the replica directory.")
            sync_folders(source_item, replica_item)
        else:
            # If the item is a file, copy it to the replica folder
            if not os.path.exists(replica_item) or os.path.getmtime(source_item) > os.path.getmtime(replica_item):
                shutil.copy2(source_item, replica_item)
                logger.info("Copying the " + item + " to the replica file")


# Target function for the thread
def run():
    logger.info("Started Synchronization.")
    while flag:
        schedule.run_pending()

# Default path for the arguments
source = "source"
replica = "replica"
output_log = "output.log"
sync_interval = 5

#Command line arguments
parser = argparse.ArgumentParser(description="Folder synchronization program")
parser.add_argument("source", nargs='?', default=source, help="Path to the source folder")
parser.add_argument("replica", nargs='?', default=replica, help="Path to the replica folder")
parser.add_argument("output_log", nargs='?', default=output_log, help="Path to the output log file")
parser.add_argument("sync_interval", nargs='?', type=int, default=sync_interval, help="Synchronization interval in seconds")
args = parser.parse_args()

#Assign command line arguments to variables
source = args.source
replica = args.replica
output_log = args.output_log
sync_interval = args.sync_interval

#Logging configuration for console
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

logger = logging.getLogger('Sync')

#Logging configuration for .log file
file_handler = logging.FileHandler(output_log)
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
file_handler.setLevel(logging.INFO)

logger.addHandler(file_handler)

#Setup the periodic call of the sync_folders
schedule.every(sync_interval).seconds.do(sync_folders, source, replica)

#flag to end synchronization
flag = True

#Thread start
sync_thread = threading.Thread(target=run)
sync_thread.start()

#list of commands
commands = ["exit - Stop synchronization",
            "path - Show source and replica folder paths",
            "log - Show log file path",
            "interval - Show synchronization interval",
            "? or help - Show available commands\n"]

#Provides the ability for the user to use command line commands for information
while sync_thread.is_alive():
    u_input = input().lower()
    if u_input == "exit":
        flag = False
        logger.info("Stopped Synchronization.")
        break
    elif u_input == "path":
        print("Source folder path: " + source)
        print("Replica folder path: " + replica + "\n")
    elif u_input == "log":
        print("Log file path: " + output_log + "\n")
    elif u_input == "interval":
        print("Synchronization interval: " + str(sync_interval) + " seconds.\n")
    elif u_input == "?" or u_input == "help":
        print("Available commands:")
        for command in commands:
            print(command)
    else:
        print("Command not recognized. Enter '?' or 'help' to see available commands.\n")

#Stops the thread
sync_thread.join()