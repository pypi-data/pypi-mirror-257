import hehd


doc = hehd.doc()
doc.titles.append("Hello World")
doc.html.body.create().tag().div("Hello World")
x = hehd.nodes.comment(doc.html.body.create().tag().div(), "Hello World2")
output = doc.output()
print(output)
