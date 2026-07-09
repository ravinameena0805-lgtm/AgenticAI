import time

from fuzzing.executor import FuzzExecutor
from fuzzing.mutator import PromptMutator
from fuzzing.mutations.ai_mutator import AIMutator

from fuzzing.seed_pool.seed_pool import SeedPool
from fuzzing.oracle.oracle import Oracle


class FuzzCampaign:

    def __init__(
        self,
        provider,
        mutation_engine="AI Generated Mutations (Recommended)"
    ):
        self.executor = FuzzExecutor(provider)
        self.template_mutator = PromptMutator()
        self.ai_mutator = AIMutator()
        self.mutation_engine = mutation_engine

        # New components for adaptive fuzzing
        self.seed_pool = SeedPool()
        self.oracle = Oracle()

    def run(self, seed_prompt, max_tests):

        print("=" * 60)
        print("NEW CAMPAIGN STARTED")
        print("=" * 60)

        # ---------------------------------------------------------
        # Adaptive Configuration
        # ---------------------------------------------------------

        MAX_GENERATIONS = 5
        TOP_K = 3

        results = []

        self.seed_pool.clear()

        root_seed = self.seed_pool.add_prompt(
            prompt=seed_prompt,
            generation=0,
            operator="Original",
            score=0
        )

        current_generation = [root_seed]

        print("\nAdaptive Beam Search Started")
        print(f"Maximum Generations : {MAX_GENERATIONS}")
        print(f"Top K Seeds         : {TOP_K}")

        # ---------------------------------------------------------
        # Generation Loop
        # ---------------------------------------------------------

        for generation in range(MAX_GENERATIONS):

            print("\n" + "=" * 70)
            print(f"Generation {generation}")
            print("=" * 70)

            next_generation = []

            # -----------------------------------------------------
            # Mutate every selected seed
            # -----------------------------------------------------

            for current_seed in current_generation:

                print(f"\nCurrent Seed:\n{current_seed.prompt}\n")

                # ---------------------------------------------
                # Generate mutations
                # ---------------------------------------------

                if self.mutation_engine == "AI Generated Mutations (Recommended)":

                    mutated_prompts = self.ai_mutator.generate(
                        current_seed.prompt,
                        count=max_tests
                    )

                    if not mutated_prompts:

                        print("AI generation failed.")
                        print("Switching to Template Mutator.")

                        mutated_prompts = (
                            self.template_mutator.generate_mutations(
                                current_seed.prompt
                            )
                        )[:max_tests]

                else:

                    mutated_prompts = (
                        self.template_mutator.generate_mutations(
                            current_seed.prompt
                        )
                    )[:max_tests]

                # ---------------------------------------------
                # Execute every mutation
                # ---------------------------------------------

                for i, attack in enumerate(mutated_prompts, start=1):

                    print("-" * 60)
                    print(f"Mutation {i}/{len(mutated_prompts)}")
                    print("Category :", attack["category"])
                    print("Prompt   :", attack["prompt"])
                    print("-" * 60)

                    response = self.executor.run_prompt(
                        attack["prompt"]
                    )

                    response_text = response["response"]

                    oracle_result = self.oracle.evaluate(
                        response_text
                    )

                    score = oracle_result["score"]

                    child_seed = self.seed_pool.add_prompt(
                        prompt=attack["prompt"],
                        parent=current_seed,
                        score=score,
                        generation=current_seed.generation + 1,
                        operator=attack["category"]
                    )

                    next_generation.append(child_seed)

                    results.append({
                        "provider": self.executor.router.provider,
                        "generation": generation,
                        "category": attack["category"],
                        "prompt": attack["prompt"],
                        "response": response_text,
                        "response_time": response["response_time"],
                        "response_length": len(response_text.split()),
                        "oracle_success": oracle_result["success"],
                        "oracle_score": score
                    })

                    time.sleep(4)

            # -----------------------------------------------------
            # Beam Search
            # -----------------------------------------------------

            if len(next_generation) == 0:

                print("No more seeds generated.")
                break

            next_generation.sort(
                key=lambda seed: seed.score,
                reverse=True
            )

            current_generation = next_generation[:TOP_K]

            print("\nTop Seeds Selected")

            for seed in current_generation:

                print(
                    f"Generation={seed.generation} "
                    f"Score={seed.score} "
                    f"Operator={seed.operator}"
                )

            # -----------------------------------------------------
            # Early Stop
            # -----------------------------------------------------

            if current_generation[0].score >= 10:

                print("\nHigh-scoring attack found.")
                print("Stopping early.")
                break

        print("\nCampaign Finished")
        print(f"Total Seeds : {self.seed_pool.size()}")

        return results
 
    def run_conversation_campaign(self, conversation_turns, max_tests):

        results = []

        for i in range(min(len(conversation_turns), max_tests)):

            messages = conversation_turns[i]

            responses = self.executor.run_conversation(messages)
            final_response = (
                responses[-1]["response"]
                if isinstance(responses, list)
                else responses
            )

            results.append({
                "provider": self.executor.router.provider,
                "category": "Multi-Turn",
                "conversation": messages,
                "responses": responses,
                "response_length": len(str(final_response).split())
            })

            time.sleep(4)

        return results