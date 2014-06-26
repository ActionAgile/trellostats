from jinja2 import Environment, PackageLoader



def get_env(templates_folder='templates'):
	return Environment(loader=PackageLoader('trellostats', templates_folder))	


def render_text(env, **data):
	template = env.get_template('text.tmpl')
	return template.render(**data)

