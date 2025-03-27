import json
import os

from google import genai
from google.genai import types


class CommitMessageGenerator:
    def __init__(self, config_path="config.json"):
        self.client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
        self.model = "gemini-2.0-flash"
        self.config_path = config_path

    def _load_config(self):
        with open(self.config_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _create_response_schema(self, schema_config):
        return genai.types.Schema(
            type=genai.types.Type[schema_config["type"]],
            required=schema_config["required"],
            properties={
                key: genai.types.Schema(
                    type=genai.types.Type[value["type"]],
                    items=(
                        genai.types.Schema(
                            type=genai.types.Type[value["items"]["type"]]
                        )
                        if "items" in value
                        else None
                    ),
                )
                for key, value in schema_config["properties"].items()
            },
        )

    def generate(self, git_diff):
        config = self._load_config()

        contents = []
        for content in config["example_contents"]:
            parts = [
                types.Part.from_text(text=part["text"]) for part in content["parts"]
            ]
            contents.append(types.Content(role=content["role"], parts=parts))

        contents[-1].parts[0].text = git_diff

        schema_config = config["generate_content_config"]["response_schema"]
        response_schema = self._create_response_schema(schema_config)

        generate_content_config = types.GenerateContentConfig(
            temperature=config["generate_content_config"]["temperature"],
            response_mime_type=config["generate_content_config"]["response_mime_type"],
            response_schema=response_schema,
            system_instruction=[
                types.Part.from_text(text=config["system_instruction"]),
            ],
        )

        response = self.client.models.generate_content(
            model=self.model,
            contents=contents,
            config=generate_content_config,
        )

        return response.text
