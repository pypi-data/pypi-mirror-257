class Parameters:
    def __init__(self, RecipeName, RecipeRevision):
        self.recipe_name = RecipeName
        self.recipe_revision = RecipeRevision

    def to_dict(self):
        return vars(self)
