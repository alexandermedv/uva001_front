import os
import sys
import front_ex.config.settings
# создает объекты настроек в соотвествии с классом settings
# Указывается значение по умолчанию - 'Dev', либо берется из переменных окружения
APP_ENV = os.environ.get('APP_ENV', 'Develop')
_current = getattr(sys.modules['front_ex.config.settings'], '{0}Config'.format(APP_ENV))()
# записывает системные атрибуты в переменные текущей сессии
for atr in [f for f in dir(_current) if not '__' in f]:
   # environment can override anything
   val = os.environ.get(atr, getattr(_current, atr))
   setattr(sys.modules[__name__], atr, val)
   # print(os.environ.get('DEBUG'))
   # if os.environ.get('DEBUG') == 'True': 
   if APP_ENV == 'Develop': print(atr, val)
# def as_dict():
#    res = {}
#    for atr in [f for f in dir(config) if not '__' in f]:
#        val = getattr(config, atr)
#        res[atr] = val
#    return res