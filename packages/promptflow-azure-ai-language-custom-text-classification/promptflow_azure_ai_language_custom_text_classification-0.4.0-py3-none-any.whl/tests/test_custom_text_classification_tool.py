import pytest
import unittest

from promptflow.connections import CustomConnection

from custom_text_classification_tool.tools.custom_text_classification import classify_text


@pytest.fixture
def language_connection() -> CustomConnection:
    language_connection = CustomConnection(
        {
            "api_key": "API_KEY",
        },
        {
            "endpoint": "https://example-endpoint.cognitiveservices.azure.com"
        }
    )
    return language_connection


class TestTool:
    def test_classify_text(self, language_connection):
        result = classify_text(language_connection,
                               {
                                   "id": "1",
                                   "text": "Welcome",
                                   "language": "en"
                               },
                               "blm-assistant-topic-ita",
                               "blm-assistant-topic-ita")
        print(result)


# Run the unit tests
if __name__ == "__main__":
    unittest.main()
