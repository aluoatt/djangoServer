from flask import Flask, send_from_directory, request, jsonify
from flask_classful import FlaskView, route
from version import server_version
from serverControlV1 import ServerControlV1
from loggerSetting import _logging
import os

logger = _logging(filename='./logs/event.log')
app = Flask(__name__)
app.config.update(dict(DEBUG=False))

os.makedirs("./personalData", exist_ok=True)


@app.route("/")
def index():
    "server status"
    return "file server backend is ready version:{}".format(server_version)


class V1View(FlaskView):
    def __init__(self):
        super(V1View, self).__init__()
        self.api = ServerControlV1(logger)

    @route('/getFile', methods=["POST"])
    def getFile(self):
        if request.method == 'POST':
            fileId = request.form.get('fileId', False)
            userName = request.form.get('userName', False)
            FileType = request.form.get('FileType', "PDF")
            if not fileId:
                return jsonify({"status": "fail", "message": "loss parameter fileId"})

            if not userName:
                return jsonify({"status": "fail", "message": "loss parameter userName"})

            resultFilePath = self.api.getFileWithWaterMark(fileId, userName, FileType=FileType)
            return resultFilePath
            # return send_from_directory(resultFilePath, fileId + '_' + userName, as_attachment=True)


V1View.register(app)

if __name__ == '__main__':
    logger.info("start server")
    app.run(host='127.0.0.1', port=15010, threaded=True)
