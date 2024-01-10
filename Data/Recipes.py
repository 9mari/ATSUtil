import re


class Recipe:
    def __init__(self, id, required_resources, produced_materials, star_level):
        self.id = id
        self.required_resources = required_resources
        self.produced_materials = produced_materials
        self.star_level = star_level
        self.name = self.generate_name()

    def generate_name(self):
        # 假设每个配方只产生一种材料
        material_name = self.produced_materials[0]['material']
        return f"{self.star_level}星_{material_name}"


# 示例配方
recipes = [
    Recipe(
        id=1,
        required_resources=[
            {'resource': '木材', 'quantity': 8}
        ],
        produced_materials=[
            {'material': '木板', 'quantity': 2}
        ],
        star_level=0
    ),
    Recipe(
        id=2,
        required_resources=[
            {'resource': '植物纤维', 'quantity': 6},
            {'resource': '皮革', 'quantity': 6},
            {'resource': '芦苇', 'quantity': 6}
        ],
        produced_materials=[
            {'material': '织物', 'quantity': 2}
        ],
        star_level=0
    ),
    Recipe(
        id=3,
        required_resources=[
            {'resource': '粘土', 'quantity': 6},
            {'resource': '石头', 'quantity': 6}
        ],
        produced_materials=[
            {'material': '砖头', 'quantity': 2}
        ],
        star_level=0
    ),
    Recipe(
        id=4,
        required_resources=[
            {'resource': '根茎', 'quantity': 6},
            {'resource': '谷物', 'quantity': 6},
            {'resource': '蘑菇', 'quantity': 6},
            {'resource': '蔬菜', 'quantity': 6}
        ],
        produced_materials=[
            {'material': '成包的庄稼', 'quantity': 2}
        ],
        star_level=2
    ),
    # 更多配方...
]


# 通过 ID 查询 name
def get_name_by_id(recipe_id):
    for recipe in recipes:
        if recipe.id == recipe_id:
            return recipe.name
    return None  # 如果没有找到配方


# 通过 name 查询 ID
def get_id_by_name(recipe_name):
    for recipe in recipes:
        if recipe.name == recipe_name:
            return recipe.id
    return None  # 如果没有找到配方


def get_recipes_by_resource(resource):
    """根据提供的资源返回可用配方的ID列表"""
    available_recipe_ids = []
    for recipe in recipes:
        if any(resource == req['resource'] for req in recipe.required_resources):
            available_recipe_ids.append(recipe.id)
    return available_recipe_ids


def sort_names_by_star_and_number(recipe_ids):
    """根据配方ID列表，查询对应的名称，并按星级和名称中的数字排序"""
    # 获取名称
    names = [get_name_by_id(id) for id in recipe_ids]

    def parse_star_and_number(name):
        # 解析星级和名称中的数字
        match = re.search(r'(\d+)星_(.+)', name)
        if match:
            star = int(match.group(1))
            number = int(re.search(r'\d+', match.group(2)).group())
            return star, number
        return 0, 0  # 如果没有匹配到格式，则默认为0星，数字0

    # 根据星级和名称中的数字排序
    names.sort(key=parse_star_and_number, reverse=True)
    return names
