from service.nodes import TextNode

def main():
    new_node = TextNode("This is a text node", "bold", "https://www.boot.dev")
    print(new_node)

if __name__ == "__main__":
    main()
