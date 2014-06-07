import collections
class acNode:
        def __init__(self,ch):
                self.char=ch
                self.transitions=[]
                self.results=[]
                self.fails=None

class searchTree:
        def __init__(self):
                self.root=None
                self.topics=[]
                self.pages=[]
        def add_topics(self,topic):
                self.topics.append(topic)
        def add_pages(self,page):
                self.pages.append(page)
        def make(self):
                root=acNode(None)
                root.fail=root
                queue=collections.deque([root])
		print self.topics
                for keyword in self.topics:
			current_node=root
                        for ch in keyword:
                                new_node=None
                                for transition in current_node.transitions:
                                        if transition.char==ch:
                                                new_node=transition
                                                break
                                if new_node is None:
                                        new_node=acNode(ch)
                                        current_node.transitions.append(new_node)
                                        if current_node is root:
                                                new_node.fail=root
                                current_node=new_node
                        current_node.results.append(keyword)
                while queue:
                        current_node=queue.popleft()
                        for node in current_node.transitions:
                                queue.append(node)
                                fail_state_node=current_node.fail
                                while not any(x for x in fail_state_node.transitions if node.char == x.char) and fail_state_node is not root:
                                        fail_state_node=fail_state_node.fail
                                node.fail=next((x for x in fail_state_node.transitions if node.char == x.char and x is not node ),root)
                self.root=root

        def search(self,text):
		self.hits=[]
                self.found_pages=[]
                currentNode=self.root
		for c in text:
                        trans=None
                        while trans==None:
                                for x in currentNode.transitions:
                                        if x.char==c:
                                                trans=x
                                if currentNode==self.root: break
                                if trans==None : currentNode=currentNode.fails
                        if trans!=None: currentNode=trans
                        for results in currentNode.results:
				self.hits.append(results)
                                self.found_pages.append(','.join(str(i) for i in self.pages[self.topics.index(results)] ))
