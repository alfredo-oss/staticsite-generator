from service.nodes.textnode import TextNode
from service.utils.functions import copy_resources_recursively
def main():
    source_path = "static"
    destination_path = "public"
    copy_resources_recursively(source_path, destination_path)


if __name__ == "__main__":
    main()
