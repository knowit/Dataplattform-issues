import json
import get_docs

docs = [
    {
        "timestamp": 123,
        "ost": "you",
        "el": "me"
    },
    {
        "timestamp": 321,
        "ost": "aeee",
        "el": "eee"
    },
    {
        "timestamp": 9999,
        "ost": "ayy",
        "el": "lmao"
    },
    {
        "timestamp": 66666,
        "ost": "oooo",
        "el": "la"
    }
]


def test_format_response_n_0():
    body = get_docs.format_response(docs, "example.org", n=0)
    body_correct = json.dumps({
        "url": "example.org",
        "docs": []
    })
    assert body == body_correct


def test_format_response_n_1():
    body = get_docs.format_response(docs, "example.org", n=1)
    body_correct = json.dumps({
        "url": "example.org",
        "docs": [
            {
                "timestamp": 66666,
                "ost": "oooo",
                "el": "la"}
        ]
    })
    assert body == body_correct


def test_format_response_n_4():
    body = get_docs.format_response(docs, "example.org", n=4)
    body_correct = json.dumps({
        "url": "example.org",
        "docs": [
            {
                "timestamp": 66666,
                "ost": "oooo",
                "el": "la"
            },
            {
                "timestamp": 9999,
                "ost": "ayy",
                "el": "lmao"
            },
            {
                "timestamp": 321,
                "ost": "aeee",
                "el": "eee"
            },
            {
                "timestamp": 123,
                "ost": "you",
                "el": "me"
            }
        ]
    })
    assert body == body_correct


def test_format_response_n_high():
    body = get_docs.format_response(docs, "example.org", n=100)
    body_correct = json.dumps({
        "url": "example.org",
        "docs": [
            {
                "timestamp": 66666,
                "ost": "oooo",
                "el": "la"
            },
            {
                "timestamp": 9999,
                "ost": "ayy",
                "el": "lmao"
            },
            {
                "timestamp": 321,
                "ost": "aeee",
                "el": "eee"
            },
            {
                "timestamp": 123,
                "ost": "you",
                "el": "me"
            }
        ]
    })
    assert body == body_correct
