"""Generic resource to create, read, update, delete, and search YetiObjects."""

from flask import request
from webargs.flaskparser import parser
from flask_classful import FlaskView, route

from yeti.core.errors import GenericYetiError, ValidationError
from ..helpers import as_json, get_object_or_404


@parser.error_handler
def handle_args(err, unused_response, unused_schema):
    raise ValidationError(err.messages)

class GenericResource(FlaskView):
    """Class describing resources to manipulate objects."""

    route_base = None
    resource_object = None
    searchargs = None
    fulltext_searchargs = None

    @as_json
    def index(self):
        """Return a list of all objects in the database."""
        return self.resource_object.list()

    @as_json
    def get(self, id):  # pylint: disable=redefined-builtin
        """Fetch a single object from the database.

        Args:
            id: The object's primary ID.

        Returns:
            A JSON representation of the requested object, or a 404 HTTP
            status code if the object cannot be found.
        """
        return get_object_or_404(self.resource_object, id)

    @as_json
    def delete(self, id):
        """Deletes a single object from the database.

        Args:
          id: The object's ID.
        """
        return get_object_or_404(self.resource_object, id).delete()

    @route('/', methods=['POST'])
    @as_json
    def post(self):
        """Creates a new object.

        Returns:
            A JSON representation of the saved object.
        """
        try:
            return self.resource_object.load(request.json).save()
        except GenericYetiError as err:
            return err, 400

    @as_json
    @route('/<id>/', methods=['PUT'])
    def put(self, id):  # pylint: disable=redefined-builtin
        """Updates a given object.

        Args:
            id: The object's primary ID.

        Returns:
            A JSON representation of the requested object, or a 404 HTTP
            status code if the object cannot be found.
        """
        try:
            obj = get_object_or_404(self.resource_object, id)
            dumped = obj.dump()
            dumped.update(request.get_json())
            return self.resource_object.load(dumped).save()
        except GenericYetiError as err:
            return err, 400

    @route('/filter/', methods=['POST'])
    @as_json
    def filter(self):
        """Search the database for object with specific fields."""
        try:
            args = parser.parse(self.searchargs, request)
            return self.resource_object.filter(args)
        except ValidationError as err:
            return err, 400

    @route('/filter/fulltext/', methods=['POST'])
    @as_json
    def filter_fulltext(self):
        """Fulltext search on the database."""
        try:
            args = parser.parse(self.fulltext_searchargs, request)
            return self.resource_object.fulltext_filter(args['keywords'])
        except ValidationError as err:
            return err, 400
