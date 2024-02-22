from socaity.core.endpoint import EndPoint
from socaity.core.job import Job
import requests

class Client:
    """
    A Client handles the requests to an API.
    """

    def __init__(self, endpoint: EndPoint):
        self.endpoint = endpoint

        self._job_queue = []
        self._results = []

    def __call__(self, *args, **kwargs):
        return self.run(*args, **kwargs)

    def prepare_payload(self, job: Job) -> Job:
        """
        Subclass this method to implement your own payload preparation.
        This is for example needed in web requests to have post, get and file parameters.
        """
        return job

    def request(self, job: Job):
        """
        The method to make the request to the API.
        Subclass this method.
        """
        raise NotImplementedError("Subclass the request method")

    def run(self, job: Job, *args, **kwargs) -> Job:
        """
        Run the job.
        """
        # call pre_process function of client api (which is referenced in the job)
        job.pre_process_params()
        # obtain post, get, and files for web request
        self.prepare_payload(job)
        # make the request
        print(f"Requesting {self.endpoint.endpoint_name} with job {job.job_statistics.created}")
        endpoint_result = self.request(job)  # result is also stored in the job
        # call post_process function of client api
        job.post_process_result(endpoint_result)
        print(f"Job {job.job_statistics.created} finished in {job.job_statistics.get_execution_time()} seconds.")
        return job

    def run_async(self):
        pass



