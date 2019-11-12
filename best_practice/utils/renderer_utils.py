from rest_framework import renderers
from rest_framework.compat import SHORT_SEPARATORS, LONG_SEPARATORS, INDENT_SEPARATORS
import json


class CustomRenderer(renderers.JSONRenderer):

    def render(self, data, accepted_media_type=None, renderer_context=None):

        renderer_context = renderer_context or {}
        indent = self.get_indent(accepted_media_type, renderer_context)

        if indent is None:
            separators = SHORT_SEPARATORS if self.compact else LONG_SEPARATORS
        else:
            separators = INDENT_SEPARATORS

        response = renderer_context.get("response")
        if hasattr(response, "errors"):
            output = {"data": None, "errors": [error.__dict__ for error in response.errors]}
        else:
            output = {"data": data, "errors": list()}

        ret = json.dumps(
            output, cls=self.encoder_class,
            indent=indent, ensure_ascii=self.ensure_ascii,
            allow_nan=not self.strict, separators=separators
        )

        # We always fully escape \u2028 and \u2029 to ensure we output JSON
        # that is a strict javascript subset.
        # See: http://timelessrepo.com/json-isnt-a-javascript-subset
        ret = ret.replace('\u2028', '\\u2028').replace('\u2029', '\\u2029')
        return ret.encode()
