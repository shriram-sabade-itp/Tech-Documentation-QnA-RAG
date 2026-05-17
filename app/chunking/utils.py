def sliding_window(items, window_size, overlap):

    start = 0

    while start < len(items):

        end = start + window_size

        yield items[start:end]

        start += window_size - overlap