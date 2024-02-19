import pytest

from autogoal_contrib import find_classes
from autogoal.grammar import generate_cfg, Sampler
from autogoal.utils import is_package_installed
from autogoal.exceptions import InterfaceIncompatibleError

from autogoal_nltk import nltk


classes = find_classes(modules=[nltk])


@pytest.mark.contrib
@pytest.mark.parametrize("clss", classes)
@pytest.mark.skipif(
    not is_package_installed("autogoal_nltk"), reason="The test requires autogoal_nltk"
)
def test_create_grammar_for_generated_class(clss):
    try:
        generate_cfg(clss, registry=classes)
    except InterfaceIncompatibleError:
        pass


@pytest.mark.slow
@pytest.mark.contrib
@pytest.mark.parametrize("clss", classes)
@pytest.mark.skipif(
    not is_package_installed("autogoal_nltk"), reason="The test requires autogoal_nltk"
)
def test_sample_generated_class(clss):
    grammar = generate_cfg(clss, registry=classes)
    sampler = Sampler(random_state=0)

    for _ in range(1000):
        grammar.sample(sampler=sampler)
