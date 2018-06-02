class Product:

    def __init__(self):
        self.asin = None
        self.price = None
        self.also_bought = []
        self.sales_rank = None
        self.categories = []

    def set_attributes(self, line):
        for key, value in line.items():
            {
                'asin': self.extract_asin,
                'related': self.extract_bought_items,
                'price': self.extract_price,
                'salesRank': self.extract_sales_rank,
                'categories': self.extract_categories
            }[key](value)

    def extract_asin(self, asin):
        self.asin = asin
    
    def extract_bought_items(self, related):
        if related.get('also_bought'):
            self.also_bought = related['also_bought']
    
    def extract_price(self, price):
        self.price = price
    
    def extract_sales_rank(self, sales_rank):
        self.sales_rank = sales_rank
    
    def extract_categories(self, categories):
        self.categories = categories[0]
