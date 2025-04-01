from service.nodes.textnode import TextNode
from service.utils.functions import copy_resources_recursively
from service.utils.functions import generate_pages_recursive
def main():
    source_path = "static"
    destination_path = "public"
    copy_resources_recursively(source_path, destination_path)
    generate_pages_recursive('content', 'template.html', destination_path)




if __name__ == "__main__":
    main()
