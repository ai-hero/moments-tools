import logging
import os
import sys
from time import perf_counter

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, Pipeline, pipeline

# Set up logger
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
log = logging.getLogger(__name__)

HF_MODEL = os.environ["HF_MODEL"]


class Generator:
    """A class for the classifier with only class methods for prediction"""

    # Class variable for the model pipeline
    generator: Pipeline = None

    @classmethod
    def load(cls):
        # Only load one instance of the model
        if cls.generator is None:
            # Load the model pipeline.
            # Note: Usually, this would also download the model.
            # But, we download the model into the container in the Dockerfile
            # so that it's built into the container and there's no download at
            # run time (otherwise, each time the container spins up
            # we'll download a 1GB model).
            # Loading still takes time, though. So, we do that here.
            # Note: You can use a GPU here if needed.
            device = "cuda:0" if torch.cuda.is_available() else "cpu"
            model = AutoModelForCausalLM.from_pretrained(HF_MODEL)
            # this line needed for now, probably a config issue.
            tokenizer = AutoTokenizer.from_pretrained(HF_MODEL)
            t0 = perf_counter()
            cls.generator = pipeline(
                "text-generation", model=model, tokenizer=tokenizer, device=device
            )

            elapsed = 1000 * (perf_counter() - t0)
            log.info("Model warm-up time: %d ms.", elapsed)

    @classmethod
    def predict(cls, prompt: str) -> str:
        """Return the prediction probabilities for each class in the same order"""
        assert prompt  # sanity check

        # Make sure the model is loaded.
        cls.load()

        # Predict.
        t0 = perf_counter()
        # pylint: disable-next=not-callable
        completion = cls.generator(prompt, max_new_tokens=150)
        elapsed = 1000 * (perf_counter() - t0)
        log.info("Model prediction time: %d ms.", elapsed)

        return completion
