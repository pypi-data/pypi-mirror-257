import os

from sphinx.builders.latex import LaTeXBuilder


# Overrides the default Sphinx latex build
class IdfLatexBuilder(LaTeXBuilder):

    def __init__(self, app, env):

        # Sets up the latex_documents config value, done here instead of conf.py
        self.init_latex_documents(app)
        self.env = app.config
        super().__init__(app, env)


    def init_latex_documents(self, app):

        if app.config.pdf_title is None:
            raise ValueError('PDF title not configured, configure the value "pdf_title" in your Sphinx config file to build PDFs')

        if app.config.pdf_file_prefix is None:
            raise ValueError('PDF file name prefix not configured, configure the value "pdf_file_prefix" in your Sphinx config file to build PDFs')

        title = app.config.pdf_title

        if app.config.language == 'zh_CN':
            latex_documents = [('index', app.config.pdf_file + '.tex', title, u'奕行智能科技', 'manual')]
        else:
            # Default to english naming
            latex_documents = [('index', app.config.pdf_file + '.tex', title, u'EVAS Intelligence', 'manual')]

        app.config.latex_documents = latex_documents

    def prepare_latex_macros(self, package_path, config):

        PACKAGE_NAME = 'evas.sty'
        latex_package = ''
        if config.doc_id is None:
            doc_id = ''
        else:
            doc_id = config.doc_id
        with open(os.path.join(package_path, PACKAGE_NAME), 'r') as template:

            latex_package = template.read()

        # Release name for the PDF front page, remove '_' as this is used for subscript in Latex
        idf_release_name = 'Release {}'.format(config.version.replace('_', '-'))
        latex_package = latex_package.replace('<idf_release_name>', idf_release_name)

        # Retrieve docid for feedback link
        latex_package = latex_package.replace('<doc_id>', doc_id)

        with open(os.path.join(self.outdir, PACKAGE_NAME), 'w') as package_file:
            package_file.write(latex_package)

    def finish(self):
        super().finish()

        TEMPLATE_PATH = self.config.latex_template_dir
        self.prepare_latex_macros(TEMPLATE_PATH, self.config)


def config_init_callback(app, config):
    if config.pdf_file_prefix:
        config.pdf_file = '{}-{}-{}'.format(config.pdf_file_prefix, config.language, config.version)


def setup(app):
    app.add_builder(IdfLatexBuilder, override=True)

    app.add_config_value('pdf_file_prefix', None, 'env')
    app.add_config_value('pdf_file', None, 'env')
    app.add_config_value('pdf_title', None, 'env')

    # Config values that depends on target which is not available when setup is called
    app.connect('config-inited',  config_init_callback)

    return {'parallel_read_safe': True, 'parallel_write_safe': True, 'version': '0.1'}
