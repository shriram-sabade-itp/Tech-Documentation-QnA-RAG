import numpy as np


def normalize_vector(vector):

    """
    Normalize vector for cosine similarity.
    """

    vector = np.array(vector)

    norm = np.linalg.norm(vector)

    if norm == 0:
        return vector

    return vector / norm