from flaskpress import app

@app.template_filter('datetime')
def datetime_format(value, format='%H:%M / %d-%m-%Y'):
  return value.strftime(format)

@app.template_filter('date')
def date_format(value):
  return datetime_format(value, format='%d-%m-%Y')
