import os
import shutil
import logging
import schedule
import threading

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

# auxiliary variables for the paths.
source = "source"
replica = "replica"
output_log = "output.log"
sync_interval = 5

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
sync_thread = threading.Thread(target=run())
sync_thread.start()

#Provides the ability for the user to use command line commands for information
while sync_thread.is_alive():
    u_input = input()
    if u_input == 'q':
        flag = False
        logger.info("Stopped Synchronization.")
        break
    elif u_input == "path":
        print("Source folder path: " + source)
        print("Replica folder path: " + replica)
    elif u_input == "log":
        print("Log file path: " + output_log)
    elif u_input == "interval":
        print("Synchronization interval: " + str(sync_interval) + " seconds.")

#Stops the thread
sync_thread.join()