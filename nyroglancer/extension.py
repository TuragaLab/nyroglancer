from notebook.base.handlers import IPythonHandler
import chunk_worker_bundle_js
import main_bundle_js
import ndstore
import neuroglancer_css

class Viewer(IPythonHandler):

    def get(self):
        self.finish("""
<!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF-8">
    <title>neuroglancer</title>
    <link rel="stylesheet" type="text/css" href="../css/neuroglancer.css" />
  </head>
  <body>
    <div id="container" style="width:100%;height:1024px;background:black"></div>
    <script type="text/javascript" src="../js/neuroglancer/main.bundle.js"></script>
  </body>
</html>
        """)

class MainBundle(IPythonHandler):
    def get(self):
        self.write(main_bundle_js.content)
        self.set_header("Content-Type", "application/javascript")

class ChunkWorkerBundle(IPythonHandler):
    def get(self):
        self.write(chunk_worker_bundle_js.content)
        self.set_header("Content-Type", "application/javascript")

class NeuroglancerCss(IPythonHandler):
    def get(self):
        self.write(neuroglancer_css.content)
        self.set_header("Content-Type", "text/css")

def load_jupyter_server_extension(nb_server_app):

    web_app = nb_server_app.web_app
    host_pattern = '.*$'

    web_app.add_handlers(host_pattern, [('/ocp/ca/([^\/]*)/info', ndstore.Info)])
    web_app.add_handlers(host_pattern, [('/ocp/ca/([^\/]*)/image/jpeg/([0-9]*)/([0-9]*),([0-9]*)/([0-9]*),([0-9]*)/([0-9]*),([0-9]*)/neariso', ndstore.Image)])
    web_app.add_handlers(host_pattern, [('/ocp/ca/([^\/]*)/segmentation/npz/([0-9]*)/([0-9]*),([0-9]*)/([0-9]*),([0-9]*)/([0-9]*),([0-9]*)/neariso', ndstore.Segmentation)])
    web_app.add_handlers(host_pattern, [('/viewer', Viewer)])
    web_app.add_handlers(host_pattern, [('/js/neuroglancer/main.bundle.js', MainBundle)])
    web_app.add_handlers(host_pattern, [('/js/neuroglancer/chunk.worker.bundle.js', ChunkWorkerBundle)])
    web_app.add_handlers(host_pattern, [('/css/neuroglancer.css', NeuroglancerCss)])

    print "nyroglancer extension loaded"
