
import tornado.web
from tornado.ioloop import IOLoop
from tornado import gen 
import time

@gen.coroutine
def async_sleep(seconds):
    yield gen.Task(IOLoop.instance().add_timeout, time.time() + seconds)

class TestHandler(tornado.web.RequestHandler):
    @gen.coroutine
    def get(self):
        for i in range(100):
            print (i)
            yield async_sleep(1)
        self.write(str(i))
        self.finish()


application = tornado.web.Application([
    (r"/test", TestHandler),
    ])  

application.listen(9999)
IOLoop.instance().start()