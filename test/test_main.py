from main import add_numbers

def test_add_numbers():
    # Arrange
    num1 = 2
    num2 = 3

    # Act
    result = add_numbers(num1, num2)

    # Assert
    assert result == 5