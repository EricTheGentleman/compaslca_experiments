from methods.material_prompt_builder import build_material_prompt
from methods.material_prompt_builder_ger import build_material_prompt_ger
from openai import OpenAI
import google.generativeai as genai
import anthropic
import json
import re

class TokenUsageWrapper:
    def __init__(self, prompt_tokens, completion_tokens):
        self.prompt_tokens = prompt_tokens
        self.completion_tokens = completion_tokens

    def to_dict(self):
        return {
            "prompt_tokens": self.prompt_tokens,
            "completion_tokens": self.completion_tokens,
            "total_tokens": self.prompt_tokens + self.completion_tokens,
            "completion_tokens_details": {
                "accepted_prediction_tokens": 0,
                "audio_tokens": 0,
                "reasoning_tokens": 0,
                "rejected_prediction_tokens": 0
            },
            "prompt_tokens_details": {
                "audio_tokens": 0,
                "cached_tokens": 0
            }
        }


def material_inference(bim_element, material_entries, mode, category, var_config, model_config):
    model_config_temp = model_config.get("model_config", {})
    model_choice = model_config_temp.get("model")
    company = model_config_temp.get("company", "OpenAI")  # default to OpenAI
    key = model_config_temp.get("key")

    framing_config = var_config.get("prompt_framing_style", {})
    german = framing_config.get("german")

    # Build the prompt
    if german:
        prompt = build_material_prompt_ger(bim_element, material_entries, mode, category, var_config)
    else:
        prompt = build_material_prompt(bim_element, material_entries, mode, category, var_config)

    # === OPENAI ===
    if company.lower() == "openai":
        if model_choice == "o3" or model_choice == "o3-pro-2025-06-10":
            client = OpenAI(api_key=key)
            response=client.responses.create(
                model=model_choice,
                input=[{"role":"user", "content":prompt}],
                reasoning={"effort":"medium"}
            )
            response_text = response.output_text
            response_cleaned = re.sub(r"```json|```", "", response_text).strip()
            parsed_response = json.loads(response_cleaned)

            usage = response.usage
            token_usage = TokenUsageWrapper(
                prompt_tokens=usage.input_tokens,
                completion_tokens=usage.output_tokens
            )

            return parsed_response, token_usage

        else:
            client = OpenAI(api_key=key)

            response = client.chat.completions.create(
                model=model_choice,
                messages=[{"role": "user", "content": prompt}],
                temperature=model_config_temp.get("temperature"),
                max_tokens=model_config_temp.get("max_tokens")
            )

            response_text = response.choices[0].message.content
            response_cleaned = re.sub(r"```json|```", "", response_text).strip()
            parsed_response = json.loads(response_cleaned)

            usage = response.usage
            token_usage = TokenUsageWrapper(
                prompt_tokens=usage.prompt_tokens,
                completion_tokens=usage.completion_tokens
            )

            return parsed_response, token_usage

    # === CLAUDE ===
    elif company.lower() == "anthropic":
        client = anthropic.Anthropic(api_key=key)

        response = client.messages.create(
            model=model_choice,
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}]
        )

        try:
            response_text = response.content[0].text.strip()
            response_cleaned = re.sub(r"```json|```", "", response_text).strip()
            parsed_response = json.loads(response_cleaned)
        except Exception as e:
            raise ValueError(f"Claude returned invalid JSON:\n{response_text}") from e

        usage = response.usage
        token_usage = TokenUsageWrapper(
            prompt_tokens=usage.input_tokens,
            completion_tokens=usage.output_tokens
        )

        return parsed_response, token_usage

    # === GEMINI ===
    elif company.lower() == "gemini":
        genai.configure(api_key=key)

        model = genai.GenerativeModel(model_choice)

        # Send the prompt
        response = model.generate_content(prompt)

        # Get response text
        try:
            response_text = response.text.strip()
            response_cleaned = re.sub(r"```json|```", "", response_text).strip()
            parsed_response = json.loads(response_cleaned)
        except Exception as e:
            raise ValueError(f"Gemini returned invalid JSON:\n{response_text}") from e

        # Get token usage (if available)
        usage = response.usage_metadata
        token_usage = TokenUsageWrapper(
            prompt_tokens = getattr(usage, "prompt_token_count", 0),
            completion_tokens = getattr(usage, "candidates_token_count", 0)
        )

        return parsed_response, token_usage

    else:
        raise ValueError(f"Unsupported company: {company}")