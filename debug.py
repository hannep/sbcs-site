from sbcswebsite.application import app

app.config.from_object('sbcswebsite.default_settings')
app.run()