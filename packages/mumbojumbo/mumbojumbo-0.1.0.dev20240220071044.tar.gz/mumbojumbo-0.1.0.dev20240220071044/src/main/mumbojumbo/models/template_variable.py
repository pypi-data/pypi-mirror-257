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


from dataclasses import dataclass


@dataclass
class TemplateVariable:
    """Describes a single project template (consisting of possibly multiple files)."""

    #  ATTRIBUTES  #####################################################################################################

    name: str
    """The name of the :class:`~.TemplateVariable`."""

    description: str
    """A description of the :class:`~.TemplateVariable`. This is displayed to users when they are asked to provide a
    value for the :class:`~.TemplateVariable`.
    """

    adjustable: bool = True
    """Indicates whether users are allowed to specify a value for the :class:`~.TemplateVariable`."""

    default_value: str | None = None
    """A default value that is used :class:`~.TemplateVariable` that is used whenever no user-defined value is
    available. Notice that this attribute is required to be specified when :attr:`~.TemplateVariable.adjustable` is
    ``False``.
    """

    #  INIT  ###########################################################################################################

    def __post_init__(self) -> None:

        # We ensure that a default value is specified in case the variable is not adjustable.
        if not self.adjustable and self.default_value is None:

            raise ValueError("A <default_value> is required when <adjustable> is False")

    #  METHODS  ########################################################################################################

    @staticmethod
    def from_json(json_spec: dict) -> "TemplateVariable":
        """Creates the :class:`~.TemplateVariable` that is described as JSON object by the given ``json_spec``."""

        default_value = json_spec["default_value"] if "default_value" in json_spec else None
        return TemplateVariable(
                json_spec["name"],
                json_spec["description"],
                json_spec["adjustable"],
                default_value
        )
