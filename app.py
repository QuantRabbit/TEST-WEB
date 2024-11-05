from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def home():
    return '''
<!DOCTYPE html>
<html>
<head>
    <title>Simple Calculator</title>
    <style>
        /* Basic Reset */
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: Arial, sans-serif;
        }

        /* Body Styling */
        body {
            background-color: #f4f4f9;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            padding: 20px;
        }

        /* Container Styling */
        .container {
            background-color: #fff;
            border-radius: 10px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
            padding: 30px;
            width: 100%;
            max-width: 400px;
            text-align: center;
        }

        /* Heading Styling */
        h2 {
            color: #333;
            margin-bottom: 20px;
        }

        /* Form Elements */
        form label {
            display: block;
            margin-bottom: 5px;
            color: #555;
            font-weight: bold;
        }

        form input[type="text"],
        form select {
            width: 100%;
            padding: 10px;
            margin-bottom: 15px;
            border: 1px solid #ddd;
            border-radius: 5px;
            outline: none;
            transition: border-color 0.3s;
        }

        form input[type="text"]:focus,
        form select:focus {
            border-color: #007BFF;
        }

        form input[type="submit"] {
            background-color: #007BFF;
            color: #fff;
            border: none;
            border-radius: 5px;
            padding: 10px 20px;
            font-size: 16px;
            cursor: pointer;
            transition: background-color 0.3s;
        }

        form input[type="submit"]:hover {
            background-color: #0056b3;
        }

        /* Modal Styling */
        .modal {
            display: none;
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background-color: #fff;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
            z-index: 1000;
            width: 80%;
            max-width: 400px;
            text-align: center;
        }

        .modal h2 {
            margin-bottom: 10px;
        }

        .modal p {
            margin-bottom: 20px;
        }

        .modal button {
            background-color: #007BFF;
            color: #fff;
            border: none;
            border-radius: 5px;
            padding: 10px 20px;
            font-size: 14px;
            cursor: pointer;
            transition: background-color 0.3s;
        }

        .modal button:hover {
            background-color: #0056b3;
        }

        /* Overlay */
        .overlay {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0, 0, 0, 0.5);
            z-index: 999;
        }
    </style>
</head>
<body>
    <div class="container">
        <h2>Simple Calculator</h2>
        <form id="calculatorForm">
            <label for="num1">Enter first number:</label>
            <input type="text" id="num1" name="num1" required>

            <label for="num2">Enter second number:</label>
            <input type="text" id="num2" name="num2" required>

            <label for="operation">Select an operation:</label>
            <select id="operation" name="operation">
                <option value="add">Addition</option>
                <option value="subtract">Subtraction</option>
                <option value="multiply">Multiplication</option>
                <option value="divide">Division</option>
            </select>

            <input type="submit" value="Calculate">
        </form>
    </div>

    <!-- Modal for Result -->
    <div class="overlay" id="overlay"></div>
    <div class="modal" id="resultModal">
        <h2>Result</h2>
        <p id="resultText"></p>
        <button onclick="closeModal()">Close</button>
    </div>

    <script>
        document.getElementById('calculatorForm').addEventListener('submit', function(event) {
            event.preventDefault(); // Prevent form from submitting normally

            // Get form data
            const num1 = document.getElementById('num1').value;
            const num2 = document.getElementById('num2').value;
            const operation = document.getElementById('operation').value;

            // Perform calculation
            let result;
            let operationText;

            if (isNaN(num1) || isNaN(num2)) {
                result = "Please enter valid numbers.";
            } else {
                const number1 = parseFloat(num1);
                const number2 = parseFloat(num2);

                switch (operation) {
                    case 'add':
                        result = number1 + number2;
                        operationText = "Addition";
                        break;
                    case 'subtract':
                        result = number1 - number2;
                        operationText = "Subtraction";
                        break;
                    case 'multiply':
                        result = number1 * number2;
                        operationText = "Multiplication";
                        break;
                    case 'divide':
                        if (number2 === 0) {
                            result = "Error: Division by zero is not allowed.";
                        } else {
                            result = number1 / number2;
                        }
                        operationText = "Division";
                        break;
                    default:
                        result = "Invalid operation selected.";
                        break;
                }
            }

            // Display the result in a modal
            document.getElementById('resultText').innerText = `${operationText} result: ${result}`;
            document.getElementById('overlay').style.display = 'block';
            document.getElementById('resultModal').style.display = 'block';
        });

        function closeModal() {
            document.getElementById('overlay').style.display = 'none';
            document.getElementById('resultModal').style.display = 'none';
        }
    </script>
</body>
</html>

    '''

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        # Get input from the form
        num1 = float(request.form.get('num1'))
        num2 = float(request.form.get('num2'))
        operation = request.form.get('operation')

        # Perform the selected operation
        if operation == 'add':
            result = num1 + num2
            operation_text = "Addition"
        elif operation == 'subtract':
            result = num1 - num2
            operation_text = "Subtraction"
        elif operation == 'multiply':
            result = num1 * num2
            operation_text = "Multiplication"
        elif operation == 'divide':
            if num2 == 0:
                return "<p>Error: Division by zero is not allowed.</p>"
            result = num1 / num2
            operation_text = "Division"
        else:
            return "<p>Invalid operation selected.</p>"

        # Return the result
        return f"<h2>Result</h2><p>{operation_text} of {num1} and {num2} is: {result}</p>"
    except ValueError:
        return "<p>Error: Please enter valid numbers.</p>"

if __name__ == "__main__":
    app.run(debug=True)
