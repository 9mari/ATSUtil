from pywebio.output import put_text, put_markdown, put_buttons, clear, put_column
from pywebio.session import set_env
from Data.Resources import *
from Data.Recipes import get_recipes_by_resource, sort_names_by_star_and_number, get_name_by_id  # 导入我们之前创建的函数


def multi_select_buttons():
    options = [resource.value for resource in Resources]  # 遍历枚举类获取选项
    selected = set()

    def update_buttons():
        clear()  # 清除当前输出
        put_markdown("### 已选择的资源")
        if selected:
            put_text(', '.join(selected))
        else:
            put_text('尚未选择任何资源')

        put_markdown("### 可选择的资源")
        buttons = [
            dict(label=option, value=option, color='primary' if option in selected else 'light')
            for option in options
        ]
        put_buttons(buttons, onclick=lambda btn: button_click(btn))

        # 添加一个新按钮用于处理资源选择
        put_buttons(['查询配方'], onclick=lambda btn: show_recipes())

    def button_click(btn):
        if btn in selected:
            selected.remove(btn)
        else:
            selected.add(btn)
        update_buttons()

    def show_recipes():
        recipe_set = set()
        for res in selected:
            matched_recipes = get_recipes_by_resource(res)  # 根据选择的资源查询配方
            for recipe in matched_recipes:
                recipe_set.add(recipe)  # 添加到集合中，自动去除重复的配方

        display_recipes(recipe_set)

    def display_recipes(recipe_ids):
        put_markdown("### 查询到的配方")
        names = []
        for recipe_id in recipe_ids:
            name = get_name_by_id(recipe_id)
            names.append(name)

        # 排序逻辑：根据星级降序排序
        def extract_star_level(recipe_name):
            # 假设名称格式为 "3星_木板"
            star_level = recipe_name.split('_')[0]
            # 提取星级数字
            return int(star_level[0])

        # 使用自定义排序函数
        names.sort(key=extract_star_level, reverse=True)

        for name in names:
            put_text(name)  # 显示配方名字

    update_buttons()
    put_text("点击按钮进行选择。")


if __name__ == '__main__':
    set_env(auto_scroll_bottom=True)
    multi_select_buttons()
