def build_lineage_path(doc_id, heading_path, chunk_id):

    heading_path = heading_path or "root"

    return f"{doc_id}/{heading_path}/{chunk_id}"