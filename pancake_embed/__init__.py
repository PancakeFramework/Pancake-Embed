"""
Pancake Embed — 零 import 插件
将框架装饰器注册到 muffin_flour，配合 DoughMeta 实现自动注入。
DoughMeta 在用户定义 Dough 子类时，自动从 muffin_flour/muffin_water
注入已注册的名称到模块命名空间。
"""

import logging

from pancake.ovenware import InitAction

logger = logging.getLogger(__name__)


class Main(InitAction):
    """Embed 插件入口

    init_order=-10 确保最先加载，
    在用户代码加载前完成装饰器注册。
    """

    init_order = -10
    build_order = 0

    def check(self) -> bool:
        return True

    def build(self):
        """确保所有装饰器已注册到 muffin_flour"""
        # 触发 decorators 模块加载（会自动注册到 muffin_flour）
        import pancake.decorators  # noqa: F401
        # 触发 base 模块加载（会自动注册到 muffin_water）
        import pancake.base  # noqa: F401
        # 触发 factory 模块加载（会自动注册到 muffin_water）
        import pancake.factory  # noqa: F401

        from pancake.oven.muffin import muffin_flour, muffin_water
        logger.info(
            f"Embed: 已注册 {len(muffin_flour)} 个装饰器, "
            f"{len(muffin_water)} 个类"
        )
