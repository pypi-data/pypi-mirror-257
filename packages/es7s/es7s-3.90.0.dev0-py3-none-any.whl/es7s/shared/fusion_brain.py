# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2024 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import io
import json
import typing as t
from functools import cached_property
from logging import getLogger
from uuid import UUID

import pytermor as pt
import requests
from requests import Response


class FusionBrainAPI:
    HOST = "https://api-key.fusionbrain.ai/"

    def __init__(self, api_key: str, secret_key: str):
        self._api_key = api_key
        self._secret_key = secret_key
        self._model_id: int | None = None
        self._style_names: list[str] = []

    @cached_property
    def _headers(self) -> dict:
        return {
            "X-Key": f"Key {self._api_key}",
            "X-Secret": f"Secret {self._secret_key}",
        }

    def copy(self) -> "FusionBrainAPI":
        c = FusionBrainAPI(self._api_key, self._secret_key)
        c._model_id = self._model_id
        c._style_names = c._style_names.copy()
        return c

    def fetch_model(self) -> int:
        response = requests.get(self.HOST + "key/api/v1/models", headers=self._headers)
        data = response.json()
        getLogger(__package__).debug("< " + format_attrs(data))

        self._model_id = int(data[0]["id"])
        return self._model_id

    def fetch_styles(self) -> list[str]:
        response = requests.get("https://cdn.fusionbrain.ai/static/styles/api")
        data = response.json()
        getLogger(__package__).debug("< " + format_attrs(data))

        self._style_names.clear()
        for style in data:
            self._style_names.append(style.get("name"))
        return self._style_names

    def generate(
        self,
        prompt: str,
        negprompt: list[str] = None,
        style: str = None,
        images=1,
        width=1024,
        height=1024,
    ) -> UUID:
        params = {
            "type": "GENERATE",
            "numImages": images,
            "width": width,
            "height": height,
            "generateParams": {"query": f"{prompt}"},
        }
        if negprompt:
            params.update({"negativePromptUnclip": ",".join(negprompt)})
        if style:
            params.update({"style": style})

        data = {
            "model_id": (None, self._model_id),
            "params": (None, json.dumps(params), "application/json"),
        }
        getLogger(__package__).debug("> " + format_attrs(data))
        response = requests.post(
            self.HOST + "key/api/v1/text2image/run",
            headers=self._headers,
            files=data,
            timeout=30,
        )
        data = response.json()
        getLogger(__package__).debug("< " + format_attrs(data))

        return UUID(data["uuid"])

    def check_generation(self, request_id: UUID) -> tuple[list[str], bool | None, Response]:
        response = requests.get(
            self.HOST + "key/api/v1/text2image/status/" + str(request_id),
            headers=self._headers,
            timeout=30,
        )
        try:
            data = response.json()
        except ValueError:
            return [], None, response
        getLogger(__package__).debug("< " + format_attrs(data, truncate=4096))

        if data["status"] == "DONE":
            return data.get("images", []), data.get("censored"), response
        return [], None, response


def format_attrs(*o: object, keep_classname=True, level=0, flat=False, truncate: int = None) -> str:
    kwargs = dict(flat=flat, truncate=truncate)

    def _to_str(a) -> str:
        if (s := str(a)).startswith(cn := a.__class__.__name__):
            if keep_classname:
                return s
            return s.removeprefix(cn)
        return f"'{s}'" if s.count(" ") else s

    def _wrap(s):
        if flat:
            return s
        return f"({s})"

    if len(o) == 1:
        o = o[0]
    if isinstance(o, str):
        if truncate is not None:
            return pt.cut(o, truncate)
        return o
    elif isinstance(o, t.Mapping):
        return _wrap(" ".join(f"{_to_str(k)}={format_attrs(v, **kwargs)}" for k, v in o.items()))
    elif issubclass(type(o), io.IOBase):
        return f"{pt.get_qname(o)}['{getattr(o, 'name', '?')}', {getattr(o, 'mode', '?')}]"
    elif isinstance(o, t.Iterable):
        return _wrap(" ".join(format_attrs(v, level=level + 1, **kwargs) for v in o))
    return _to_str(o)
