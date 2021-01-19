__author__ = "{{ cookiecutter.authors }}"
__copyright__ = "Copyright {% now 'utc', '%Y' %}"
__email__ = "{{ cookiecutter.email }}"
__license__ = "{{ cookiecutter.license }}"

import os
from snakemake.shell import shell

scriptFolder = os.path.dirname(os.path.abspath(__file__))

class MissingInputException(Exception):
    """Exception raised for errors in the input.

    Args:
        Exception ([type]): Exception class cast

    Attributes:
        inp (string): Input which is missing.
    """

    def __init__(self, inp):
        self.inp = inp

    def __str__(self):
        return("Input %s is missing!" % (self.inp))

class MissingOutputException(Exception):
    """Exception raised for errors in the input.

    Args:
        Exception ([type]): Exception class cast

    Attributes:
        output (string): Output which is missing.
    """

    def __init__(self, output):
        self.output = output

    def __str__(self):
        return("Output %s is missing!" % (self.output))

class MissingParameterException(Exception):
    """Exception raised for errors in the input.

    Args:
        Exception ([type]): Exception class cast

    Attributes:
        parameter (string): Parameter which is missing.
    """

    def __init__(self, parameter):
        self.parameter = parameter

    def __str__(self):
        return("Parameter %s is missing!" % (self.parameter))


# Checking inputs
{% for inp in cookiecutter.inputs.split(',') %}
if "{{ inp.strip() }}" in snakemake.inputs.keys():
    input_{{inp.strip()}} = snakemake.inputs["{{ inp.strip() }}"]
else:
    raise MissingInputException("{{ inp.strip() }}")
 {% endfor %}

 # Checking outputs
{% for output in cookiecutter.outputs.split(',') %}
if "{{ output.strip() }}" in snakemake.outputs.keys():
    output_{{output.strip()}} = snakemake.outputs["{{ output.strip() }}"]
else:
    raise MissingOuputException("{{ output.strip() }}")
 {% endfor %}

# Checking parameters, remove else when parameter is not necessary and add a default value
{% for param in cookiecutter.params.split(',') %}
if "{{ param.strip() }}" in snakemake.params.keys():
    param_{{ param.strip() }} = snakemake.params["{{ param.strip() }}"]
else:
    raise MissingParameterException("{{ param.strip() }}")
 {% endfor %}


# running the shell
shell(
    """
    python  {scriptFolder}/script.py\
    {% for param in cookiecutter.params.split(',') %} {param_{{ param.strip() }}} {% endfor %} \
    {% for inp in cookiecutter.inputs.split(',') %} {input_{{ inp.strip() }}} {% endfor %} | \
    > {% for output in cookiecutter.outputs.split(',') %} {output_{{ output.strip() }}} {% endfor %}
    """
)
