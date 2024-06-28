from datetime import datetime

GPT_COMMON_FUNCTIONS = [
    {
        "name": "generate_blog_post",
        "description": "If user asked to Generate Blog Post for Heatlhcare, Generate posts on Diseases & Health awareness",
        "parameters": {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": f"Title of Blog Post"
                },
                "content": {
                    "type": "string",
                    "description": f"Content of Blog Post. Content length must be greated than 5000 words, must invlude Bold, Italic, Paragrams, Awesome Content. More realistic and SEO Friendly"
                },
                "category": {
                    "type": "string",
                    "description": f"Category of Blog Post. try selecting category from given list. If does not match then return new one."
                },
                "read_time": {
                    "type": "number",
                    "description": "Estimated Read time of blog post in minutes"
                },
                "tags": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    },
                    "description": "Array of tags related to the blog post"
                }
            },
            "required": [
                "title",
                "content",
                "category",
                "read_time",
                "tags",
            ]
        }
    },
]

