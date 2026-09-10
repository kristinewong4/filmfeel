import numpy as np
from unittest.mock import patch

from embeddings import get_top_matches


def _fake_encode(texts):
    return np.array(texts if isinstance(texts, np.ndarray) else texts)


def test_get_top_matches_ranks_by_similarity():
    metadata = {"a": "...", "b": "...", "c": "..."}
    embeddings = np.array([
        [1.0, 0.0],   # a: orthogonal to the phrase
        [0.0, 1.0],   # b: identical direction to the phrase
        [0.7, 0.7],   # c: partially aligned
    ])

    with patch("embeddings.model") as mock_model:
        mock_model.encode.return_value = np.array([[0.0, 1.0]])
        results = get_top_matches("cozy rainy night", metadata, embeddings, top_n=3)

    ranked_movies = [movie for movie, _score in results]
    assert ranked_movies == ["b", "c", "a"]


def test_get_top_matches_respects_top_n():
    metadata = {"a": "...", "b": "...", "c": "..."}
    embeddings = np.array([
        [1.0, 0.0],
        [0.0, 1.0],
        [0.7, 0.7],
    ])

    with patch("embeddings.model") as mock_model:
        mock_model.encode.return_value = np.array([[0.0, 1.0]])
        results = get_top_matches("cozy rainy night", metadata, embeddings, top_n=1)

    assert len(results) == 1
    assert results[0][0] == "b"
