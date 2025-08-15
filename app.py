import os
import shutil
import argparse
import yaml
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

DEFAULT_CONFIG_PATH = 'config.yml'
DEFAULT_CONFIG_CONTENT = {
    'dir': '.',
    'ext': 'ext'
}

def ensure_config_file_exists():
    if not os.path.exists(DEFAULT_CONFIG_PATH):
        with open(DEFAULT_CONFIG_PATH, 'w') as f:
            yaml.dump(DEFAULT_CONFIG_CONTENT, f)
        logging.info(f"Created default config file: {DEFAULT_CONFIG_PATH}")


def read_yaml_config(file_path):
    try:
        with open(file_path, 'r') as f:
            return yaml.safe_load(f) or {}
    except Exception as e:
        logging.error(f"Failed to read config file: {e}")
        return {}


def generate_unique_filename(destination_path):
    base, ext = os.path.splitext(destination_path)
    counter = 1
    while os.path.exists(destination_path):
        destination_path = f"{base}_{counter}{ext}"
        counter += 1
    return destination_path


import errno

def safe_move(src, dst):
    try:
        shutil.move(src, dst)
        logging.info(f"Moved: {os.path.basename(src)} → {dst}")
    except FileExistsError as e:
        if e.errno == errno.EEXIST or "WinError 183" in str(e):
            dst_unique = generate_unique_filename(dst)
            try:
                shutil.move(src, dst_unique)
                logging.warning(f"File already exists. Renamed and moved to: {dst_unique}")
            except Exception as e2:
                logging.error(f"Failed to move after renaming: {e2}")
        else:
            logging.error(f"Unhandled FileExistsError: {e}")
    except Exception as e:
        logging.error(f"Failed to move {src} → {dst}: {e}")



def move_png_files(target_folder, ext_folder):
    destination = os.path.join(target_folder, ext_folder)
    os.makedirs(destination, exist_ok=True)

    for filename in os.listdir(target_folder):
        if filename.lower().endswith('.png'):
            src = os.path.join(target_folder, filename)
            dst = os.path.join(destination, filename)
            safe_move(src, dst)


def move_files_by_ext(ext, target_folder):
    ext = ext.lower()
    for filename in os.listdir(target_folder):
        if filename.lower().endswith(f'.{ext}'):
            base_name = os.path.splitext(filename)[0]
            folder_name = base_name.split(' ')[0]
            folder_path = os.path.join(target_folder, folder_name)

            # Check if a file (not folder) already exists with the desired folder name
            if os.path.exists(folder_path) and not os.path.isdir(folder_path):
                folder_path = folder_path + "_folder"

            os.makedirs(folder_path, exist_ok=True)

            src = os.path.join(target_folder, filename)
            dst = os.path.join(folder_path, filename)
            safe_move(src, dst)



def main():
    ensure_config_file_exists()

    parser = argparse.ArgumentParser(description='Organize image and video files.')
    parser.add_argument('--dir', type=str, help='Directory to scan for files.')
    parser.add_argument('--ext', type=str, help='Folder to move .png files into.')
    parser.add_argument('--config', type=str, help='Path to YAML configuration file.')

    args = parser.parse_args()

    config_path = args.config or DEFAULT_CONFIG_PATH
    config = read_yaml_config(config_path)

    target_folder = config.get('dir') or args.dir or '.'
    ext_folder = config.get('ext') or args.ext or 'ext'

    logging.info(f"Target directory: {target_folder}")
    logging.info(f"PNG destination subfolder: {ext_folder}")

    move_png_files(target_folder, ext_folder)
    move_files_by_ext('jpg', target_folder)
    move_files_by_ext('mov', target_folder)


if __name__ == "__main__":
    main()
