import blog_poller
import pickle


def read_html_from_pickle():
    with open('poller/daily_poller/test/website_data.pickle', 'rb') as handle:
        return pickle.load(handle)


def test_get_medium_data_dict():
    html = read_html_from_pickle()
    medium_data = blog_poller.get_medium_data_dict(html)

    docs = blog_poller.create_docs(medium_data)

    assert len(docs) == 10

    first_subtitle_correct = "Best of is making a comeback! Since the beginning of this year, we" \
                             " have uploaded no less than 81🙀 videos on Knowit’s YouTube channel…"
    # This is going to fail if utf-8 is no longer working because of the emoji.
    assert first_subtitle_correct == docs[0]["subtitle"]

    for doc in docs:
        assert "title" in doc
        assert "id" in doc
        assert "author" in doc
        assert "subtitle" in doc
        assert "created" in doc
