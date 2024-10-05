from app import create_app
import os
app = create_app()

if __name__ == '__main__':
    print(os.environ.get('PORT'))
    app.run(debug=False, port=os.environ.get('PORT', 10000))
