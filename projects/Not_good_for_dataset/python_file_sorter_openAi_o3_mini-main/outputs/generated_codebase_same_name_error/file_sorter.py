import os
import shutil
import time
import datetime


def sort_file(file_path, config):
    '''
    Moves the file based on sorting rules and returns a tuple (destinationFolder, ruleApplied)
    ruleApplied is a string identifying the sorting rule used.
    '''
    try:
        sorting_rules = config.get('sorting_rules', {})
        destination = None
        rule_applied = None
        
        # Determine destination based on file type
        if sorting_rules.get('by_file_type', False):
            file_ext = os.path.splitext(file_path)[1].lstrip('.').lower()
            parent_dir = os.path.dirname(file_path)
            dest_dir = os.path.join(parent_dir, file_ext + '_files')
            os.makedirs(dest_dir, exist_ok=True)
            destination = os.path.join(dest_dir, os.path.basename(file_path))
            rule_applied = 'by_file_type'
            shutil.move(file_path, destination)
            print(f"Moved {file_path} to {destination} based on file type.")
            return destination, rule_applied
        
        # Alternatively, sort by creation date
        if sorting_rules.get('by_creation_date', False):
            creation_time = os.path.getctime(file_path)
            date_str = datetime.datetime.fromtimestamp(creation_time).strftime('%Y_%m_%d')
            parent_dir = os.path.dirname(file_path)
            dest_dir = os.path.join(parent_dir, date_str)
            os.makedirs(dest_dir, exist_ok=True)
            destination = os.path.join(dest_dir, os.path.basename(file_path))
            rule_applied = 'by_creation_date'
            shutil.move(file_path, destination)
            print(f"Moved {file_path} to {destination} based on creation date.")
            return destination, rule_applied
        
        # If no rule applied, do nothing
        return None, None
    except Exception as e:
        print(f"Error sorting file {file_path}: {e}")
        return None, None
