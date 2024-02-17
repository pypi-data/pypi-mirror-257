import json
import os
from typing import Any, Dict, List, Union

import requests

JSONType = Union[str, int, float, bool, None, Dict[str, Any], List[Any]]


class AutomizorJobError(RuntimeError):
    """Exception raised for errors encountered while interacting with the Job."""


class Job:
    """
    Represents a job in the `Automizor Platform`, managing the retrieval and storage of job
    context and results.

    This class provides functionality to interact with the `Automizor API` or local files to
    obtain job context and persist job results.

    For testing purposes, you may want to set the environment variables in your local environment.
    The required variables are:

    - ``AUTOMIZOR_API_HOST``: The host URL of the `Automizor API`
    - ``AUTOMIZOR_API_TOKEN``: The token used for authenticating with the `Automizor API`
    - ``AUTOMIZOR_JOB_ID``: The ID of the job from which to retrieve context

    Additionally, you can specify a local context file; in this case, you don't need to set the
    above environment variables:

    - ``AUTOMIZOR_CONTEXT_FILE``: The path to a local file containing the job context.

    Example of a local context file:

    .. code-block:: json

        {
            "key": "value"
        }

    Example usage:

    .. code-block:: python

        from automizor.job import Job

        job = Job()

        def read_context():
            context = job.get_job_context()
            print(context["key"])  # Output: "value"

        def save_result():
            job.set_job_result("result_key", "result_value")

    """

    def __init__(self):
        self._api_host = os.getenv("AUTOMIZOR_API_HOST")
        self._api_token = os.getenv("AUTOMIZOR_API_TOKEN")
        self._context_file = os.getenv("AUTOMIZOR_CONTEXT_FILE")
        self._job_id = os.getenv("AUTOMIZOR_JOB_ID")

    @property
    def headers(self) -> dict:
        """Headers for API requests, including Authorization and Content-Type."""
        return {
            "Authorization": f"Token {self._api_token}",
            "Content-Type": "application/json",
        }

    def get_job_context(self) -> dict:
        """
        Retrieves the job's context from either a local file or via an API call, based on
        the configuration.

        If a local context file is specified (via `AUTOMIZOR_CONTEXT_FILE`), it reads the context
        from the file. Otherwise, it fetches the context from the Automizor API using the job ID
        and API credentials.

        Returns:
            A dictionary with the job's context.

        Raises:
            AutomizorJobError: If retrieving the job context fails.
        """

        if self._context_file:
            return self._read_file_context()
        return self._read_job_context()

    def set_job_result(self, name: str, value: JSONType):
        """
        Saves a job result into a JSON file (`output/result.json`).

        Updates the file with the new result, creating or overwriting the file as necessary.
        If the file exists and contains data, it merges the new result with the existing data.

        Parameters:
            name (str): The key under which to store the result.
            value (JSONType): The result value, must be JSON serializable.

        Note: Errors during file operations will raise unhandled exceptions.
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
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            return response.json().get("context", {})
        except Exception as exc:
            raise AutomizorJobError(f"Failed to get job context: {exc}") from exc
