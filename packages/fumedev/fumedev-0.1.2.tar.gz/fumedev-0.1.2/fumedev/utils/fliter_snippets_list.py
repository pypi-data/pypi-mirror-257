def filter_snippets_list(snippets, file_paths):
    return [snippet for snippet in snippets if snippet.get('file_path').replace('codebase/', '') in file_paths]