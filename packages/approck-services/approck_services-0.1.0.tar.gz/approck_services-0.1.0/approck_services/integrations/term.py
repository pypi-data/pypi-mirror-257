import datetime
from collections import defaultdict
from typing import Dict, List, Tuple

import httpx
from html_sanitizer import Sanitizer

from approck_services.base import BaseService


class BaseTermService(BaseService):
    TERMS_TTL_S = 60
    TERMS_DEFAULT_LANGUAGE = "ru"

    def __init__(self, base_url: str) -> None:
        super().__init__()

        self.client = httpx.AsyncClient(base_url=base_url)
        self.terms: Dict[str, Dict[Tuple[str, str], str]] = defaultdict(dict)
        self.updated_at: Dict[str, datetime.datetime] = {}

    async def _load_terms(self, namespace: str):
        response = await self.client.get(f"/v1/terms?namespaces[]={namespace}")
        response.raise_for_status()

        self.terms = defaultdict(dict)

        for raw_term in response.json():
            for translation in raw_term["translations"]:
                self.terms[translation["language"]][(raw_term["name"], namespace)] = translation["content"]

        self.updated_at[namespace] = datetime.datetime.utcnow()

    async def term(self, language: str, name: str, namespace: str, *args, **kwargs) -> str:
        if (
            not self.updated_at
            or self.updated_at.get(namespace, datetime.datetime.fromtimestamp(0))
            + datetime.timedelta(seconds=self.TERMS_TTL_S)
            < datetime.datetime.utcnow()
        ):
            await self._load_terms(namespace)

        if language in self.terms:
            localized_terms = self.terms[language]
        else:
            localized_terms = self.terms[self.TERMS_DEFAULT_LANGUAGE]

        if (name, namespace) not in localized_terms:
            return name

        content = localized_terms[(name, namespace)]
        content = content.format(*args, **kwargs)

        return content

    async def term_html(
        self,
        language: str,
        name: str,
        namespace: str,
        *args,
        strip_new_line: bool = True,
        **kwargs,
    ) -> str:
        content = await self.term(language, name, namespace, *args, **kwargs)

        return self.sanitize(content=content, strip_new_line=strip_new_line)

    @staticmethod
    def sanitize(content: str, strip_new_line: bool = True) -> str:
        sanitized_content = (
            Sanitizer(
                {
                    "tags": {"a", "br", "b", "strong", "i", "em", "code", "s", "strike", "del", "u"},
                    "attributes": {"a": ("href",)},
                    "whitespace": set(),
                    "empty": {"a", "br"},
                    "separate": {"br"},
                }
            )
            .sanitize(content.replace("<p>", "").replace("</p>", "\n").replace("\n", "<br>"))
            .replace("<br>", "\n")
        )

        if strip_new_line:
            sanitized_content = sanitized_content.strip("\n")

        return sanitized_content

    async def create_terms(self, terms: List[Dict[str, str]]) -> None:
        response = await self.client.put("/v1/internal/terms", json=terms)
        response.raise_for_status()

    async def delete_terms(self, namespace: str) -> None:
        response = await self.client.delete(f"/v1/internal/terms?namespaces[]={namespace}")
        response.raise_for_status()
