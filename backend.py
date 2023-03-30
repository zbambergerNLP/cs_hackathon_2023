import typing
import openai
import os

EXAMPLE_1 = """
When my child was diagnosed with diabetes, it was a difficult and emotional experience. It was tough to come to
terms with the fact that our lives were going to change dramatically, but we were determined to do everything we
could to manage the condition and help our child lead a healthy and happy life.

We tried a number of different treatments, including insulin therapy and dietary changes. It was a learning curve,
and there were some ups and downs along the way, but we persevered and gradually found the right combination of
treatments and lifestyle changes that worked for our child.

It was a relief to see our child's condition improve over time, and we became much more confident and optimistic
about the future. We learned to be proactive about managing diabetes and became more comfortable with things like
administering insulin injections and monitoring blood sugar levels.

Today, our child is doing much better and living a full and active life. While there are still challenges that come
with managing diabetes, we feel much more equipped to handle them and are grateful for the medical advances and
resources that have made it possible for our child to thrive.
"""


def analyze_text(text: str) -> typing.Tuple[str, typing.List[str]]:
    """
    Given a testimonial text, retrieve the ailment mentioned in the text, and the treatments for that ailment.

    :param text: A long text such as the one above.
    :return: A 2-tuple of the form [ailment, list_of_treatments] where ailment is a single entity diagnosis of the
        ailment discussed in the text, and list_of_treatments is a list of textual treatments for that ailment.
    """
    pass


if __name__ == '__main__':
    # Set up your OpenAI API key
    openai.organization = "org-JjJq8L2sJ9qYKxxy3JeFSH1u"
    openai.api_key = "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"

    # Define the prompt and parameters for the ChatGPT model
    prompt = "text: Diet is the single most significant risk factor for disability and premature death. Patients and " \
             "physicians often have difficulty staying abreast of diet trends, many of which focus primarily on " \
             "weight loss rather than nutrition and health. Recommending an eating style can help patients make " \
             "positive change. Dietary patterns that support health include the Mediterranean diet, the Dietary " \
             "Approaches to Stop Hypertension diet, the 2015 Dietary Guidelines for Americans, and the Healthy " \
             "Eating Plate. These approaches have benefits that include prevention of cardiovascular disease, " \
             "cancer, type 2 diabetes mellitus, and obesity. These dietary patterns are supported by strong evidence " \
             "that promotes a primary focus on unprocessed foods, fruits and vegetables, plant-based fats and " \
             "proteins, legumes, whole grains, and nuts. Added sugars should be limited to less than 5% to 10% of " \
             "daily caloric intake. Vegetables (not including potatoes) and fruits should make up one-half of each " \
             "meal. Carbohydrate sources should primarily include beans/legumes, whole grains, fruits, and " \
             "vegetables. An emphasis on monounsaturated fats, such as olive oil, avocados, and nuts, and omega-3 " \
             "fatty acids, such as flax, cold-water fish, and nuts, helps prevent cardiovascular disease, type 2 " \
             "diabetes, and cognitive decline. A focus on foods rather than macronutrients can assist patients in " \
             "understanding a healthy diet. Addressing barriers to following a healthy diet and utilizing the entire " \
             "health care team can assist patients in following these guidelines. " \
             "claim: Eating olive oil helps prevent cardiovascular disease. " \
             "is there a support for the claim in the text? return yes or no"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system",
             "content": f"{prompt}"},
        ]
    )

    message = response.choices[0].message.content
    print(message)
