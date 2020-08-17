
from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

#setup(ext_modules = cythonize(["auth/user_login.py"])) # 列表中是要加密的文件名
ext_modules = [
    Extension("baserepo",  ["repo/baserepo.py"]),
    Extension("productarticle",  ["repo/productarticle.py"]),
    Extension("form_productarticle",  ["repo/form_productarticle.py"]),
    Extension("form_blogarticle",  ["repo/form_blogarticle.py"]),
    Extension("user",  ["repo/user.py"]),
    Extension("blogarticle",  ["repo/blogarticle.py"]),
    Extension("form_base",  ["repo/form_base.py"]),
    Extension("blogcategory",  ["repo/blogcategory.py"]),
    Extension("sitearticle",  ["repo/sitearticle.py"]),
    Extension("form_sitearticle",  ["repo/form_sitearticle.py"]),
    Extension("form_blogcategory",  ["repo/form_blogcategory.py"]),
    Extension("form_user",  ["repo/form_user.py"])
#   ... all your modules that need be compiled ...
]

for e in ext_modules:
    e.cython_directives = {'language_level': "3"} #all are Python-3
    
setup(
    name = 'captain_repos',
    cmdclass = {'build_ext': build_ext},
    ext_modules = ext_modules
)
#command
#python3 encryption.py build_ext --inplace
