"""
Pancake Embed — 零 import 插件
将框架装饰器、基类、核心 API 注入 builtins，
用户代码无需显式 import 即可使用。
"""

import builtins
import logging

from pancake.ovenware import InitAction

logger = logging.getLogger(__name__)


def _patch_dough_meta():
    """Patch DoughMeta，使所有新定义的 Dough 子类自动注入 builtins"""
    from pancake.dough import DoughMeta

    original_new = DoughMeta.__new__

    def patched_new(mcs, name, bases, namespace):
        cls = original_new(mcs, name, bases, namespace)

        if name == "Dough" or namespace.get("_no_register", False):
            return cls

        if name not in builtins.__dict__:
            builtins.__dict__[name] = cls

        return cls

    DoughMeta.__new__ = patched_new


def _patch_register_decorator():
    """Patch register_decorator，使后续注册的装饰器自动注入 builtins"""
    import pancake.registry as registry_module

    original = registry_module.register_decorator

    def patched(name, decorator):
        original(name, decorator)
        if name not in builtins.__dict__:
            builtins.__dict__[name] = decorator

    registry_module.register_decorator = patched


class Main(InitAction):
    """Embed 插件入口

    init_order=999 最后加载，确保所有其他插件已注册完毕。
    在 __init__ 中完成 builtins 注入（load_ovenware 阶段，早于 load_dish）。
    """

    init_order = 999
    build_order = 0

    def __init__(self):
        from pancake.registry import (
            flour, water, egg, sugar,
            get_all_classes, get_all_decorators,
        )

        # 确保框架模块已导入，注册表已填充
        import pancake.decorators  # noqa: F401
        import pancake.base  # noqa: F401
        import pancake.factory  # noqa: F401

        count = 0

        def _inject(source: dict):
            nonlocal count
            for name, obj in source.items():
                if name not in builtins.__dict__:
                    builtins.__dict__[name] = obj
                    count += 1

        # 注入框架 API
        _inject(flour)
        _inject(water)
        _inject(egg)
        _inject(sugar)

        # 注入 ovenware 插件注册的装饰器（如 broker 的 event_node、on_event）
        _inject(get_all_decorators())

        # 注入已注册的 Dough 子类
        _inject(get_all_classes())

        # Patch 元类和注册函数，后续新增的类/装饰器自动注入 builtins
        _patch_dough_meta()
        _patch_register_decorator()

        logger.info(f"Embed: 已注入 {count} 个名称到 builtins")

    def check(self) -> bool:
        return True

    def build(self):
        pass
