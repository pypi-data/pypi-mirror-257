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


import pathlib
import re
import shutil

import jinja2

import mumbojumbo.models as models


class TemplateRenderer:
    """Renders :class:`~.models.project_template.ProjectTemplate`\\ s."""

    #  METHODS  ########################################################################################################

    @staticmethod
    def _assemble_target_path(
            data: dict[str, str],
            target_dir: pathlib.Path,
            template_file: pathlib.Path
    ) -> pathlib.Path:
        """Creates the path that the ``template_file`` will be rendered to in the ``target_dir``.

        As part of assembling the new path, any variable expressions referencing
        :class:`~.models.template_variable.TemplateVariable`\\ s  (i.e., ``{{ VAR_NAME }}``) will be resolved by means
        of the provided ``data``. Variable references that do not have an according value in the ``data`` are simply
        left unchanged.

        Args:
            data: The data (usually :class:`~.models.template_variable.TemplateVariable`\\ s) used to render the
                according :class:`~.models.project_template.ProjectTemplate`.
            target_dir: The path of the directory that the :class:`~.models.project_template.ProjectTemplate` that the
                ``template_file`` is part of is rendered to.
            template_file: The relative path of the considered file inside the
                :class:`~.models.project_template.ProjectTemplate`.

        Returns:
            The assembled :class:`~pathlib.Path`.
        """

        target_path_as_str = str(target_dir / template_file)

        for template_variable, value in data.items():

            target_path_as_str = re.sub(r"\{\{ ?" + template_variable + " ?}}", value, target_path_as_str)

        return pathlib.Path(target_path_as_str)

    @staticmethod
    def _ensure_no_overrides(template: models.ProjectTemplate, target_dir: pathlib.Path) -> None:
        """Ensures that rendering the ``template`` into the ``target_dir`` would not override existing files.

        Raises:
            ValueError: If rendering the ``template`` would override (one or more) existing files.
        """

        for template_file in template.template_files:

            target_path = target_dir / template_file
            if target_path.is_file():

                raise ValueError(
                        f"Rendering the given <template> would override the following existing file: <{target_path}>"
                )

    @classmethod
    def _render_template_file(
            cls,
            template: models.ProjectTemplate,
            data: dict[str, str],
            target_dir: pathlib.Path,
            template_file: pathlib.Path
    ) -> None:
        """Renders the specified ``template_file`` into the ``target_dir``."""

        # We start by assembling the source path that the template file is written and the target path that the rendered
        # file will be written to. Furthermore, we prepare the required directory structure.
        source_path = template.template_dir / template_file
        target_path = cls._assemble_target_path(data, target_dir, template_file)
        target_path.parent.mkdir(parents=True, exist_ok=True)

        try:

            # Next, we load and render the template file.
            jinja_template = jinja2.Template(
                    source_path.read_text(),  # -> Raises a UnicodeDecodeError in case of a binary file.
                    keep_trailing_newline=True
            )
            rendered = jinja_template.render(data=data)

            # Finally, we write the rendered template to the disk.
            target_path.write_text(rendered)

        except UnicodeDecodeError:  # -> The rendered file is a binary (as opposed to a text) file.

            # We copy the binary file to the target path as-is.
            shutil.copyfile(source_path, target_path)

    @classmethod
    def render(
            cls,
            template: models.ProjectTemplate,
            data: dict[str, str],
            target_dir: pathlib.Path = pathlib.Path("."),
            fail_if_file_exists: bool = True
    ) -> None:
        """Renders the given ``template`` into the ``target_dir``.

        The given ``data`` is added to the :mod:`jinja2` context as an object also called ``data``. Hence, if there is
        a key ``"ABC"`` in the ``data``, then the according value can be used in the rendered ``template`` like this:
        ``{{ data.ABC }}``.

        If ``fail_if_file_exists`` is set to ``True`` (which is also the default value), then a check is performed that
        ensures that no existing file is overridden by rendering the ``template`` into the ``target_dir``. Notice that
        this check is performed before any file is created, which means that rendering either succeeds or fails entirely
        without producing any output at all. If the check fails, then a :class:`ValueError` is raised.

        Args:
            template: The rendered :class:`~.models_project_template.ProjectTemplate`.
            data: The data (usually :class:`~.models.template_variable.TemplateVariable`\\ s) used by the ``template``.
            target_dir: The path of the directory that the ``template`` is rendered into.
            fail_if_file_exists: Indicates whether a check that ensures no files are overridden should be performed.

        Raises:
            ValueError: If ``fail_if_file_exists`` is ``True`` and rendering the ``template`` would override (one or
                more) existing files.
        """

        # If required, we check whether rendering would override any existing files, and raise an error if this should
        # be the case.
        if fail_if_file_exists:

            cls._ensure_no_overrides(template, target_dir)

        # We iterate over all file that are part of the project template, and render them one by one.
        for template_file in template.template_files:

            cls._render_template_file(template, data, target_dir, template_file)
