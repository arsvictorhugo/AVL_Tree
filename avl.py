import random
from graphviz import Digraph

class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1

class AVLTree:
    def insert(self, root, key):
        if not root:
            return Node(key)
        elif key < root.key:
            root.left = self.insert(root.left, key)
        else:
            root.right = self.insert(root.right, key)

        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))
        balance = self.get_balance(root)

        if balance > 1 and key < root.left.key:
            return self.rotate_right(root)
        if balance < -1 and key > root.right.key:
            return self.rotate_left(root)
        if balance > 1 and key > root.left.key:
            root.left = self.rotate_left(root.left)
            return self.rotate_right(root)
        if balance < -1 and key < root.right.key:
            root.right = self.rotate_right(root.right)
            return self.rotate_left(root)

        return root

    def delete(self, root, key):
        if not root:
            return root
        elif key < root.key:
            root.left = self.delete(root.left, key)
        elif key > root.key:
            root.right = self.delete(root.right, key)
        else:
            if not root.left:
                return root.right
            elif not root.right:
                return root.left
            temp = self.get_min_value_node(root.right)
            root.key = temp.key
            root.right = self.delete(root.right, temp.key)

        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))
        balance = self.get_balance(root)

        if balance > 1 and self.get_balance(root.left) >= 0:
            return self.rotate_right(root)
        if balance > 1 and self.get_balance(root.left) < 0:
            root.left = self.rotate_left(root.left)
            return self.rotate_right(root)
        if balance < -1 and self.get_balance(root.right) <= 0:
            return self.rotate_left(root)
        if balance < -1 and self.get_balance(root.right) > 0:
            root.right = self.rotate_right(root.right)
            return self.rotate_left(root)

        return root

    def rotate_left(self, z):
        y = z.right
        T2 = y.left
        y.left = z
        z.right = T2
        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        return y

    def rotate_right(self, z):
        y = z.left
        T3 = y.right
        y.right = z
        z.left = T3
        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        return y

    def get_height(self, node):
        return node.height if node else 0

    def get_balance(self, node):
        return self.get_height(node.left) - self.get_height(node.right) if node else 0

    def get_min_value_node(self, node):
        current = node
        while current.left:
            current = current.left
        return current

    def pre_order(self, root):
        if not root:
            return
        print(f"{root.key} ", end="")
        self.pre_order(root.left)
        self.pre_order(root.right)

    def gerar_grafico(self, root, filename="arvore_avl"):
        dot = Digraph()
        def adicionar_nos(node):
            if not node:
                return
            dot.node(str(id(node)), f"{node.key}")
            if node.left:
                dot.edge(str(id(node)), str(id(node.left)))
                adicionar_nos(node.left)
            if node.right:
                dot.edge(str(id(node)), str(id(node.right)))
                adicionar_nos(node.right)
        adicionar_nos(root)
        dot.render(filename, format='png', cleanup=True)
        print(f"Imagem gerada: {filename}.png")

# Interface aprimorada
def main():
    tree = AVLTree()
    root = None

    # Gera árvore inicial com 5 a 10 números aleatórios entre 1 e 100
    quantidade = random.randint(5, 10)
    numeros = random.sample(range(1, 100), quantidade)
    print(f"Gerando árvore inicial com os valores: {numeros}")
    for num in numeros:
        root = tree.insert(root, num)
    
    tree.gerar_grafico(root)

    while True:
        print("\n--- Árvore AVL ---")
        print("1. Inserir")
        print("2. Remover")
        print("3. Exibir (Pré-ordem)")
        print("4. Sair")
        op = input("Escolha: ")

        if op == "1":
            valor = int(input("Valor para inserir: "))
            root = tree.insert(root, valor)
            print("Valor inserido.")
            tree.gerar_grafico(root)
        elif op == "2":
            valor = int(input("Valor para remover: "))
            root = tree.delete(root, valor)
            print("Valor removido (se existia).")
            tree.gerar_grafico(root)
        elif op == "3":
            print("Pré-ordem: ", end="")
            tree.pre_order(root)
            print()
        elif op == "4":
            break
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    main()
