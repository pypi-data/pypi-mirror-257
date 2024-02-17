import io
import typing
import urllib.parse

import aioboto3

from approck_services.base import BaseService


class BaseUploadService(BaseService):
    def __init__(
        self,
        aws_access_key_id: str,
        aws_secret_access_key: str,
        region_name: str,
        bucket: str,
        endpoint_url: typing.Optional[str] = None,
    ) -> None:
        super().__init__()

        self.session = aioboto3.Session(
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region_name,
        )

        self.bucket = bucket
        self.endpoint_url = endpoint_url

    async def upload_from_bytes(self, key: str, body: bytes) -> str | None:
        with io.BytesIO(body) as spfp:
            return await self.upload_from_file(key=key, file_=spfp)

    async def upload_from_file(self, key: str, file_: typing.BinaryIO) -> str | None:
        async with self.session.client("s3", endpoint_url=self.endpoint_url) as s3:
            await s3.upload_fileobj(file_, self.bucket, key)

        if self.endpoint_url is not None:
            return f"{self.endpoint_url}/{self.bucket}/{urllib.parse.quote(key)}"

        return None
