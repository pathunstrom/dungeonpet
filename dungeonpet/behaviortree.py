from typing import Any, Hashable

FAILURE = 0
RUNNING = 1
SUCCESS = 2


class Blackboard(object):

    def __init__(self):
        self._base_memory = {}
        self._tree_memory = {}

    def _get_tree_memory(self, tree_id: int):
        if self._tree_memory.get(tree_id) is None:
            self._tree_memory[tree_id] = {'node_memory': {},
                                          'open_nodes': []}
        return self._tree_memory[tree_id]

    @staticmethod
    def _get_node_memory(tree_memory: dict, node_id: int):
        memory = tree_memory['node_memory']
        if memory.get(node_id) is None:
            memory[node_id] = {}
        return memory[node_id]

    def _get_memory(self, tree_id: int=None, node_id: int=None):
        memory = self._base_memory
        if tree_id is not None:
            memory = self._get_tree_memory(tree_id)
            if node_id is not None:
                memory = self._get_node_memory(memory, node_id)
        return memory

    def set(self, key: Hashable,
            value: Any,
            tree_id: int=None,
            node_id: int=None):
        memory = self._get_memory(tree_id, node_id)
        memory[key] = value

    def get(self, key: Hashable, tree_id: int=None, node_id: int=None):
        memory = self._get_memory(tree_id, node_id)
        return memory[key]

    def update_open_nodes(self, tree_id: int, tick: Tick):
        previously_opened = self.get("open_nodes", tree_id)
        currently_opened = tick.open_nodes

        start = None
        for i, (p, c) in enumerate(zip(previously_opened, currently_opened)):
            if p != c:
                start = i + 1
                break

        if start is not None:
            for node in previously_opened[start:0:-1]:
                node.close(tick)

        self.set("open_nodes", currently_opened, tree_id)


class Tick(object):

    def __init__(self, target: Any, blackboard: Blackboard, tree: BehaviorTree):
        self.tree = tree
        self.open_nodes = []
        self.debug = None
        self.target = target
        self.blackboard = blackboard

    def enter_node(self, node):
        self.open_nodes.append(node)

    def open_node(self, node):
        self.blackboard.set("open", True, id(self.tree), id(node))

    def tick_node(self, node):
        pass

    def close_node(self, node):
        self.blackboard.set("open", False, id(self.tree), id(node))
        self.open_nodes.pop()

    def exit_node(self, node: BaseNode):
        pass


class BehaviorTree(object):

    def __init__(self):
        self.root = None

    def tick(self, target, blackboard: Blackboard):
        tick = Tick(target, blackboard, self)
        self.root.execute(tick)
        blackboard.update_open_nodes(id(self), tick)


class BaseNode(object):

    def __init__(self, children: list):
        self.children = children

    def execute(self, tick: Tick):
        self._enter(tick)

        if not tick.blackboard.get("open", id(tick.tree), id(self)):
            self._open(tick)

        status = self._tick(tick)

        if status != RUNNING:
            self._close(tick)

        self._exit(tick)

        return status

    def enter(self, tick: Tick):
        pass

    def _enter(self, tick: Tick):
        tick.enter_node(self)
        self.enter(tick)

    def open(self, tick: Tick):
        pass

    def _open(self, tick: Tick):
        tick.open_node(self)
        self.open(tick)

    def tick(self, tick: Tick) -> int:
        pass

    def _tick(self, tick: Tick):
        tick.tick_node(self)
        return self.tick(tick)

    def close(self, tick: Tick):
        pass

    def _close(self, tick: Tick):
        tick.close_node(self)
        self.close(tick)

    def exit(self, tick: Tick):
        pass

    def _exit(self, tick: Tick):
        tick.exit_node(self)
        self.exit(tick)


class Sequence(BaseNode):

    def tick(self, tick: Tick):
        for child in self.children:
            status = child.execute(tick)

            if status != SUCCESS:
                return status
        return SUCCESS


class Priority(BaseNode):

    def tick(self, tick: Tick):
        for child in self.children:
            status = child.execute(tick)

            if status != FAILURE:
                return status

        return FAILURE


class MemSequence(BaseNode):

    def open(self, tick: Tick):
        tick.blackboard.set("running_child", 0, id(tick.tree), id(self))

    def tick(self, tick: Tick):

        current_child = tick.blackboard.get("running_child",
                                            id(tick.tree),
                                            id(self))

        for index, child in enumerate(self.children[current_child:]):

            status = child.execute(tick)

            if status != SUCCESS:
                if status == RUNNING:
                    tick.blackboard.set("running_child",
                                        current_child + index,
                                        id(tick.tree),
                                        id(self))
                return status

        return SUCCESS


class MemPriority(BaseNode):

    def open(self, tick: Tick):
        tick.blackboard.set('running_child', 0, id(tick.tree), id(self))

    def tick(self, tick: Tick):
        current_child = tick.blackboard.get('running_child',
                                            id(tick.tree),
                                            id(self))
        for index, child in enumerate(self.children[current_child:]):
            status = child.execute(tick)

            if status != FAILURE:
                if status == RUNNING:
                    tick.blackboard.set('running_child',
                                        current_child + index,
                                        id(tick.tree),
                                        id(self))
                return status
        return FAILURE
