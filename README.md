# Ollama Cog Model - deepseek-r1:70b

This is an implementation of the Ollama model [deepseek-r1:70b](https://ollama.com/library/deepseek-r1:70b) as a [Cog](https://github.com/replicate/cog) model.

## Development

Follow the [model pushing guide](https://replicate.com/docs/guides/push-a-model) to push your own model to [Replicate](https://replicate.com).
    
## Basic Usage

To run a prediction:

    cog predict -i prompt="solve the equation x^2 - 3x + 2 = 0"


## Output

    <think>
    To solve the quadratic equation \( x^2 - 3x + 2 = 0 \), I'll start by recognizing that it fits the standard quadratic form \( ax^2 + bx + c = 0 \).

    Next, I'll use the factoring method to factorize the quadratic expression. I'll look for two numbers that multiply to give 2 (the constant term) and add up to -3 (the coefficient of the x-term). The numbers -1 and -2 satisfy these conditions.

    After factoring, the equation becomes \( (x - 1)(x - 2) = 0 \). Setting each factor equal to zero gives the potential solutions for x.

    Finally, I'll solve each simple equation to find the roots of the quadratic equation. This will provide the complete solution set.
    </think>
