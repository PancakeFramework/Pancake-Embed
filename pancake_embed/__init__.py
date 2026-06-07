"""
Pancake Embed — 零 import 插件
将框架装饰器、基类、核心 API 注入 builtins，
用户代码无需显式 import 即可使用。
"""

import builtins
import logging

from pancake.ovenware import InitAction

logger = logging.getLogger(__name__)


class Main(InitAction):
    """Embed 插件入口

    init_order=-10 确保最先加载，
    在用户代码加载前完成 builtins 注入。
    """

    init_order = -10
    build_order = 0

    def check(self) -> bool:
        return True

    def build(self):
        """将框架 API 注入 builtins"""
        from pancake.oven.muffin import muffin_flour, muffin_water

        # 触发模块加载，确保注册表填充
        import pancake.decorators  # noqa: F401
        import pancake.base  # noqa: F401
        import pancake.factory  # noqa: F401
        import pancake.registry  # noqa: F401

        count = 0
        for name, obj in muffin_flour.items():
            if name not in builtins.__dict__:
                builtins.__dict__[name] = obj
                count += 1
        for name, obj in muffin_water.items():
            if name not in builtins.__dict__:
                builtins.__dict__[name] = obj
                count += 1

        logger.info(f"Embed: 已注入 {count} 个名称到 builtins")
