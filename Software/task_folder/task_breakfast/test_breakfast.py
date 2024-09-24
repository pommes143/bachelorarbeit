from example_solution import breakfast as breakfast
#!cut_imports!#
def test_breakfast():
    # Test case 1: Check if the function correctly processes the input sentence
    sentence1 = "ham, fruit, juice"
    result1 = breakfast(sentence1)
    assert result1[0] == 6,  "It seems that the length of the list is not calcualted properly."
    assert result1[2] == ['coffee', 'ham', 'fruit'],  "1. It seems that the new list is not created properly."
    assert result1[1] == 8, "It seems that the sum of lengths of products is not correct." 
    assert result1[2][0] == 'coffee', "Coffee always comes first!"

    # Test case 2: Test the function with a different input sentence
    sentence2 = "cereal, milk, yogurt"
    result2 = breakfast(sentence2)
    assert result2[0] == 6,  "It seems that the length of the list is not calcualted properly."
    assert result2[2] == ["coffee", "cereal", "milk"],  "2. It seems that the new list is not created properly."
    assert result2[1] == 10,  "It seems that the sum of lengths of products is not correct."

    # Test case 3: Test the function with an empty input sentence
    sentence3 = ""
    result3 = breakfast(sentence3)
    assert result3[0] == 4,  "It seems that the length of the list is not calcualted properly."
    assert result3[2] == ['coffee', '', 'coffee'],  "If you have nothing to eat, then coffee should be double." 
    assert result3[1] == 6,  "It seems that the length of the list is not calcualted properly."