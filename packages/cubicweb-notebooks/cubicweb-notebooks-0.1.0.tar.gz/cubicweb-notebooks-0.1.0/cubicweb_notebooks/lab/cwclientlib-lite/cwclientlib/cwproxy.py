import requests


class CWProxy:
    def __init__(self, url):
        self.url = url
        self._default_vid = "jsonexport"

    def rql(self, query):
        headers = {
            "Content-Type": "application/json",
        }
        query = query.replace(" ", "+")
        return requests.get(
            self.url + "/view" + f"?vid=jsonexport&rql={query}",
            headers=headers,
        )

    def view(self, vid: str, **args):
        headers = {"Accept": "application/json"}
        params_str = f"?vid={vid}&" + "&".join(
            [f"{key}={val}" for key, val in args.items()]
        )
        return requests.get(
            self.url + "/view" + params_str,
            headers=headers,
        )

    def rqlio(self, *kwargs):
        raise NotImplementedError
