from typing import Any, Dict, Optional, Union
from urllib.parse import ParseResult, parse_qs, urlencode, urljoin, urlparse, urlunparse

from IPython.display import IFrame
from requests import Session

from datarefiner_client.iclient import IDataRefinerClient


class ExploreEntrypoints(IDataRefinerClient):
    _base_url: str
    session: Session

    def __init__(self, *args, **kwargs) -> None:
        self._explore_url = urljoin(self._base_url, "/explore")
        super(ExploreEntrypoints, self).__init__(*args, **kwargs)

    def _make_request(self, url: str, method: str = "GET", *args: object, **kwargs: object) -> Optional[Dict[str, Any]]:
        pass

    def _make_project_explore_url(self, project_id: int) -> str:
        project_explore_url = urljoin(f"{self._explore_url}/", str(project_id))
        project_explore_url_parts = list(urlparse(project_explore_url))
        query_params = parse_qs(project_explore_url_parts[4])
        query_params["is_notebook"] = 1
        project_explore_url_parts[4] = urlencode(query_params)
        return urlunparse(project_explore_url_parts)

    def explore(
        self, project_id: int, width: Optional[Union[int, str]] = None, height: Optional[Union[int, str]] = None
    ) -> IFrame:
        width = width or "100%"
        height = height or 720

        project_explore_url_parts: ParseResult = urlparse(self._make_project_explore_url(project_id=project_id))

        login_url_parts: ParseResult = list(urlparse(urljoin(self._base_url, "/login")))
        query_params = parse_qs(login_url_parts[4])
        query_params["next"] = f"{project_explore_url_parts.path}?{project_explore_url_parts.query}"
        query_params["is_notebook"] = 1
        login_url_parts[4] = urlencode(query_params)
        login_url = urlunparse(login_url_parts)

        return IFrame(
            src=login_url,
            width=width,
            height=height,
            extras=[
                'sandbox="allow-same-origin || allow-top-navigation || allow-forms || allow-scripts || allow-downloads"'
            ],
        )
