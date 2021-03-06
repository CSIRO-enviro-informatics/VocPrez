import logging
import _config as config
from flask import Flask, g
from controller import routes
import helper
import data.source as source
import os
import pickle
import time

app = Flask(__name__, template_folder=config.TEMPLATES_DIR, static_folder=config.STATIC_DIR)

app.register_blueprint(routes.routes)

if hasattr(config, 'VOCAB_CACHE_DAYS'):
    cache_seconds = config.VOCAB_CACHE_DAYS * 86400
else:
    cache_seconds = 0

if os.path.isfile(config.VOCAB_CACHE_PATH):
    # if the VOCABS.pickle file is older than VOCAB_CACHE_DAYS days, delete it
    vocab_file_creation_time = os.stat(config.VOCAB_CACHE_PATH).st_mtime
    # if the VOCABS.pickle file is older than VOCAB_CACHE_DAYS days, delete it
    if vocab_file_creation_time < time.time() - cache_seconds:
        os.remove(config.VOCAB_CACHE_PATH)
    
@app.before_request
def before_request():
    """
    Runs before every request and populates vocab index either from disk (VOCABS.p) or from a complete reload by
    calling collect() for each of the vocab sources defined in config/__init__.py -> VOCAB_SOURCES
    :return: nothing
    """
    # check to see if g.VOCABS exists, if so, do nothing
    if hasattr(g, 'VOCABS'):
        return
    

    # we have no g.VOCABS so try and load it from a pickled VOCABS.p file
    if os.path.isfile(config.VOCAB_CACHE_PATH):
        try:
            with open(config.VOCAB_CACHE_PATH, 'rb') as f:
                g.VOCABS = pickle.load(f)
                f.close()
            if g.VOCABS: # Ignore empty file
                return
        except Exception as e:
            logging.debug('Unable to read vocab index file {}: {}'.format(config.VOCAB_CACHE_PATH, e))
            pass

    # we haven't been able to load from VOCABS.p so run collect() on each vocab source to recreate it

    # check each vocab source and,
    # using the appropriate class (from details['source']),
    # load all the vocabs from it into this session's (g) VOCABS variable
    g.VOCABS = {}
    for _name, details in config.VOCAB_SOURCES.items():
        getattr(source, details['source']).collect(details)

    # also load all vocabs into VOCABS.p on disk for future use
    if g.VOCABS: # Don't write empty file
        with open(config.VOCAB_CACHE_PATH, 'wb') as f:
            pickle.dump(g.VOCABS, f)
            f.close()

@app.context_processor
def context_processor():
    """
    A set of global variables available to 'globally' for jinja templates.
    :return: A dictionary of variables
    :rtype: dict
    """
    return dict(h=helper)


# run the Flask app
if __name__ == '__main__':
    logging.basicConfig(filename=config.LOGFILE,
                        level=logging.DEBUG,
                        datefmt='%Y-%m-%d %H:%M:%S',
                        format='%(asctime)s %(levelname)s %(filename)s:%(lineno)s %(message)s')

    app.run(debug=config.DEBUG, threaded=True)
