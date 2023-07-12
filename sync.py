import os
import shutil
import logging
import schedule
import threading
import time

def sync_folders(source_folder, replica_folder):
    print("SYNC DEBUG")
    # Remove any items in the replica folder that don't exist in the source folder
    for item in os.listdir(replica_folder):
        replica_item = os.path.join(replica_folder, item)
        source_item = os.path.join(source_folder, item)

        if not os.path.exists(source_item):
            if os.path.isdir(replica_item):
                shutil.rmtree(replica_item)
                logger.info("Removing the " + item + " folder from the replica directory.")
            else:
                os.remove(replica_item)
                logger.info("Removing the " + item + " item from the replica directory.")
    
    # Iterate over files and directories in the source folder
    for item in os.listdir(source_folder):
        source_item = os.path.join(source_folder, item)
        replica_item = os.path.join(replica_folder, item)

        if os.path.isdir(source_item):
            # If the item is a directory, recursively synchronize it
            if not os.path.exists(replica_item):
                os.makedirs(replica_item)
                logger.info("Creating the folder " + item + " to the replica directory.")
            sync_folders(source_item, replica_item)
        else:
            # If the item is a file, copy it to the replica folder
            if not os.path.exists(replica_item) or os.path.getmtime(source_item) > os.path.getmtime(replica_item):
                shutil.copy2(source_item, replica_item)
                logger.info("Copying the " + item + " to the replica file")

def run():
    while flag:
        schedule.run_pending()
        time.sleep(1)

source_folder = "source"
replica_folder = "replica"
sync_interval = 1

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

logger = logging.getLogger('Sync')

file_handler = logging.FileHandler('output.log')
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
file_handler.setLevel(logging.INFO)

# Create a console handler
#console_handler = logging.StreamHandler()
#console_handler.setLevel(logging.INFO)

# Create a formatter
#formatter = logging.Formatter('%(asctime)s - %(message)s')

# Set the formatter for the handlers
#file_handler.setFormatter(formatter)
#console_handler.setFormatter(formatter)

# Add the handlers to the logger
logger.addHandler(file_handler)
#logger.addHandler(console_handler)



schedule.every(5).seconds.do(sync_folders, source_folder, replica_folder)

flag = True
scheduler_thread = threading.Thread(target=run)
scheduler_thread.start()

while scheduler_thread.is_alive():
    if input().lower() == 'q':
        flag = False
        print("Thread stopped")
        break

scheduler_thread.join()