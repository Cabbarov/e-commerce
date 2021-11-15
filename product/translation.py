from modeltranslation.translator import translator, TranslationOptions

from product.models import Category

class CategoryTranslationOptions(TranslationOptions):
    fields = ('title', 'parent_cat')
    

translator.register(Category,CategoryTranslationOptions)
