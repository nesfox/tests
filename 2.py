# Задача №2 Автотест API Яндекса

import requests
import time
import uuid

API_BASE_URL = "https://cloud-api.yandex.net/v1/disk/resources"


def read_token_from_file(file_path):
    """
    Reads a token from a file specified by its path.

    Args:
        file_path (str): The path to the file containing the token.

    Raises:
        FileNotFoundError: If the file does not exist.
        RuntimeError: If there was an error reading the file contents.

    Returns:
        str: The token read from the file.
    """
    try:
        with open(file_path, "r") as file:
            token = file.read().strip()
            if not token:
                raise ValueError("Token is empty or missing.")
            return token
    except FileNotFoundError:
        raise FileNotFoundError(f"File '{file_path}' not found.")
    except Exception as e:
        raise RuntimeError(f"Failed to read token from file: {e}")


def create_folder(folder_name, token) -> requests.Response:
    """
    Creates a new folder on Yandex Disk using the provided token.

    Args:
        folder_name (str): Name of the folder to be created.
        token (str): Token used for authentication.

    Returns:
        requests.Response: The response from the server after attempting to create the folder.
    """
    url = f"{API_BASE_URL}"
    headers = {"Authorization": f"OAuth {token}"}
    params = {"path": folder_name}
    response = requests.put(url, headers=headers, params=params)
    return response


def list_folders(token):
    """
    Retrieves a list of all available folders on Yandex Disk.

    Args:
        token (str): Token used for authentication.

    Returns:
        list: A list of dictionaries representing folders.
    """
    url = f"{API_BASE_URL}resources/files"
    headers = {"Authorization": f"OAuth {token}"}
    response = requests.get(url, headers=headers)
    return response.json().get("_embedded", {}).get("items", [])


def find_folder_in_list(folders, folder_name):
    """
    Checks whether a specific folder exists within a list of folders.

    Args:
        folders (list): List of folders to search through.
        folder_name (str): Name of the folder to look for.

    Returns:
        bool: Whether the folder is present in the list of folders.
    """
    return any(item["name"] == folder_name for item in folders)


class TestYandexDiskAPITests:
    def setup_method(self):
        """
        Sets up the test fixture by reading a token from a file and generating a unique folder name.
        """
        self.token = read_token_from_file("token_ya.txt")
        self.folder_name = f"test-folder-{uuid.uuid4()}"

    def teardown_method(self):
        """
        Tears down the test fixture by deleting the created folder.
        """
        delete_url = f"{API_BASE_URL}"
        headers = {"Authorization": f"OAuth {self.token}"}
        params = {"path": self.folder_name}
        delete_response = requests.delete(delete_url, headers=headers, params=params)
        if delete_response.status_code not in [202, 204]:
            print(f"Warning: Failed to delete folder {self.folder_name}. Status code: {delete_response.status_code}")

    def test_create_folder_successfully(self):
        """
        Tests successful creation of a folder on Yandex Disk.

        Raises:
            AssertionError: If the folder could not be created successfully.
        """
        response = create_folder(self.folder_name, self.token)
        assert response.status_code == 201, (f"Failed to create folder. Status code: {response.status_code}, "
                                             f"Response: {response.text}")

    def test_created_folder_appears_in_list(self):
        """
        Verifies that a newly created folder appears in the list of folders on Yandex Disk.

        Raises:
            AssertionError: If the folder does not appear in the list of folders.
        """
        create_folder(self.folder_name, self.token)
        time.sleep(10)  # Increases delay to ensure folder is visible.
        folders = list_folders(self.token)
        assert find_folder_in_list(folders, self.folder_name), "Folder not found in the list of files"

    def test_create_folder_with_invalid_path_returns_bad_request(self):
        """
        Ensures that trying to create a folder with an invalid path results in a Bad Request status code.

        Raises:
            AssertionError: If the status code received is not 400.
        """
        invalid_path = "invalid_path"
        response = create_folder(invalid_path, self.token)
        assert response.status_code == 400, (f"Expected bad request with invalid path. Status code: "
                                             f"{response.status_code}, Response: {response.text}")

    def test_invalid_token_returns_unauthorized(self):
        """
        Confirms that providing an invalid token returns an Unauthorized status code.

        Raises:
            AssertionError: If the status code returned is not 401.
        """
        invalid_token = "invalid-token"
        response = create_folder(self.folder_name, invalid_token)
        assert response.status_code == 401, (f"Expected unauthorized error with invalid token. Status code: "
                                             f"{response.status_code}, Response: {response.text}")

    def test_create_folder_with_invalid_path_returns_bad_request(self):
        """
        Verifies that creating a folder with an invalid path results in a Bad Request status code.

        Raises:
            AssertionError: If the status code received is not 400.
        """
        invalid_path = "/invalid/path"
        response = create_folder(invalid_path, self.token)
        assert response.status_code == 400, (f"Expected bad request with invalid path. Status Code: "
                                             f"{response.status_code}, Response: {response.text}")
