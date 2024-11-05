from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def home():
    return '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Simple Calculator</title>
        </head>
        <body>
            <h2>Simple Calculator</h2>
            <form action="/calculate" method="post">
                <label for="num1">Enter first number:</label><br>
                <input type="text" id="num1" name="num1"><br><br>

                <label for="num2">Enter second number:</label><br>
                <input type="text" id="num2" name="num2"><br><br>

                <label for="operation">Select an operation:</label><br>
                <select id="operation" name="operation">
                    <option value="add">Addition</option>
                    <option value="subtract">Subtraction</option>
                    <option value="multiply">Multiplication</option>
                    <option value="divide">Division</option>
                </select><br><br>

                <input type="submit" value="Calculate">
            </form>
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
