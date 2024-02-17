import json
import os
from typing import Dict, List, Union

import requests

from ._exceptions import AutomizorJobError

JSON = Union[str, int, float, bool, None, Dict[str, "JSON"], List["JSON"]]


class Job:
    """
    `Job` is a class that facilitates interaction with job-specific data within the
    `Automizor Platform`, allowing for the retrieval and updating of job context and
    results. It provides mechanisms to access job context either from a local file or
    directly from the `Automizor API`, based on the environment configuration. Additionally,
    it offers functionality to save job results, enhancing automation workflows.

    This class utilizes environment variables for configuration, specifically for setting
    up the API host and API token, which are essential for authenticating requests made
    to the `Automizor Storage API`. These variables are typically configured by the
    `Automizor Agent`.

    The job ID is required to fetch the job context from the `Automizor API`. If a job ID
    is not available in the environment, the context can be read from a local file by setting
    the `AUTOMIZOR_CONTEXT_FILE` environment variable. In this case, no other environment
    variables are required.

    To use this class effectively, ensure that the following environment variables are
    set in your environment:

    - ``AUTOMIZOR_API_HOST``: The URL of the `Automizor API` host.
    - ``AUTOMIZOR_API_TOKEN``: The authentication token for API access.
    - ``AUTOMIZOR_CONTEXT_FILE``: The path to a local file containing job context, if used.
    - ``AUTOMIZOR_JOB_ID``: The identifier for the current job, used when fetching context via API.

    Example usage:

    .. code-block:: python

        from automizor import job

        # Retrieving job context
        context = job.get_context()
        print(context)  # Output: {"key": "value"}

        # Saving a job result
        job.set_result("result_name", {"key": "value"})
    """

    def __init__(self):
        self._api_host = os.getenv("AUTOMIZOR_API_HOST")
        self._api_token = os.getenv("AUTOMIZOR_API_TOKEN")
        self._context_file = os.getenv("AUTOMIZOR_CONTEXT_FILE")
        self._job_id = os.getenv("AUTOMIZOR_JOB_ID")

        self.session = requests.Session()
        self.session.headers.update(
            {
                "Authorization": f"Token {self._api_token}",
                "Content-Type": "application/json",
            }
        )

    def get_context(self) -> dict:
        """
        Retrieves the context of the current job, which contains necessary information
        for job execution. The context can be fetched from two sources based on the
        environment configuration:

        1. A local file specified by the `AUTOMIZOR_CONTEXT_FILE` environment variable.
        This is useful in environments where direct access to the `Automizor API` is
        not possible or preferred.
        2. The `Automizor API`, using the job ID (`AUTOMIZOR_JOB_ID`) to fetch the specific
        job context. This requires valid API host (`AUTOMIZOR_API_HOST`) and token
        (`AUTOMIZOR_API_TOKEN`) settings.

        Returns:
            A dictionary containing the job context.

        Raises:
            AutomizorJobError: If retrieving the job context fails.
        """

        if self._context_file:
            return self._read_file_context()
        return self._read_job_context()

    def set_result(self, name: str, value: JSON):
        """
        Saves the result of the job execution to a local JSON file (`output/result.json`).
        The `Automizor Agent` uploads this file to the `Automizor Platform` after the job.

        The result is stored as a key-value pair within the JSON file, where the key is the
        name of the result and the value is the result itself. If the file already exists,
        this method updates the file with the new result, merging it with any existing data.
        If the file does not exist, it is created.

        Parameters:
            name: The name of the result, used as a key in the JSON file.
            value: The result value, must be JSON serializable.

        Note:
            This method does not handle exceptions related to file access or JSON serialization
            internally. It is the caller's responsibility to handle such exceptions as needed.
        """

        data = {}
        file_path = "output/result.json"
        try:
            if os.path.exists(file_path):
                with open(file_path, "r", encoding="utf-8") as file:
                    data = json.load(file)
        except json.JSONDecodeError:
            pass

        data[name] = value

        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    def _read_file_context(self) -> dict:
        with open(self._context_file, "r", encoding="utf-8") as file:
            return json.load(file)

    def _read_job_context(self) -> dict:
        url = f"https://{self._api_host}/api/v1/rpa/job/{self._job_id}/"
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return response.json().get("context", {})
        except Exception as exc:
            raise AutomizorJobError(f"Failed to get job context: {exc}") from exc
