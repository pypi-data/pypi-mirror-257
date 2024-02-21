from sigmaepsilon.core.downloads import _download_file


def download_bernoulli_console_json_linstat():  # pragma: no cover
    """
    Downloads the description of a simple bernoulli console as a json file.

    Returns
    -------
    str
        A path to a file on your filesystem.

    Example
    --------
    >>> from sigmaepsilon.examples import download_bernoulli_console_json_linstat
    >>> jsonpath = download_bernoulli_console_json_linstat()
    """
    return _download_file("console_bernoulli_linstat.json")[0]
