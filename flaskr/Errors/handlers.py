from flask import Blueprint, jsonify


errors = Blueprint('errors', __name__)


@errors.app_errorhandler(404)
def error_404(error):
    msg = messageHandler(error)
    return jsonify({
        'error': 404,
        'message': msg or 'Not Found',
        'success': False
    }), 404


@errors.app_errorhandler(400)
def error_400(error):
    msg = messageHandler(error)
    return jsonify({
        'error': 400,
        'message': msg or 'Bad Request',
        'success': False
    }), 400


@errors.app_errorhandler(405)
def error_405(error):
    msg = messageHandler(error)
    return jsonify({
        'error': 405,
        'message': msg or 'Method Not Allowed',
        'success': False
    }), 405


@errors.app_errorhandler(422)
def error_422(error):
    msg = messageHandler(error)
    return jsonify({
        'error': 422,
        'message': msg or 'Unprocessable',
        'success': False
    }), 422


@errors.app_errorhandler(500)
def error_500(error):
    msg = messageHandler(error)
    return jsonify({
        'error': 500,
        'message': msg or 'Something Went Wrong On Our Side',
        'success': False
    }), 500


def messageHandler(error):
    try:
        msg = str(error).split(':', 1)[1]
    except Exception as e:
        msg = None
        print(e)
    return msg
