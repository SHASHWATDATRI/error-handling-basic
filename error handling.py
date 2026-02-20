def errorhandler():
    try:
        num1 = float(input("Enter the first number: "))
        num2 = float(input("Enter the second number: "))
        result = num1 / num2
    except ZeroDivisionError:
        print("Error: Cannot divide by zero.")
    except ValueError:
        print("Error: Invalid input. Please enter a number.")
    else:
        print(f"The division  is: {result}")
    finally:
        print("Execution completed.")

errorhandler()
