from dataclasses import dataclass


@dataclass()
class CommitMessage:
    title: str
    body: str


{
    "cbdc56a1": CommitMessage(
        "Move rolling average functionality to separate class",
        "long desc i'm too lazy to write"
    ),
    "ce729611": CommitMessage(
        "Decrease target range for trigno",
        "long desc i'm too lazy to write"
    )
}
