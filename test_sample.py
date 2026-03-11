class TreeNode:
    def __init__(self, val=0):
        self.val = val
        self.left = None
        self.right = None

class Solution:
    def construct_bst(self, preorder):
        self.index = 0

        def build(min_val, max_val):
            if self.index == len(preorder):
                return None

            val = preorder[self.index]

            if val <= min_val or val >= max_val:
                return None

            root = TreeNode(val)
            self.index += 1

            root.left = build(min_val, val)
            root.right = build(val, max_val)

            return root

        return build(float('-inf'), float('inf'))