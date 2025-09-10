import os
import shutil
import time
import datetime

import database

# This function applies the file organization rules to a given file

def apply_rules(file_path, cfg, dry_run=False):
    if not os.path.isfile(file_path):
        return
    
    file_moved = False
    applied_rule = None
    dest_path = None
    
    try:
        # Rule 1: Organize by File Type
        ext = os.path.splitext(file_path)[1].lower()
        file_type_rules = cfg.get('rules', {}).get('file_type', {})
        if ext in file_type_rules:
            dest_dir = file_type_rules[ext]
            os.makedirs(dest_dir, exist_ok=True)
            dest_path = os.path.join(dest_dir, os.path.basename(file_path))
            applied_rule = f"FileType: {ext}"
            file_moved = True
        else:
            # Rule 2: Organize by Creation Date (if enabled)
            date_rule_cfg = cfg.get('rules', {}).get('creation_date', {})
            if date_rule_cfg.get('enabled', False):
                # Use creation time; on some systems, this may be modified time
                ctime = os.path.getctime(file_path)
                dt = datetime.datetime.fromtimestamp(ctime)
                dest_dir = date_rule_cfg.get('path_template', 'organized/{year}/{month}').format(year=dt.year, month=dt.month)
                os.makedirs(dest_dir, exist_ok=True)
                dest_path = os.path.join(dest_dir, os.path.basename(file_path))
                applied_rule = f"CreationDate: {dt.year}-{dt.month}"
                file_moved = True

        if file_moved and dest_path is not None:
            if dry_run:
                print(f"Dry run: Would move {file_path} to {dest_path}")
            else:
                # Check for potential conflict: if file exists at destination, append timestamp
                if os.path.exists(dest_path):
                    base, extension = os.path.splitext(dest_path)
                    dest_path = base + '_' + str(int(time.time())) + extension
                shutil.move(file_path, dest_path)
                # Log the operation in the database
                database.log_operation(time.strftime('%Y-%m-%d %H:%M:%S'), file_path, dest_path, applied_rule)
                print(f"Moved {file_path} to {dest_path} using rule {applied_rule}")
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")
