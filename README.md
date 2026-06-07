# Pancake Embed

> 零 import 插件 — 配合 DoughMeta 实现框架 API 自动注入

## 工作原理

1. **Embed 插件**加载时（`init_order=-10`，最先执行），将装饰器注册到 `muffin_flour`
2. 用户定义 `Dough` 子类时，**DoughMeta** 自动从 `muffin_flour`/`muffin_water` 注入已注册的名称到模块命名空间
3. 用户代码无需 `import` 即可使用所有装饰器和基类

```python
from pancake.dough import Dough

# 定义子类后，Singleton、Service、DoughFactory 等自动可用
@Singleton
class UserService(Service):
    async def on_init(self):
        self.db = DoughFactory.get().resolve("DatabaseService")
```

## 注册的名称

### 装饰器 (muffin_flour)
- `@Singleton` / `@Prototype` / `@Lazy` — 作用域
- `@DoughDecorator` — 标记类为 Bean
- `@DependsOn("A", "B")` — 声明依赖
- `@Import(Cls)` — 自动注册外部类
- `@Maker` / `@noMaker` — 控制方法 Bean 注册
- `@inject` — 自动注入依赖
- `@Config` — 从配置注入字段

### 基类 (muffin_water)
- `Configuration` — 配置类
- `Service` — 服务类
- `Function` — 方法类
- `Struct` — 数据结构类
- `DoughFactory` — Bean 工厂

## 安装

```bash
pip install pancake-embed
```

或在 `pancake.xml` 中添加：

```xml
<dependency>
    <groupId>io.pancake</groupId>
    <artifactId>embed</artifactId>
</dependency>
```

## 开源协议

MIT
