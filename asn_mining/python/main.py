if __name__ == "__main__":
    import stats
    import os
    download = os.environ.get("DOWNLOAD", "true").lower() == "true"
    cache = os.environ.get("CACHE", "false").lower() == "true"
    stats.stats(download, cache)