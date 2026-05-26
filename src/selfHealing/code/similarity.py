from rapidfuzz import fuzz


def text_similarity(a, b):
    a = str(a or "")
    b = str(b or "")

    return round(
        fuzz.ratio(a.lower(), b.lower()) / 100,
        2
    )


def tag_match(tag1, tag2):
    return 1 if tag1 == tag2 else 0