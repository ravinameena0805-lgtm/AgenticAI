from agents.template_agent import TemplateAgent


def main():

    template_agent = TemplateAgent()

    prompt = template_agent.run(

        "Summarize the following article."

    )

    print(prompt)


if __name__ == "__main__":
    main()