
import base64
from ..bl.text2image_bl import generate_storyboards, get_images_id
from ..bl.auth_svc.validate import token_required_bl
from ..helper.custom_response import CustomResponse
from flask import current_app
from flask import Blueprint, request, render_template_string

from ..database import db_session

from functools import wraps


text2image_blueprint = Blueprint('text2text', __name__)


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')

        if not token:
            return CustomResponse(succeeded=False, message='missing credentails!', status=401)

        result = token_required_bl(token)
        status = result['status']
        if status == 200:
            current_user = result['current_user']
            return f(current_user, *args, **kwargs)
        else:
            return CustomResponse(succeeded=False, message=result['message'], status=status)

    return decorated


@text2image_blueprint.route('/create_storyboards', methods=['POST'])
@token_required
def create_storyboards(current_user):
    if request.is_json:
        data = request.get_json()
    else:
        data = request.form
    result = generate_storyboards(data, db_session=db_session)
    data = result['data']
    return CustomResponse(succeeded=True, data=data, status=200)


def b64encode_filter(data):
    return base64.b64encode(data).decode('utf-8')


# Register the custom filter with Flask
current_app.jinja_env.filters['b64encode'] = b64encode_filter


@text2image_blueprint.route('/image/<ref_id>')
def get_image(ref_id):

    images_data = get_images_id(ref_id)
    # Retrieve the image file from GridFS

    # Render a template string with the images
    html_content = """
    <!doctype html>
    <html lang="en">
      <head>
        <meta charset="utf-8">
        <title>Images</title>
      </head>
      <body>
        {% for image in images %}
          {% if image.content %}
            <div>
              <h3>Image ID: {{ image.id }}</h3>
              <h3>Image Order: {{ image.filename }}</h3>
              <img src="data:image/jpeg;base64,{{ image.content | b64encode }}">
            </div>
          {% else %}
            <div>
              <h3>Image ID: {{ image.id }}</h3>
              <h3>Image Order: {{ image.filename }}</h3>
              <p>File not found</p>
            </div>
          {% endif %}
        {% endfor %}
      </body>
    </html>
    """
    return render_template_string(html_content, images=images_data)
