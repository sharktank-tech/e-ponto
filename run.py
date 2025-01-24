from web import create_app
from web.modules.models import db
import os

os.environ["FLASK_APP"] = "run"
app = create_app()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port='8000')
