# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                                                                             #
#   Copyright 2024 Patrick Hohenecker                                         #
#                                                                             #
#   Redistribution and use in source and binary forms, with or without        #
#   modification, are permitted provided that the following conditions        #
#   are met:                                                                  #
#                                                                             #
#   1. Redistributions of source code must retain the above copyright         #
#      notice, this list of conditions and the following disclaimer.          #
#                                                                             #
#   2. Redistributions in binary form must reproduce the above copyright      #
#      notice, this list of conditions and the following disclaimer in the    #
#      documentation and/or other materials provided with the distribution.   #
#                                                                             #
#   3. Neither the name of the copyright holder nor the names of its          #
#      contributors may be used to endorse or promote products derived        #
#      from this software without specific prior written permission.          #
#                                                                             #
#   THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS       #
#   “AS IS” AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT         #
#   LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR     #
#   A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT      #
#   HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,    #
#   SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT          #
#   LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,     #
#   DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY     #
#   THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT       #
#   (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE     #
#   OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.      #
#                                                                             #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


"""Lists all existing :class:`~.models.project_template.ProjectTemplate`\\ s."""


import argparse
import datetime
import logging
import sys

import mumbojumbo.models as models
import mumbojumbo.template_loader as template_loader
import mumbojumbo.template_renderer as template_renderer

from collections.abc import Iterable
from typing import Final


#  CONSTANTS  ##########################################################################################################


_LOG_FORMAT: Final[str] = "%(message)s"
"""The used format of logged messages."""

_LOGGER: Final[logging.Logger] = logging.getLogger(__name__)
"""The :class:`logging.Logger` used by this module."""


#  HELPER FUNCTIONS  ###################################################################################################


def _fetch_template(template_name: str) -> models.ProjectTemplate | None:
    """Retrieves the template with the given ``template_name`` or ``None`` if no such template exists."""

    loader = template_loader.TemplateLoader()
    for template in loader.load_templates():

        if template.name == template_name:

            return template


def _parse_args() -> str:
    """Parses the command-line args.

    Returns:
        The name of the used template.
    """

    # First, we create the parser used for processing the command-line args.
    parser = argparse.ArgumentParser(
            prog="mj-apply",
            formatter_class=lambda prog: argparse.HelpFormatter(prog, max_help_position=59, width=120),
            description=(
                    "TODO(pat): add help text"  # TODO
            )
    )
    parser.add_argument(
            "template",
            action="store",
            type=str,
            help="The name of the used template.",
            metavar="TEMPLATE"
    )

    # Next, we parse the args.
    args = parser.parse_args()

    return args.template


def _prepare_custom_variables(custom_variables: Iterable[models.TemplateVariable]) -> dict[str, str]:
    """Prepares the values for the given custom ``variables``."""

    return {
            variable.name: _read_input(variable)
            for variable in custom_variables
    }


def _prepare_special_variables(special_variables: Iterable[str]) -> dict[str, str]:
    """Prepares the values for the given special ``variables``.

    Note:
        Unknown variables are simply ignored.
    """

    data = {}

    for variable in special_variables:

        if variable == "YEAR":

            data[variable] = str(datetime.datetime.now().year)

    return data


def _prepare_variables(template: models.ProjectTemplate) -> dict[str, str]:
    """Prepares the values for all :class:`~.models.template_variable.TemplateVariable`\\ s used by the ``template``.

    If any custom variable uses the same variable name as a special variable, then the custom one has precedence.
    """

    return (
            _prepare_special_variables(template.special_variables) |
            _prepare_custom_variables(template.custom_variables)  # -> Has precedence!
    )


def _read_input(variable: models.TemplateVariable) -> str:
    """Prompts the user to provide a value for the given ``variable``."""

    prompt = f"\n{variable.name}"
    if variable.default_value is not None:

        prompt += f" [{variable.default_value}]"

    prompt += ":\n"

    value = None
    while value is None:

        value = input(prompt) or variable.default_value

    return value


#  MAIN  ###############################################################################################################


def _main() -> None:

    template_name = _parse_args()
    template = _fetch_template(template_name)

    # We make sure that the requested template actually exists.
    if template is None:  # -> The template does not exist.

        _LOGGER.critical(f"There is no template with name <{template_name}>")
        sys.exit(1)

    else:  # -> The template exists.

        # Next, we prepare values for all used variables.
        data = _prepare_variables(template)

        # Finally, we render the template.
        template_renderer.TemplateRenderer.render(template, data)
        _LOGGER.info("OK")


if __name__ == "__main__":

    _main()
