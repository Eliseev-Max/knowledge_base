#-*- coding: utf-8 -*-
class MyClass:
    def __init__(self, x):
        self.__privateVar = x
    def set_var(self, x):           # Изменяем значение
        self.__privateVar = x
    def get_var(self):              # Получаем значение
        return self.__privateVar
c = MyClass(10)
print("Значение, переданное экземпляру класса: ", c.get_var())
c.set_var(20)           # Изменяем значение с помощью созданного метода
print("Новое значение: ", c.get_var())
try:
    print(c.__privateVar)
except AttributeError as msg:
    print("Мы пытались вызвать атрибут __privateVar напрямую, через экземпляр класса, и вот что получилось\n", msg)
### Меняем значение псевдочастного атрибута особо хитрым способом
c._MyClass__privateVar = 50
print("Изменили значение атрибута не через set_var()\nMyClass.__privateVar = ", c.get_var())

### Использование атрибута __slots__
class WithSlots:
    __slots__ = ["x", "y"]      # Указываем атрибуты, разрешённые для экземпляров класса
    def __init__(self, a, b):
        self.x, self.y = a, b
        self.z = self.x*self.y
del c
c = WithSlots(10,20)
print(c.x, c.y)
c.x = 123
c.y = 321
print("Новые значения атрибутов: ", c.x, c.y)
try:
    c.z = 50; print(c.z)
except AttributeError as msg:
    print("Ошибка: ", msg)
