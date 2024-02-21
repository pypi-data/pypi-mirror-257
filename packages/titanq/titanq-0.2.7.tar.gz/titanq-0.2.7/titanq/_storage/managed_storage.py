import logging
import requests
import time

from .._client.model import UrlInput, UrlOutput
from .storage_client import StorageClient
from .._client.client import Client

log = logging.getLogger("TitanQ")


class ManagedStorage(StorageClient):
    def __init__(self, titanq_client: Client):
        """
        Initiate the managed storage client for handling the temporary files.

        :titanq_client: titanq_client to be used to fetch temporary URL's
        """
        self._titanq_client = titanq_client
        self._urls = titanq_client.temp_storage()

    def _upload_arrays(self, bias: bytes, weights: bytes):
        log.debug(f"Uploading bias array on our temporary storage")
        requests.put(self._urls.input.bias_file.upload, data=bias)

        log.debug(f"Uploading weights array on our temporary storage")
        requests.put(self._urls.input.weights_file.upload, data=weights)

    def _input(self) -> UrlInput:
        return UrlInput(
            weights_file_name=self._urls.input.weights_file.download,
            bias_file_name=self._urls.input.bias_file.download)

    def _output(self) -> UrlOutput:
        return UrlOutput(result_archive_file_name=self._urls.output.result_archive_file.upload)

    def wait_for_result_to_be_uploaded_and_download(self) -> bytes:
        self._wait_for_file_to_be_uploaded(self._urls.output.result_archive_file.download)
        return self._download_file(self._urls.output.result_archive_file.download)

    def _wait_for_file_to_be_uploaded(self, url: str):
        """
        Wait until the content of the file in the temporary storage is bigger
        than 0 bytes. Meaning it will wait until the file is uploaded

        :param url: Url to download the file.
        """
        response = requests.get(url)
        response.raise_for_status()
        while len(response.content) == 0:
            time.sleep(0.25)
            response = requests.get(url)
            response.raise_for_status()

    def _download_file(self, url) -> bytes:
        """
        Download file from the temporary storage

        :param url: Url to download the file.

        :return: content of the file in bytes
        """
        log.debug(f"Downloading object from the temporary storage")
        request = requests.get(url)
        return request.content

    def _delete_remote_object(self) -> None:
        log.debug("Temporary storage option does not delete any file at the moment")