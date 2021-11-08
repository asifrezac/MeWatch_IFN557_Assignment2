# this script runs our package
from mewatch import create_app

if __name__=='__main__':
    napp = create_app()
    napp.run(debug=True, port=2000) 