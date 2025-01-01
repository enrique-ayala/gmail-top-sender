"""This script fetches emails from Gmail and calculates the top senders by storage usage."""

import os
from collections import defaultdict
from dataclasses import dataclass
from typing import List, Tuple

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import Resource, build

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


@dataclass
class AnalysisResult:
    """Class for keeping track of results."""

    sorted_senders: List[Tuple[str, int]]
    total_messages: int


def get_gmail_service(client_secrets_path: str = "credentials.json") -> Resource:
    """Authenticate and return the Gmail API service resource.

    Args:
        client_secrets_path (str): The path to the client secrets file.

    Returns:
        Resource: The Gmail API service resource.
    """
    print("Authenticating with Gmail API...")
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                client_secrets_path, SCOPES
            )
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    print("Authentication successful.")
    return build("gmail", "v1", credentials=creds)


def get_top_senders(service: Resource, max_pages: int = 0) -> AnalysisResult:
    """Fetch messages from Gmail and calculate the top senders by storage usage.

    Args:
        service (Resource): The Gmail API service resource.
        max_pages (int): The maximum number of pages to fetch. If 0, fetch all pages.

    Returns:
        AnalysisResult: The result of the analysis.
    """
    print("Fetching messages from Gmail...")
    senders = defaultdict(int)
    page_token = None
    page_count = 0
    total_messages = 0

    while True:
        print(f"Fetching page {page_count + 1}...")
        results = (
            service.users()  # type: ignore
            .messages()
            .list(userId="me", maxResults=500, pageToken=page_token)
            .execute()
        )
        messages = results.get("messages", [])
        total_messages += len(messages)

        for message in messages:
            msg = (
                service.users().messages().get(userId="me", id=message["id"]).execute()  # type: ignore
            )
            headers = msg.get("payload", {}).get("headers", [])
            size = msg.get("sizeEstimate", 0)

            sender = next(
                (h["value"] for h in headers if h["name"] == "From"), "Unknown"
            )
            senders[sender] += size

        page_token = results.get("nextPageToken")
        page_count += 1

        if not page_token or (max_pages > 0 and page_count >= max_pages):
            break

    print("Finished fetching messages.")
    sorted_senders = sorted(senders.items(), key=lambda x: x[1], reverse=True)

    return AnalysisResult(sorted_senders, total_messages)


if __name__ == "__main__":
    service = get_gmail_service()
    results = get_top_senders(service, max_pages=0)

    print("====Top senders by storage usage:")
    for sender, size in results.sorted_senders[:10]:
        print(f"{sender}: {size / (1024 * 1024):.2f} MB")

    print(f"\nTotal number of senders: {len(results.sorted_senders)}")
    print(f"Total number of messages: {results.total_messages}")
