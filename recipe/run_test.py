"""Exercise model loading and endpoint resolution without AWS requests."""

from botocore.session import get_session
from botocore.stub import Stubber


client = get_session().create_client(
    "s3",
    region_name="us-east-1",
    verify=True,
    aws_access_key_id="testing",
    aws_secret_access_key="testing",
)
with Stubber(client) as stubber:
    stubber.add_response("list_buckets", {"Buckets": []})
    assert client.list_buckets()["Buckets"] == []
client.close()
