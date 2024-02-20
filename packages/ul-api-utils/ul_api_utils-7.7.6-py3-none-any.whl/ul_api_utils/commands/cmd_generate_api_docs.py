import argparse
import ast
import importlib
import inspect
import os
import logging
from datetime import datetime
from typing import Dict, Callable, Any

from flask import url_for, Flask
from ul_py_tool.commands.cmd import Cmd


logger = logging.getLogger(__name__)


class CmdGenApiFunctionDocumentation(Cmd):
    api_dir: str
    db_dir: str

    @staticmethod
    def add_parser_args(parser: argparse.ArgumentParser) -> None:
        parser.add_argument('--api-dir', dest='api_dir', type=str, required=True)
        parser.add_argument('--db-dir', dest='db_dir', type=str, required=True)

    @property
    def api_module(self) -> str:
        return self.api_dir.replace('/', '.')

    @property
    def main_module(self) -> str:
        return self.api_dir.replace('/', '.') + ".main"

    @staticmethod
    def get_db_helpers_names(directory: str) -> Dict[str, Callable[..., Any]]:
        db_helpers = {}
        for root, _dirs, files in os.walk(directory):
            for file in files:
                if file.endswith('.py'):
                    module_name = file[:-3]  # Strip the .py to get the module name.
                    module_path = os.path.join(root, file)
                    spec = importlib.util.spec_from_file_location(module_name, module_path)
                    module = importlib.util.module_from_spec(spec)  # type: ignore
                    spec.loader.exec_module(module)  # type: ignore

                    functions = inspect.getmembers(module, inspect.isfunction)
                    for name, func in functions:
                        db_helpers[name] = func
        return db_helpers

    @staticmethod
    def get_flask_app(api_sdk_module: str) -> Flask:
        module = importlib.import_module(api_sdk_module)
        return module.sdk._flask_app

    def run(self) -> None:
        current_app = self.get_flask_app(self.main_module)
        db_helpers = self.get_db_helpers_names(self.db_dir)
        utils = self.get_db_helpers_names(f'{self.api_dir}/utils')
        db_utils = self.get_db_helpers_names(f'{self.db_dir}/utils')
        with current_app.app_context():
            current_app.config['SERVER_NAME'] = '{base_url}'
        with current_app.app_context(), open(f'.tmp/api_doc_{datetime.now().isoformat()}.md', 'w') as file:
            for api_num, rule in enumerate(current_app.url_map.iter_rules()):
                options = {}
                for arg in rule.arguments:
                    options[arg] = "[{0}]".format(arg)
                methods = ','.join([method for method in rule.methods if method not in ('HEAD', 'OPTIONS')])  # type: ignore
                url = url_for(rule.endpoint, **options).replace('%5B', '[').replace('%5D', ']')
                func_obj = current_app.view_functions[rule.endpoint]
                if not func_obj.__module__.startswith(self.api_module):
                    continue
                func_name = func_obj.__name__
                source = inspect.getsource(func_obj)
                tree = ast.parse(source)
                calls = []
                for node in ast.walk(tree):
                    if isinstance(node, ast.Call):
                        if isinstance(node.func, ast.Name):
                            calls.append(node.func.id)
                        elif isinstance(node.func, ast.Attribute):
                            calls.append(node.func.attr)
                        else:
                            pass

                docstring = inspect.getdoc(func_obj)
                api_docstring = 'None' if docstring is None else docstring

                file.write(f"## {api_num} Путь апи {url}\n\n")
                file.write(f"####  Имя функции апи: {func_name}\n")
                file.write(f"### Апи методы: {methods}\n\n")
                file.write("**Описание апи метода:** \n\n")
                file.write(f"```python\n{api_docstring}\n```\n")
                helper_call = 1
                for call in calls:
                    if call not in ('transaction_commit', 'and_', 'or_', 'foreign', 'query_soft_delete', 'ensure_db_object_exists', 'db_search'):
                        if call in db_helpers:
                            helper_func_obj = db_helpers[call]
                            helper_docstring = inspect.getdoc(helper_func_obj)
                            helper_docstring = 'None' if helper_docstring is None else helper_docstring

                            file.write(f"### {api_num}.{helper_call} Вызвана функция работы с БД : {call}\n")
                            file.write(f"**Описание функции {call}:**\n\n")
                            file.write(f"```python\n{helper_docstring}\n```\n")
                            helper_call += 1
                        elif call in utils:
                            util_func_obj = utils[call]
                            util_docstring = inspect.getdoc(util_func_obj)
                            util_docstring = 'None' if util_docstring is None else util_docstring
                            if 'db_tables_used' in util_docstring or 'db_table_used' in util_docstring:
                                file.write(f"### {api_num}.{helper_call} Вызвана функция работы с БД : {call}\n")
                                file.write(f"**Описание функции {call}:**\n\n")
                                file.write(f"```python\n{util_docstring}\n```\n")
                                helper_call += 1
                        elif call in db_utils:
                            util_func_obj = db_utils[call]
                            db_util_docstring = inspect.getdoc(util_func_obj)
                            db_util_docstring = 'None' if db_util_docstring is None else db_util_docstring
                            if 'db_tables_used' in db_util_docstring or 'db_table_used' in db_util_docstring:
                                file.write(f"### {api_num}.{helper_call} Вызвана функция работы с БД : {call}\n")
                                file.write(f"**Описание функции {call}:**\n\n")
                                file.write(f"```python\n{db_util_docstring}\n```\n")
                                helper_call += 1
                file.write('-' * 20)
                file.write('\n\n')
                file.write('\n\n')
