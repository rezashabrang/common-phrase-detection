from phrase_counter.word_graph import generate_word_graph


def test_simple_output_word_graph():
    """Simple output test for word graph"""
    samlpe_text = "test number one"
    output = generate_word_graph(samlpe_text)
    assert output
