import numpy as np

from inferelator_velocity.utils.noise2self import (
    _dist_to_row_stochastic,
    dot
)

def global_graph(
    data,
    layer="X",
    standardization_method='log',
    neighbors=None,
    npcs=None,
    use_sparse=True,
    connectivity=False,
    verbose=False,
    **kwargs
):
    """
    Use a noise2self kNN to denoise data

    :param data: Data AnnData object
    :type data: ad.AnnData
    :param layer: Layer to use for kNN, defaults to "X"
    :type layer: str, optional
    :param standardization_method: Depth-normalize and log1p data ('log')
        or depth-normalize and run robust scaler ('scale'). Defaults to 'log'.
    :type standardization_method: str, optional
    :param neighbors: Search space for k neighbors,
        defaults to 15 - 105 by 10
    :type neighbors: np.ndarray, optional
    :param npcs: Search space for number of PCs,
        defaults to 5-105 by 10
    :type npcs: np.ndarray, optional
    :param use_sparse: Use sparse data structures (slower).
        Will densify a sparse expression matrix (faster, more memory) if False,
        defaults to True
    :type use_sparse: bool
    :param connectivity: Use a connectivity graph instead of a distance graph,
        defaults to False
    :type connectivity: bool, optional
    :param verbose: Print detailed status, defaults to False
    :type verbose: bool, optional
    :return: AnnData object with `noise2self` obps and uns key
    :rtype: ad.AnnData
    """