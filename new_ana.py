from bs4 import BeautifulSoup
with open('new.html', 'r', encoding='utf8') as f:
    html = f.read()
soup = BeautifulSoup(html, 'lxml')
h1 = soup.find('h1')
print(h1)
x = soup.body.find(class_="post_content post_area clearfix")
#print(x)
y = x.find(id="epContentLeft")

y = y.find(class_="post_body")
y = y.find(id="endText")
y = y.find_all('p')
with open('y.html', 'w', encoding='utf8') as f:
    for s in y[2:]:
        s = s.prettify()
        f.write(s)