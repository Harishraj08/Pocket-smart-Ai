CATALOG={
"home":[
{"name":"Minimalist LED Ceiling Light","category":"lighting","platform":"IKEA","price":2499,"url":"https://www.ikea.com/"},
{"name":"Modern 3-Seater Sofa","category":"seating","platform":"Amazon","price":28999,"url":"https://www.amazon.in/"},
{"name":"Solid Wood Dining Table","category":"dining table","platform":"Amazon","price":17999,"url":"https://www.amazon.in/"},
{"name":"Contemporary Wall Art Set","category":"decor","platform":"Amazon","price":1999,"url":"https://www.amazon.in/"},
{"name":"Adjustable Ceiling Fan","category":"ceiling fan","platform":"Amazon","price":3299,"url":"https://www.amazon.in/"},
{"name":"Compact Kitchen Storage Unit","category":"storage","platform":"IKEA","price":7499,"url":"https://www.ikea.com/"},
{"name":"Accent Floor Lamp","category":"lighting","platform":"IKEA","price":3499,"url":"https://www.ikea.com/"}],
"party":[
{"name":"Vegetarian Catering Package","category":"catering","platform":"Swiggy","price":450,"url":"https://www.swiggy.com/"},
{"name":"Mixed Catering Package","category":"catering","platform":"Zomato","price":550,"url":"https://www.zomato.com/"},
{"name":"Basic Party Decoration Package","category":"decoration","platform":"Local Vendor","price":6500,"url":None},
{"name":"Premium Party Decoration Package","category":"decoration","platform":"Local Vendor","price":12000,"url":None},
{"name":"Budget Hotel Stay","category":"accommodation","platform":"OYO","price":1800,"url":"https://www.oyorooms.com/"},
{"name":"DJ / Entertainment Basic","category":"entertainment","platform":"Local Vendor","price":7000,"url":None}],
"jewelry":[
{"name":"Classic Gold-Tone Stud Earrings","category":"earrings","platform":"Amazon","price":1299,"url":"https://www.amazon.in/"},
{"name":"Pearl Drop Earrings","category":"earrings","platform":"Flipkart","price":1799,"url":"https://www.flipkart.com/"},
{"name":"Minimal Pendant Necklace","category":"necklace","platform":"Amazon","price":2499,"url":"https://www.amazon.in/"},
{"name":"Statement Necklace Set","category":"necklace","platform":"Flipkart","price":3499,"url":"https://www.flipkart.com/"},
{"name":"Slim Bracelet","category":"bracelet","platform":"Amazon","price":1599,"url":"https://www.amazon.in/"}]}
def get_catalog(planner): return [dict(x) for x in CATALOG[planner]]
