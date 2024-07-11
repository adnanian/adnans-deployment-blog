from config import app, db, api
from flask import send_from_directory
from flask_restful import Resource
from models import LanguageClassification, Language


class Index(Resource):
    """The first resource that a request is made to in production mode."""

    def get(self):
        """Renders the index.html document from the frontend.

        Returns:
            Response: the index.html document.
        """
        # print(f"The CWD at index call is: {os.getcwd()}", flush=True)
        return send_from_directory("../client/dist", "index.html")


api.add_resource(Index, "/", endpoint="index")

if __name__ == "__main__":
    app.run(port=5000, debug=True)
