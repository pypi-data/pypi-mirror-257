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


import json
import os
import pathlib

import jsonschema

import mumbojumbo.models as models

from typing import Final


class TemplateLoader:
    """Loads available :class:`~.models.project_template.ProjectTemplate`\\ s from the disk.

    TODO(pat): describe how loading works under the hood
    """

    _DEFAULT_SOURCE_DIR: Final[pathlib.Path] = pathlib.Path.home() / ".mumbo-jumbo/templates"
    """The default source directory that is used when no other directory is specified via environment variables."""

    _JSON_SCHEMA: Final[dict] = {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "type": "object",
            "properties": {
                    "name": {
                            "type": "string"
                    },
                    "description": {
                            "type": "string"
                    },
                    "special_variables": {
                            "type": "array",
                            "items": {
                                    "type": "string"
                            }
                    },
                    "custom_variables": {
                            "type": "array",
                            "items": {
                                    "type": "object",
                                    "properties": {
                                            "name": {
                                                    "type": "string"
                                            },
                                            "description": {
                                                    "type": "string"
                                            },
                                            "adjustable": {
                                                    "type": "boolean"
                                            },
                                            "default_value": {
                                                    "type": "string"
                                            }
                                    },
                                    "required": ["name", "description", "adjustable"]
                            }
                    }
            },
            "required": ["name", "description"]
    }
    """Describes all JSON objects considered valid specifications of a ``template.json`` file."""

    _SOURCE_DIR_ENV_VAR: Final[str] = "MJ_TEMPLATE_DIR"
    """The name of the environment variable that can be used to specify the directory that contains all templates."""

    _TEMPLATE_JSON_NAME: Final[str] = "template.json"
    """The filename of the template specification file."""

    #  INIT  ###########################################################################################################

    def __init__(self) -> None:
        """Creates a new instance of :class:`~.TemplateLoader`."""

        self._source_dir = self._get_source_dir()

    #  METHODS  ########################################################################################################

    @classmethod
    def _get_source_dir(cls) -> pathlib.Path:
        """Retrieves the path of the folder that contains all available
        :class:`~.models.project_template.ProjectTemplate`\\ s.
        """

        return (
                pathlib.Path(os.environ[cls._SOURCE_DIR_ENV_VAR])
                if cls._SOURCE_DIR_ENV_VAR in os.environ else
                cls._DEFAULT_SOURCE_DIR
        )

    def _load_template(self, template_dir: pathlib.Path) -> models.ProjectTemplate | None:
        """Loads the :class:`~.models.project_template.ProjectTemplate` stored in the given ``template_dir``."""

        template_json_path = template_dir / self._TEMPLATE_JSON_NAME
        if template_json_path.is_file():

            template_json = json.loads(template_json_path.read_text())

            try:

                jsonschema.validate(instance=template_json, schema=self._JSON_SCHEMA)
                template_files = self._scan_for_template_files(template_dir)

                return models.ProjectTemplate.create(template_dir, template_files, template_json)

            except jsonschema.ValidationError:

                return None

    @classmethod
    def _scan_for_template_files(cls, template_dir: pathlib.Path) -> list[pathlib.Path]:
        """Recursively scans the given ``template_dir`` and retrieves the (relative) paths of all files contained.

        Note:
            ``.DS_Store``  are ignored.
        """

        return [
                x.relative_to(template_dir)
                for x in template_dir.glob("**/*")
                if (
                        x.is_file() and
                        x.relative_to(template_dir) != pathlib.Path(cls._TEMPLATE_JSON_NAME) and
                        str(x.name) != ".DS_Store"
                )
        ]

    def load_templates(self) -> list[models.ProjectTemplate]:
        """Retrieves all available :class:`~.models.project_template.ProjectTemplate`\\ s."""

        template_dirs = [x for x in self._source_dir.glob("*") if x.is_dir()]
        templates = [self._load_template(x) for x in template_dirs]
        return [x for x in templates if x]
