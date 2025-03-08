import chromadb

class Memory:
    
    def __init__(self):
        self.client = chromadb.Client()
        self.collection = self.client.get_or_create_collection("memories")
        self.memoryIndex = 0

    def get_relevant_memories(self, prompt):
        return ""
    
    # memory is a list of strings
    def UpdateMemory(self, memoryUpdates):
        documents = []
        metadatas = []
        memoryIDs = []

        for k, v in memoryUpdates.items():
            documents.append(v)
            metadatas.append({"tag" : k})
            memoryIDs.append(str(self.memoryIndex) + "." + k)
        self.memoryIndex += 1
        self.collection.add(documents=documents,
                            ids=memoryIDs,
                            metadatas=metadatas)

    def queryMemories(self, query):
        return self.collection.query(query_texts=query, n_results=10)
