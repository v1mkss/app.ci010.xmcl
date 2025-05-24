import sys
import re
import logging
import requests
import json
import yaml
from pathlib import Path
import shutil

# --- Configuration ---
JSON_FILENAME = "io.github.voxelum.xmcl.json"
YAML_FILENAME = "io.github.voxelum.xmcl.yaml"
REPO_OWNER = "Voxelum"
REPO_NAME = "x-minecraft-launcher"

ARCH = "x64"
REPO_API_URL = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/releases/latest"
REQUEST_TIMEOUT = 15

# --- Logging Setup ---
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s: %(message)s',
    stream=sys.stderr,
)

# --- Functions ---

def error_exit(message: str, exit_code: int = 1):
    """Logs an error message and exits."""
    logging.error(message)
    sys.exit(exit_code)

def get_current_version_from_json(file_path: Path) -> str | None:
    """Gets the current version from the JSON file."""
    logging.info(f"Checking current version in {file_path}...")
    try:
        with file_path.open('r', encoding='utf-8') as f:
            data = json.load(f)
            for module in data.get('modules', []):
                if module.get('name') == 'xmcl':
                    for source in module.get('sources', []):
                        url = source.get('url', '')
                        if 'xmcl-' in url and '.tar.xz' in url:
                            version = re.search(r'xmcl-(\d+\.\d+\.\d+)-x64\.tar\.xz', url)
                            if version:
                                version = version.group(1)
                                logging.info(f"Current version found: {version}")
                                return version
            logging.warning(f"Could not find current version in {file_path}.")
            return None
    except (IOError, json.JSONDecodeError) as e:
        error_exit(f"Failed to read {file_path}: {e}")
        return None

def get_current_version_from_yaml(file_path: Path) -> str | None:
    """Gets the current version from the YAML file."""
    logging.info(f"Checking current version in {file_path}...")
    try:
        with file_path.open('r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
            for module in data.get('modules', []):
                if module.get('name') == 'xmcl':
                    for source in module.get('sources', []):
                        url = source.get('url', '')
                        if 'xmcl-' in url and '.tar.xz' in url:
                            version = re.search(r'xmcl-(\d+\.\d+\.\d+)-x64\.tar\.xz', url)
                            if version:
                                version = version.group(1)
                                logging.info(f"Current version found: {version}")
                                return version
            logging.warning(f"Could not find current version in {file_path}.")
            return None
    except (IOError, yaml.YAMLError) as e:
        error_exit(f"Failed to read {file_path}: {e}")
        return None

def get_latest_tag_from_github() -> str:
    """Fetches the latest release tag name from the GitHub API."""
    try:
        response = requests.get(REPO_API_URL, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        data = response.json()
        tag = data.get('tag_name')

        if not tag:
            error_exit(f"Could not find 'tag_name' in API response from {REPO_API_URL}. Response: {data}")

        if not re.match(r'^v\d+\.\d+\.\d+$', tag):
            error_exit(f"Fetched tag '{tag}' does not match expected format (e.g., vX.Y.Z).")

        return tag

    except requests.exceptions.Timeout:
        error_exit(f"Request timed out while fetching {REPO_API_URL}.")
    except requests.exceptions.HTTPError as e:
        error_message = f"HTTP Error fetching latest release: {e}\nURL: {REPO_API_URL}"
        if e.response.status_code in (403, 429):
            error_message += "\nPossible reason: GitHub API rate limit exceeded. Wait or use an access token."
        elif e.response.status_code == 404:
            error_message += f"\nPossible reason: Repository '{REPO_OWNER}/{REPO_NAME}' or API endpoint not found."
        error_exit(error_message)
    except requests.exceptions.RequestException as e:
        error_exit(f"Network error fetching latest release: {e}\nURL: {REPO_API_URL}")
    except ValueError as e:
        error_exit(f"Failed to decode JSON response from {REPO_API_URL}. Error: {e}")
    return ""

def get_sha256_for_tag(tag: str) -> str:
    """Downloads and returns the SHA256 hash for a given tag and architecture."""
    if not tag.startswith('v'):
        error_exit(f"Tag '{tag}' must start with 'v'.")

    version = tag.lstrip('v')
    sha256_filename = f"xmcl-{version}-{ARCH}.tar.xz.sha256"
    sha256_url = f"https://github.com/{REPO_OWNER}/{REPO_NAME}/releases/download/{tag}/{sha256_filename}"

    try:
        response = requests.get(sha256_url, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        sha256_content = response.text.strip()

        if not sha256_content:
            error_exit(f"Received empty content from SHA256 URL: {sha256_url}")

        if not re.match(r'^[a-f0-9]{64}$', sha256_content):
            error_exit(f"Content from SHA256 URL ('{sha256_content}') does not look like a valid SHA256 hash.")

        return sha256_content

    except requests.exceptions.Timeout:
        error_exit(f"Request timed out while fetching {sha256_url}.")
    except requests.exceptions.HTTPError as e:
        error_exit(f"HTTP Error {e.response.status_code} fetching SHA256.\nURL: {sha256_url}\nCheck if the asset exists for tag {tag} and architecture {ARCH}.")
    except requests.exceptions.RequestException as e:
        error_exit(f"Network error fetching SHA256: {e}\nURL: {sha256_url}")
    return ""

def update_json_file(file_path: Path, new_version: str, new_sha256: str):
    """Updates the version and sha256 in the JSON file."""
    backup_path = file_path.with_suffix(file_path.suffix + '.bak')

    try:
        with file_path.open('r', encoding='utf-8') as f:
            data = json.load(f)

        # Create backup before modification
        logging.info(f"Creating backup: {backup_path}")
        shutil.copy2(file_path, backup_path)

        # Update version and sha256
        for module in data.get('modules', []):
            if module.get('name') == 'xmcl':
                for source in module.get('sources', []):
                    if 'xmcl-' in source.get('url', '') and '.tar.xz' in source['url']:
                        source['url'] = f"https://github.com/{REPO_OWNER}/{REPO_NAME}/releases/download/v{new_version}/xmcl-{new_version}-{ARCH}.tar.xz"
                        source['sha256'] = new_sha256

        # Write updated content
        with file_path.open('w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)

        logging.info(f"\033[32mSuccessfully updated {file_path}\033[0m")
        backup_path.unlink()
        logging.info(f"Removed backup file: {backup_path}")

    except Exception as e:
        logging.error(f"Error updating JSON file {file_path}: {e}")
        if backup_path.exists():
            try:
                shutil.move(backup_path, file_path)
                logging.info("Restored from backup successfully.")
            except Exception as restore_err:
                logging.error(f"Failed to restore from backup: {restore_err}")
        error_exit("File update failed.", 2)

def update_yaml_file(file_path: Path, new_version: str, new_sha256: str):
    """Updates the version and sha256 in the YAML file."""
    backup_path = file_path.with_suffix(file_path.suffix + '.bak')

    try:
        with file_path.open('r', encoding='utf-8') as f:
            data = yaml.safe_load(f)

        # Create backup before modification
        logging.info(f"Creating backup: {backup_path}")
        shutil.copy2(file_path, backup_path)

        # Update version and sha256
        for module in data.get('modules', []):
            if module.get('name') == 'xmcl':
                for source in module.get('sources', []):
                    if 'xmcl-' in source.get('url', '') and '.tar.xz' in source['url']:
                        source['url'] = f"https://github.com/{REPO_OWNER}/{REPO_NAME}/releases/download/v{new_version}/xmcl-{new_version}-{ARCH}.tar.xz"
                        source['sha256'] = new_sha256

        # Write updated content
        with file_path.open('w', encoding='utf-8') as f:
            yaml.dump(data, f, default_flow_style=False, sort_keys=False)

        logging.info(f"\033[32mSuccessfully updated {file_path}\033[0m")
        backup_path.unlink()
        logging.info(f"Removed backup file: {backup_path}")

    except Exception as e:
        logging.error(f"Error updating YAML file {file_path}: {e}")
        if backup_path.exists():
            try:
                shutil.move(backup_path, file_path)
                logging.info("Restored from backup successfully.")
            except Exception as restore_err:
                logging.error(f"Failed to restore from backup: {restore_err}")
        error_exit("File update failed.", 2)

def update_files(json_path: Path, yaml_path: Path, new_version: str, new_sha256: str):
    """Updates both JSON and YAML files if they exist."""
    if json_path.is_file():
        update_json_file(json_path, new_version, new_sha256)
    if yaml_path.is_file():
        update_yaml_file(yaml_path, new_version, new_sha256)

def main():
    """Main script logic."""
    json_file = Path(JSON_FILENAME)
    yaml_file = Path(YAML_FILENAME)

    if not json_file.is_file() and not yaml_file.is_file():
        error_exit(f"Neither {json_file} nor {yaml_file} found.")

    # Get current version from either file
    current_version = None
    if json_file.is_file():
        current_version = get_current_version_from_json(json_file)
    if current_version is None and yaml_file.is_file():
        current_version = get_current_version_from_yaml(yaml_file)

    # Get latest version from GitHub
    latest_tag = get_latest_tag_from_github()
    latest_version = latest_tag.lstrip('v')
    logging.info(f"Latest version from GitHub: {latest_version} (tag: {latest_tag})")

    # Compare versions
    if current_version == latest_version:
        logging.info(f"\033[32mVersion {latest_version} is already up-to-date. No update needed.\033[0m")
        sys.exit(0)

    # Update files
    new_sha256 = get_sha256_for_tag(latest_tag)
    update_files(json_file, yaml_file, latest_version, new_sha256)

    logging.info("\033[32mUpdate process finished.\033[0m")

if __name__ == "__main__":
    try:
        import requests
        import yaml
    except ImportError as e:
        error_exit(f"Required Python package not installed: {e}. Please install it (e.g., 'pip install {e.name}').")

    main()
