from bs4 import BeautifulSoup

aim = ['wangyi.html', 'domestic.html', 'world.html', 'tech.html', 'jiankang.html']
with open('html/tech.html', 'r') as f:
    s = BeautifulSoup(f, 'lxml')
    text = s.get_text()

x = s.body
print(type(x))
print(x)