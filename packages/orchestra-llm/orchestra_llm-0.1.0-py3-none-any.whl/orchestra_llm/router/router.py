from orchestra_llm.core.schema import RouteSchema
import importlib

class Router:
    def __init__(self, **kwargs):
        self.route = []

    def add_route(self, path, composer, schema, name):
        module_name, _, class_name = composer.rpartition('.')
        module = importlib.import_module(module_name)
        composerClass = getattr(module, class_name)

        composer_instance = composerClass()

        composer = composer_instance.run()
        self.route.append(RouteSchema(path=path, composer=composer, input_schema=schema, name=name))

    def to_json(self):
        return [r.to_json() for r in self.route]

def include_urls(file_path, var):
    pass