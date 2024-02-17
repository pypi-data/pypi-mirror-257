from concurrent.futures import ThreadPoolExecutor
import concurrent
import json
import os

from openai import OpenAI
from fumedev.env import relative_path
from fumedev import env

from fumedev.index.FolderGraph import FolderGraph
from fumedev.index.VectorStore import VectorStore
from fumedev.index.utils.get_emmbedding import get_embedding
from fumedev.index.utils.line_chunker import line_chunker
from fumedev.utils.filter_snippets_header import filter_snippets_header

class Documentation():
    def __init__(self, root_folder=relative_path('codebase')):
        self.snippet_docs = []
        self.root_folder = root_folder

        self.db = None
        self.index = {}
        self.vector_index = VectorStore(relative_path('snippets_index.idx'), 3072)
        self.embedded_snippets = []

    def document(self):
        
        if os.path.exists(relative_path('snippets_code.json')):
            os.remove(relative_path('./snippets_code.json'))

        if os.path.exists(relative_path('snippets_index.idx')):     
            self.vector_index.flush_index()

        fg = FolderGraph(root_folder=self.root_folder)
        files = fg.get_leaf_files()

        file_dict_list = []
        for file in files:
            file_dict_list.append(self.process_file(file))
                
                    
        self.vectorize_snippets(file_dict_list) 

    def process_file(self, file):
        try:
            snippets = line_chunker(file, 20)
        except:
            return
        
        for i,snippet in enumerate(snippets):
            snippets[i] = f'File Path: {file}\n\n{snippet}'

        file = {
            'file_path': file,
            'snippets': snippets
        }
        return file

    def save_snippet_code(self, file):
        file_path = file.get('file_path')
        snippets = file.get('snippets')

        for snippet in snippets:
            # Compute the document embedding
            doc_vec = get_embedding(snippet)

            embedded_snippet = {
                'code': snippet,
                'file_path': file_path,
                'embedding': doc_vec
            }
            self.embedded_snippets.append(embedded_snippet)
        
    def search_code(self, query, k=5, extension=None, iteration=1):
        
        q = get_embedding(query)
        vs = self.vector_index
        distances, indices = vs.search_vectors(query_vectors=q, k=k*iteration)
        distances = distances[0]
        indices = indices[0]
        with open(relative_path('snippets_code.json'), 'r') as file:
            snippets_data = json.load(file)
            if not extension:
                return filter_snippets_header([snippets_data[f"{indices[i]}"] for i in range(k)])
            elif k*iteration > 1000:
               res = [snippets_data[f"{indices[i]}"] for i in range(k*iteration)]
               correct = [snip for snip in res if snip.get('file_path').split('.')[-1] == extension] 

               return filter_snippets_header(correct)
            else:
                res = [snippets_data[f"{indices[i]}"] for i in range(k*iteration)]
                correct = [snip for snip in res if snip.get('file_path').split('.')[-1] == extension]

                if len(correct) < k:
                    return self.search_code(query=query, k=k, extension=extension, iteration=iteration+1)
                else:
                    return filter_snippets_header(correct)
        

    def get_relevant_codes(self, query, k=5, extension=None):
        docs = self.search_code(query=query, k=k, extension=extension)
        res = []
        for doc in docs:
            snippet = doc.get('code')
            file_path = doc.get('file_path')
            res.append({'snippet': snippet, 'file_path': file_path})

        return res

    def vectorize_snippets(self, files):
        with ThreadPoolExecutor(max_workers=15) as executor:  # Adjust max_workers as needed
            future_to_snippet = {executor.submit(self.save_snippet_code, file): file for file in files}
            for future in concurrent.futures.as_completed(future_to_snippet):
                file = future_to_snippet[future]
                try:
                    data = future.result()
                except Exception as exc:
                    print(f'Sorry, bumbed in to a mistake indexing file: {file.get("file_path")} \n {exc}')


        for snippet in self.embedded_snippets:
            idx = self.vector_index.add_vectors(snippet.get('embedding'))

            self.index[idx] = {
            'code': snippet.get('code'),
            'file_path': snippet.get('file_path')  
            }  # No need to convert to list
             
        json_file_path = relative_path('snippets_code.json')
        with open(json_file_path, 'w') as file:
            json.dump(self.index, file)

        
        self.vector_index.save_index_to_disk()        
        json_file_path = relative_path('snippets_code.json')
        with open(json_file_path, 'w') as file:
            json.dump(self.index, file)

        
        self.vector_index.save_index_to_disk()

