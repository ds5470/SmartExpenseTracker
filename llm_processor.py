import json
from openai import OpenAI

client = OpenAI()

def get_category_from_llm(name, amount):
    try:
        prompt = f"{name} ${amount}"

        response = client.chat.completions.create(
            model="gpt-5-nano",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expense categorization assistant. Return ONLY one category word like Food, Travel, Shopping, Bills, Entertainment, or Other."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
        )

        category = response.choices[0].message.content.strip()

        return category

    except Exception as e:
        print("LLM Error:", e)
        return "Other"  # fallback so your app doesn’t crash
    

def get_insight(name):
    try:
        prompt = f"{name}"

        response = client.chat.completions.create(
            model="gpt-5-nano",
            messages=[
                {
                    "role": "system",
                    "content": "Analyze this spending and give an insight comparing the spending to other categories. Keep it concise in 1-2 lines, no extra information"
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
        )

        insight = response.choices[0].message.content.strip()

        return insight

    except Exception as e:
        print("LLM Error:", e)
        return "Other"  # fallback so your app doesn’t crash




if __name__ == "__main__":
    print(get_insight("STARBUCKS"))


#     print(get_category_from_llm("STARBUCKS", 10.50))
#     print(get_category_from_llm("TIM HORTONS", 8.50))
#     print(get_category_from_llm("MARSHALLS", 100.50))
#     print(get_category_from_llm("TARGET", 50.50))
